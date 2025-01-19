from django.contrib import admin
from .models import Vehicle, Rental, Location, Operator, VehicleActivity, Report, Payment, Manager

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Rental)
admin.site.register(Location)
admin.site.register(Operator)
admin.site.register(VehicleActivity)
admin.site.register(Report)
admin.site.register(Payment)
admin.site.register(Manager)
