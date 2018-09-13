from django.urls import reverse
from django.contrib.auth import login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from usuarios_app.models import UserProfileInfo
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.shortcuts import get_object_or_404,render
from django.db import connections
from . import forms
import csv
from datetime import datetime
from datetime import timedelta

class Index(LoginRequiredMixin,TemplateView):
    template_name = 'MiscelAppnea/home.html'

class Charts(LoginRequiredMixin,TemplateView):
    template_name = "MiscelAppnea/charts.html"

class Home(LoginRequiredMixin,TemplateView):
    template_name = 'MiscelAppnea/index.html'

class Register(TemplateView):
    template_name = "registration/register.html"

def registration(request):
    registered = False

    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            userProfile = UserProfileInfo.objects.create(user=user,opc_recientes=False,opc_notificaciones=False)
            registered = True

        else:
            raise ValidationError(user_form.errors)

    else:
        user_form = forms.UserForm()

    return render(request,'registration/register.html',{'user_form':user_form, 'registered':registered})

# class UserSettings(TemplateView):
#     """This is the user settings page"""
#     template_name = "comedor_app/user_settings.html"

class Reciente(LoginRequiredMixin,TemplateView):
    template_name = 'MiscelAppnea/reciente.html'
