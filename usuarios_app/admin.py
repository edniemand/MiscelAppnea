from django.contrib import admin
from usuarios_app.models import UserProfileInfo,UserAppPermit,UserMenuPermit,EmpresaReporte
# Register your models here.
class UserAppPermitAdmin(admin.ModelAdmin):
    list_filter = ['user_profile']

class UserMenuPermitAdmin(admin.ModelAdmin):
    list_filter = ['user_app_permit','menu_name']

admin.site.register(UserProfileInfo)
admin.site.register(UserAppPermit,UserAppPermitAdmin)
admin.site.register(UserMenuPermit,UserMenuPermitAdmin)
admin.site.register(EmpresaReporte)

# Register your models here.
