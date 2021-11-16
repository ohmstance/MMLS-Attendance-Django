import asyncio
import json
import datetime
from django.http.response import Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator, classonlymethod
from django.contrib import messages
from asgiref.sync import async_to_sync, sync_to_async
from django.utils import timezone
from django.http import FileResponse

# Create your views here.
from .modules import mmlsattendance, mmu_ics
from .models import UserData

class CourseView(generic.View):
    template_name = "app/course.html"

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        course_raw = UserData.objects.get(user=user.pk).course
        course = mmlsattendance.Courses()
        course.load_json(json.dumps(course_raw))
        if len(course.subjects) == 0:
            messages.info(request, "No courses loaded.")
        return render(request, self.template_name, {'course': course})

class LoadCourseView(generic.View):

    @method_decorator(login_required)
    def post(self, request):
        try:
            mmls_username = request.POST['mmls_username']
            mmls_password = request.POST['mmls_password']
        except:
            return HttpResponseForbidden()
        user = request.user
        course = mmlsattendance.Courses()
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            authenticated = loop.run_until_complete(course.load_online(mmls_username, mmls_password))
            if authenticated:
                loop.run_until_complete(course.autoselect_classes(mmls_username))
                user_app_data = UserData.objects.get(user=user.pk)
                user_app_data.course = json.loads(course.json())
                user_app_data.save()
                messages.success(request, "Courses loaded successfully.")
            else:
                messages.error(request, "Your username and password didn't match. Please try again.")
        except mmlsattendance.MMLSResponseError:
            messages.error(request, "Something went wrong. Please try again later.")
            return redirect("app:course")
        finally:
            loop.close()
        return redirect("app:course")

class ModifyCourseView(generic.View):

    @method_decorator(login_required)
    def post(self, request):
        checked_values = request.POST.getlist('class[]')
        user = request.user
        course = mmlsattendance.Courses()
        course_raw = UserData.objects.get(user=user.pk).course
        course.load_json(json.dumps(course_raw))
        for a_class in course.classes:
            if str(a_class.id) in checked_values:
                a_class.selected = True
            else:
                a_class.selected = False
        user_app_data = UserData.objects.get(user=user.pk)
        user_app_data.course = json.loads(course.json())
        user_app_data.save()
        messages.success(request, "Class selection updated.")
        return redirect("app:course")

class TimetableView(generic.View):
    template_name = "app/timetable.html"

    @method_decorator(login_required)
    def get(self, request, weekday=None):
        if weekday is None:
            tzinfo = datetime.timezone(datetime.timedelta(hours=8), name="Malaysian Standard Time (MST)")
            dtnow = datetime.datetime.now(tzinfo)
            weekday = dtnow.today().weekday()
        if not (0 <= weekday <= 6):
            return redirect("app:timetable")
        user = request.user
        timetable = UserData.objects.get(user=user.pk).timetable
        if len(timetable) == 0:
            messages.info(request, "Timetable not loaded.")
        weekday_day = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday',
        }
        timetable_flattened = (event for day in timetable for event in day)
        schedule = [event for event in timetable_flattened if event['day'] == weekday_day[weekday]]
        return render(request, self.template_name, {'schedule': schedule, 'weekday': weekday})

class LoadTimetableView(generic.View):

    @method_decorator(login_required)
    def post(self, request):
        try:
            mmls_username = request.POST['mmls_username']
            mmls_password = request.POST['mmls_password']
        except:
            return HttpResponseForbidden()
        user = request.user
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            timetable = loop.run_until_complete(mmu_ics.get_timetable_mmumobileapi(mmls_username, mmls_password))
            if timetable: # If not empty
                user_app_data = UserData.objects.get(user=user.pk)
                user_app_data.timetable = timetable
                user_app_data.save()
                messages.success(request, "Timetable loaded successfully.")
            else:
                messages.error(request, "Your username and password didn't match, or timetable is empty. Please try again later.")
        except mmu_ics.RateLimitError:
            messages.error(request, "Rate-limited. Please try again later.")
            return redirect("app:timetable")
        finally:
            loop.close()
        return redirect("app:timetable")

class ExportTimetableView(generic.View):

    @method_decorator(login_required)
    def post(self, request):
        try:
            date1 = datetime.date.fromisoformat(request.POST['date1'])
            date2 = datetime.date.fromisoformat(request.POST['date2'])
        except:
            return HttpResponseBadRequest()
        user = request.user
        timetable = UserData.objects.get(user=user.pk).timetable
        f = mmu_ics.ics_from_timetable(timetable, date1, date2)
        f.seek(0)
        response = FileResponse(f, as_attachment=True, filename=f"mmutimetable-{user.username}.ics")
        return response

class AttendanceView(generic.View):
    template_name = "app/attendance.html"

    @method_decorator(login_required)
    def get(self, request):
        tz = datetime.timezone(datetime.timedelta(hours=8))
        date1_str = request.GET.get("date1", datetime.datetime.now(tz).date().isoformat())
        date2_str =  request.GET.get("date2", date1_str)
        try:
            date1 = datetime.date.fromisoformat(date1_str)
            date2 = datetime.date.fromisoformat(date2_str)
        except ValueError:
            date1 = datetime.datetime.now(tz).replace(tzinfo=None).date()
            date2 = date1
        dates = [(date1 + datetime.timedelta(days=x)).isoformat() for x in range((date2-date1).days+1)]

        user = request.user
        course = mmlsattendance.Courses()
        course_raw = UserData.objects.get(user=user.pk).course
        course.load_json(json.dumps(course_raw))
        subject_ids = {subject.id for subject in course.subjects}

        with open("app/modules/attendance_cache.json", "r+") as f:
            scraper = mmlsattendance.Scraper(f)

        async def list_from_async_generator(async_gen, *args, **kwargs):
            result_list = []
            async for result in async_gen(*args, **kwargs):
                result_list.append(result)
            return result_list

        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            attendances = loop.run_until_complete(
                list_from_async_generator(scraper.scrape_date, course, date1, date2, do_requests=False)
            )
        finally:
            loop.close()

        for attendance in attendances:
            start_datetime = datetime.datetime.fromisoformat(f"{attendance.class_date}T{attendance.start_time}")
            end_datetime = datetime.datetime.fromisoformat(f"{attendance.class_date}T{attendance.end_time}")
            now_datetime = datetime.datetime.now(tz).replace(tzinfo=None)
            attendance.upcoming = start_datetime > now_datetime
            attendance.in_progress = start_datetime <= now_datetime < end_datetime
            attendance.ended = now_datetime >= end_datetime

        # found_dates = []
        # for date in dates:
        #     if next((True for attendance in attendances if attendance.class_date == date), False):
        #         found_dates.append(date)

        # {date_str: {subject: [attendance, ... ], ... }, ... }
        categorized_attendances = {}

        for date in dates:
            filtered_subjects = {}
            for subject in course.subjects:
                # Append to attendance list if belong to subject and date
                filtered_attendances = [
                    attendance for attendance in attendances
                    if attendance.subject_id == subject.id
                    and attendance.class_date == date
                ]
                # Sort attendances by start time
                filtered_attendances = sorted(filtered_attendances, key=lambda attendance: attendance.start_time)
                if filtered_attendances:
                    filtered_subjects.update({subject: filtered_attendances})
            if filtered_subjects:
                categorized_attendances.update({date: filtered_subjects})


        if len(attendances) == 0:
            messages.info(request, "No attendances found.")

        return render(request, self.template_name, {'categorized_attendances': categorized_attendances, 'date1': date1, 'date2': date2})
