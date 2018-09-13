from django.conf.urls import url

from . import views

app_name = 'usuarios_app'

urlpatterns = [
    #url(r"^perfil/$", views.PerfilUsuario.as_view(), name="perfil"),
    url(r"perfil/(?P<pk>\d+)/$",views.PerfilUsuario.as_view(),name="perfil"),
    url(r"usuarios/$",views.Usuarios.as_view(),name="usuarios"),
]
