from django.contrib import admin
from comedor_app.models import Comedor,ComedorDetalle,Opcion

# Register your models here.
#admin.site.register(Comedor)
class ComedorAdmin(admin.ModelAdmin):

    fields = ['empresa','ejercicio','semana','aplicado','validado','bloqueado']

    #search_fields = ['title','release_year']

    #list_filter = ['release_year','length']

    list_display = ['id','empresa','semana','ejercicio','aplicado','validado','bloqueado']

    #list_editable = ['lunes','martes','miercoles','jueves','viernes']
class ComedorDetalleAdmin(admin.ModelAdmin):

    #fields = ['empresa','ejercicio','semana','aplicado','validado','bloqueado']

    #search_fields = ['title','release_year']

    list_filter = ['id_comedor']

    list_display = ['nombre_empleado','lunes','martes','miercoles','jueves','viernes','sabado','domingo','total']

    list_editable = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo','total']
class OpcionAdmin(admin.ModelAdmin):

    #fields = ['empresa','ejercicio','semana','aplicado','validado','bloqueado']

    #search_fields = ['title','release_year']

    #list_filter = ['release_year','length']

    list_display = ['semana','dia','comida','id_comedor_detalle','empresa']

    #list_editable = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo','total']

admin.site.register(Comedor,ComedorAdmin)
admin.site.register(ComedorDetalle,ComedorDetalleAdmin)
admin.site.register(Opcion,OpcionAdmin)
