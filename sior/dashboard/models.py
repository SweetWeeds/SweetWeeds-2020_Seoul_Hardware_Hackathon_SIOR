from django.db import models
from django.db.models import DateTimeField
from django.db.models import Max
MAX_LEN = 100

# Create your models here.
# worked by hangyeol
class Hat(models.Model):
    id = models.AutoField(primary_key = True)
    device_id = models.CharField(max_length = 50, null = True, unique=True)
    user_name = models.CharField(max_length = 50, null = True)
    employee_id = models.CharField(max_length = 100, null = True)
    phone_number = models.CharField(max_length = 20, null = True)
    job_position = models.CharField(max_length = MAX_LEN, null = True)
    #last_location_gps_lat = objects.filter(testfield=12).latest()
    #last_location_gps_lng = models.CharField(max_length = MAX_LEN, null = True, blank = True)
    #last_location_gps_alt = models.CharField(max_length = MAX_LEN, null = True, blank = True)
    #last_location_str = models.CharField(max_length = MAX_LEN, null = True, blank = True)
    #last_connect_date = models.DateTimeField(null = True, blank = True)

class SensorValue(models.Model):
    owner = models.ForeignKey(Hat, on_delete=models.CASCADE)        # 센서 값 소유자
    recordtime = models.DateTimeField(auto_now_add=True)            # 센서 값 기록 시간
    temperature = models.FloatField(null = True, blank = True)    # 온도 값
    humid = models.FloatField(null = True, blank = True)          # 습도 값
    accelX = models.FloatField(null = True, blank = True)
    accelY = models.FloatField(null = True, blank = True)
    accelZ = models.FloatField(null = True, blank = True)
    pressure = models.FloatField(null = True, blank = True)
    distance = models.FloatField(null = True, blank = True)
    gyroX = models.FloatField(null = True, blank = True)
    gyroY = models.FloatField(null = True, blank = True)
    gyroZ = models.FloatField(null = True, blank = True)
    gps_lat = models.FloatField(max_length = MAX_LEN, null = True, blank = True)
    gps_lng = models.FloatField(max_length = MAX_LEN, null = True, blank = True)
    gps_alt = models.FloatField(max_length = MAX_LEN, null = True, blank = True)
    voc = models.FloatField(null = True, blank = True)            # voc 값
    air_quality = models.FloatField(null = True, blank = True)
    


#max_temperature = SensorValue.objects.all().aggregate(Max('temperature'))
