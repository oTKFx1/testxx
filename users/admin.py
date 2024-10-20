from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.User)
admin.site.register(models.SpecialistProfile)
admin.site.register(models.Specialization)
admin.site.register(models.NormalUserInfo)
admin.site.register(models.CyberSecurityCategory)