import os
import requests
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth import authenticate, login, logout
from . import forms
from . import models


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verify = True
        user.save()
        user.email_secret = ""
    except models.User.DoesNotExist:
        pass
    return redirect(reverse("core:home"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = 'users/update_profile.html'
    fields = (
        "first_name",
        "last_name",
        "bio",
        "gender",
        "birthdate",
        "language",
        "currency",
    )

    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['first_name'].widget.attrs = {"placeholder": "First name"}
        form.fields['last_name'].widget.attrs = {"placeholder": "Last name"}
        form.fields['bio'].widget.attrs = {"placeholder": "Bio"}
        form.fields['birthdate'].widget.attrs = {"placeholder": "Birthdate"}
        return form


class UpdatePassword(SuccessMessageMixin, PasswordChangeView):
    template_name = "users/change-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current Password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "Confirm New Password"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()
