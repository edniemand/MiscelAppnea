from django.shortcuts import render
from django.views.generic import TemplateView,UpdateView
from django.db import connections,transaction
from datetime import datetime
from usuarios_app.models import UserProfileInfo
from usuarios_app.forms import UserForm,UserProfileInfoForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
# Create your views here.
class PerfilUsuario(LoginRequiredMixin,UpdateView):
    template_name = 'usuarios_app/user_settings.html'
    # login_url = '/login/'
    # redirect_field_name = 'index.html'

    model = UserProfileInfo
    fields = ('opc_recientes','opc_notificaciones','indicadores')

    def post(self, request, **kwargs):
        context = super().post(request,**kwargs)
        if request.method == 'POST':
            my_data = request.POST
            fuser = request.POST.get('username')
            profile_form = UserProfileInfoForm(data=request.POST)

            first_name = my_data['first_name']
            last_name = my_data['last_name']
            email = my_data['email']

            print('profile_form: ',profile_form)
            user= User.objects.filter(username=fuser).update(first_name=first_name,last_name=last_name,email=email)

            return render(request,'usuarios_app/user_settings.html',{'profile_form':profile_form})
        else:
            user_form = forms.UserForm()
            profile_form = forms.UserProfileInfoForm()

            return render(request,'usuarios_app/user_settings.html',{'user_form':user_form, 'profile_form':profile_form})

class Usuarios(LoginRequiredMixin,TemplateView):
    template_name = 'usuarios_app/usuarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.order_by('last_name')
        context  = {'user':user}
        return context
