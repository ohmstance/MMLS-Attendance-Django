import django.db.utils
from django.urls import path
from background_task.models import Task

import datetime
import asyncio
from . import views, tasks

app_name = 'app'
urlpatterns = [
    path('course/', views.CourseView.as_view(), name='course'),
    path('load_course/', views.LoadCourseView.as_view(), name='load_course'),
    path('modify_course/', views.ModifyCourseView.as_view(), name='modify_course'),
    path('attendance/', views.AttendanceView.as_view(), name='attendance'),
    path('timetable/', views.TimetableView.as_view(), name='timetable'),
    path('timetable/<int:weekday>/', views.TimetableView.as_view(), name='timetable'),
    path('load_timetable/', views.LoadTimetableView.as_view(), name='load_timetable'),
    path('export_timetable/', views.ExportTimetableView.as_view(), name='export_timetable'),
]