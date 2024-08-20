from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Staff)
admin.site.register(TransportOfficer)
admin.site.register(Department)
admin.site.register(Vehicle)
admin.site.register(CarRequest)

