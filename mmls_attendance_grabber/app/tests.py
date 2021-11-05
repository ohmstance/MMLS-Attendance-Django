from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from .models import UserData

# Create your tests here.

class AppTests(TestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "complicatedpassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_course_page_url(self):
        response = self.client.get("/app/course/")
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/app/course/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='app/course.html')

    def test_course_page_view_name(self):
        response = self.client.get(reverse("app:course"))
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("app:course"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='app/course.html')

    def test_timetable_page_url(self):
        response = self.client.get("/app/timetable/")
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/app/timetable/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='app/timetable.html')

    def test_timetable_page_view_name(self):
        response = self.client.get(reverse("app:timetable"))
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("app:timetable"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='app/timetable.html')

    def test_attendance_page_url(self):
        response = self.client.get("/app/attendance/")
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/app/attendance/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='app/attendance.html')

    def test_attendance_page_view_name(self):
        response = self.client.get(reverse("app:attendance"))
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("app:attendance"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='app/attendance.html')

    def test_user_userdata_one_to_one_relation(self):
        self.user = User.objects.create_user(username='testuser1', password=self.password)
        self.user = User.objects.create_user(username='testuser2', password=self.password)
        self.user = User.objects.create_user(username='testuser3', password=self.password)

        user = User.objects.get(username=self.username)
        userdata = user.userdata
        self.assertEqual(len(User.objects.filter(userdata=userdata)), 1)
        self.assertEqual(len(UserData.objects.filter(user=user)), 1)

    # Todo: Additional test cases, maybe unit test, to test validity of json in JSONField in UserData model.