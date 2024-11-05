from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserCreateForm, ProfileUpdateForm


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            "form": create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST, files=request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully log in.')
            return redirect('books:list')
        else:
            context = {
                'login_form': login_form
            }
            return render(request, 'users/login.html', context)


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'user': request.user
        }
        return render(request, 'users/profile.html', context)


class LogOutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.info(request, 'You have successfully logged out.')
        return redirect('common:landing_page')


class ProfileUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        profile_edit_form = ProfileUpdateForm(instance=request.user)
        context = {
            "form": profile_edit_form
        }
        return render(request, 'users/profile-edit.html', context)

    def post(self, request):
        profile_edit_form = ProfileUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )

        if profile_edit_form.is_valid():
            profile_edit_form.save()
            return redirect('users:profile')
        context = {
            "form": profile_edit_form
        }
        return render(request, 'users/profile-edit.html', context)
