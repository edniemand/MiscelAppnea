from django.conf.urls import url

from . import views

app_name = 'comedor_app'

urlpatterns = [
    url(r"^comedor/$", views.ComedorView.as_view(), name="comedor"),
    url(r"^consumos/$", views.Consumos.as_view(), name="consumos"),
    url(r"^listas/$", views.GenerarListas.as_view(), name="listas"),
    url(r"^opciones/$", views.Opciones.as_view(), name="opciones"),
    url('ajax/load-empleados/', views.load_empleados, name='ajax_load_empleados'),
]
