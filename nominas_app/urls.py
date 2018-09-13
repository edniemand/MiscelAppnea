from django.conf.urls import url

from . import views

app_name = 'nominas_app'

urlpatterns = [
    url(r"^nominas/$", views.Nominas.as_view(), name="nominas"),
    url(r"^alimentos/$", views.Alimentos.as_view(), name="alimentos"),
    url(r"^bancos/$", views.Bancos.as_view(), name="bancos"),
    url(r"^dispersion/$", views.Dispersion.as_view(), name="dispersion"),
    url(r"^factura/$", views.Factura.as_view(), name="factura"),
    url(r"^fondo_ahorro/$", views.FondoAhorro.as_view(), name="fondo_ahorro"),
    url(r"^acumulados/$", views.Acumulados.as_view(), name="acumulados"),
    url(r"^promobien/$", views.Promobien.as_view(), name="promobien"),
    url(r"^asistencia/$", views.Asistencia.as_view(), name="asistencia"),
    url(r'^empleado/$', views.Empleado, name="empleado"),
]
