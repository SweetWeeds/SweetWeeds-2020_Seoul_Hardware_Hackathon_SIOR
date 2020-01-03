from django.contrib import admin
from dashboard.models import Hat
from dashboard.models import SensorValue
from accounts.models import Token
# Register your models here.

admin.site.register(Hat)
admin.site.register(SensorValue)
admin.site.register(Token)