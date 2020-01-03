from django import template
from ..models import Hat, SensorValue

register = template.Library()

@register.filter
def get_last_pos(hat):
    if not hat:
        hat = Hat.objects.last()
    SensorValues = SensorValue.objects.all()
    returnVal = "{}, {}".format(SensorValues.filter(owner=hat).last().gps_lat, SensorValues.filter(owner=hat).last().gps_lng)
    return returnVal

@register.filter
def get_last_date(hat):
    if not hat:
        hat = Hat.objects.last()
    SensorValues = SensorValue.objects.all()
    returnVal = SensorValues.filter(owner=hat).last().recordtime
    return returnVal