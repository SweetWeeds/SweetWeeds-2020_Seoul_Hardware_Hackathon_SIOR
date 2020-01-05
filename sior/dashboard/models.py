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
    risk_level = models.CharField(max_length = 10, \
        choices=(('정상', 1), ('주의',2), ('위험', 3)), default=1)
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
    co2 = models.FloatField(null = True, blank = True)            # co2 값
    air_quality = models.FloatField(null = True, blank = True)
    
class SensorCriteria(models.Model):
    temperature_normal = models.FloatField(null = True, blank = True)
    temperature_warning = models.FloatField(null = True, blank = True)
    temperature_dangerous = models.FloatField(null = True, blank = True)
    humid_normal = models.FloatField(null = True, blank = True)
    humid_warning = models.FloatField(null = True, blank = True)
    humid_dangerous = models.FloatField(null = True, blank = True)
    pressure_normal = models.FloatField(null = True, blank = True)
    pressure_warning = models.FloatField(null = True, blank = True)
    pressure_dangerous = models.FloatField(null = True, blank = True)
    voc_normal = models.FloatField(null = True, blank = True)            # voc 값
    voc_warning = models.FloatField(null = True, blank = True)            # voc 값
    voc_dangerous = models.FloatField(null = True, blank = True)            # voc 값
    air_quality_normal = models.FloatField(null = True, blank = True)
    air_quality_warning = models.FloatField(null = True, blank = True)
    air_quality_dangerous = models.FloatField(null = True, blank = True)

class isWarning(models.Model):
    isWarning = models.IntegerField(null = False, blank = True, default=0)
