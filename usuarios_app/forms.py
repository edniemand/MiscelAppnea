from django import forms
from usuarios_app import models
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ('username','email','password','first_name','last_name')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = models.UserProfileInfo
        fields=('opc_recientes','opc_notificaciones','indicadores')
