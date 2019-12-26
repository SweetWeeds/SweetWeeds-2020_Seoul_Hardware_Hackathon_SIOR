from django.contrib import admin
from dashboard.models import Hat
from dashboard.models import SensorValue
# Register your models here.

admin.site.register(Hat)
admin.site.register(SensorValue)