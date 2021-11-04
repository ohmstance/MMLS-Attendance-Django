from django.contrib import auth
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth import forms, update_session_auth_hash, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import classonlymethod, method_decorator
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

class AccountView(generic.View):
    template_name = "acc/account.html"

    @method_decorator(login_required)
    def get(self, request):
        password_change_form = forms.PasswordChangeForm(user=request.user)
        user_delete_form = forms.AuthenticationForm()
        form = {
            'password_change_form': password_change_form,
            'user_delete_form': user_delete_form
        }
        return render(request, self.template_name, form)

class PasswordChangeView(generic.View):

    @method_decorator(login_required)
    def post(self, request):
        form = forms.PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully updated.')
        else:
            for errors in form.errors.values():
                for error_message in errors:
                    messages.error(request, error_message)
        return redirect('acc:account')

class UserDeleteView(generic.View):

    @method_decorator(login_required)
    def post(self, request):
        form = forms.AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('common:index')
        else:
            for errors in form.errors.values():
                for error_message in errors:
                    messages.error(request, error_message)
        return redirect('acc:account')

class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = "acc/login.html"
    success_message = "You have logged in."

class RegisterView(generic.View):
    template_name = "acc/register.html"

    def get(self, request):
        form = forms.UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account '{username}' registered successfully.")
        else:
            for errors in form.errors.values():
                for error_message in errors:
                    messages.error(request, error_message)
        return redirect("acc:register")

class LogoutView(generic.View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "You have logged out.")
        return redirect("common:index")

class ConfigView(generic.View):

    @method_decorator(login_required)
    def post(self, request):
        user = request.user

        # Advanced mode
        permission = Permission.objects.get(codename = "can_view_all_attendance")
        if request.POST.get('advanced_mode', None):
            user.user_permissions.add(permission)
        else:
            user.user_permissions.remove(permission)

        user.save()
        return redirect('acc:account')
