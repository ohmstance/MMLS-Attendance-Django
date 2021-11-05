from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User, Permission
from django.contrib import auth

# Create your tests here.

class AccTests(TestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "complicatedpassword123"
        self.password_simple = "password"
        self.password_changeto = "extracomplicatedpassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.username2 = "testuser2"

    def test_registration_page_url(self):
        response = self.client.get("/acc/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='acc/register.html')

    def test_registration_page_view_name(self):
        response = self.client.get(reverse('acc:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='acc/register.html')

    def test_login_page_url(self):
        response = self.client.get("/acc/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='acc/login.html')

    def test_login_page_view_name(self):
        response = self.client.get(reverse('acc:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='acc/login.html')

    def test_acc_page_url(self):
        response = self.client.get("/acc/")
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/acc/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='acc/account.html')

    def test_acc_page_view_name(self):
        response = self.client.get(reverse('acc:account'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('acc:account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='acc/account.html')

    def test_registration_form(self):
        init_size = len(User.objects.all())
        response = self.client.post(reverse('acc:register'), data={
            'username': self.username2,
            'password1': self.password_simple,
            'password2': self.password_simple
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(User.objects.all()), init_size)
        for i in range(2):
            response = self.client.post(reverse('acc:register'), data={
                'username': self.username2,
                'password1': self.password,
                'password2': self.password
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(len(User.objects.all()), init_size+1)

    def test_login_form(self):
        response = self.client.post(reverse('acc:login'), data={
            'username': self.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        response = self.client.post(reverse('acc:login'), data={
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.client.logout()

    def test_settings_form(self):
        self.client.login(username=self.username, password=self.password)
        for i in range(2):
            init_adv = User.objects.get(username=self.username).has_perm('app.can_view_all_attendance')
            if init_adv:
                self.client.post(reverse('acc:config'))
            else:
                self.client.post(reverse('acc:config'), {'advanced_mode': 'on'})
            post_adv = User.objects.get(username=self.username).has_perm('app.can_view_all_attendance')
            self.assertNotEqual(post_adv, init_adv)
        self.client.logout()

    def test_password_change_form(self):
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse('acc:password_change'), data={
            'old_password': self.password,
            'new_password1': self.password_changeto,
            'new_password2': self.password_changeto
        })
        self.client.logout()
        self.assertFalse(self.client.login(username=self.username, password=self.password))
        self.assertTrue(self.client.login(username=self.username, password=self.password_changeto))
        self.client.logout()

    def test_delete_account_form(self):
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse('acc:user_delete'), data={
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(len(User.objects.filter(username=self.username)), 0)


