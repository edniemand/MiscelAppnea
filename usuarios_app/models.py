from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional fields
    opc_recientes = models.BooleanField(default=False)
    opc_notificaciones = models.BooleanField(default=False)
    indicadores = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('usuarios_app:perfil',kwargs={'pk':self.pk})

class UserAppPermit(models.Model):
    user_profile = models.ForeignKey(UserProfileInfo, related_name='user_apps', on_delete=models.CASCADE)

    app_name = models.CharField(max_length=128)
    value = models.CharField(blank=True, max_length=6)

    def __str__(self):
        return self.user_profile.user.username + '-' + self.app_name

class UserMenuPermit(models.Model):
    user_app_permit = models.ForeignKey(UserAppPermit, related_name='user_menus', on_delete = models.CASCADE)

    menu_name = models.CharField(max_length=128)
    value = models.CharField(blank=True, max_length=6)

    def __str__(self):
        return str(self.user_app_permit.user_profile) + '-' + self.menu_name

class EmpresaReporte(models.Model):
    user_company_permit = models.ForeignKey(UserProfileInfo, related_name='user_companies', on_delete = models.CASCADE)

    company_name = models.CharField(max_length=128)

    def __str__(self):
        return self.user_company_permit.user.username + '-' + self.company_name
