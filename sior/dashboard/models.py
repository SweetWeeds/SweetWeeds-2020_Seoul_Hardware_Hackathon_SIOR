from django.db import models
from django.db.models import DateTimeField
from django.db.models import Max
MAX_LEN = 100

# Create your models here.
# worked by hangyeol
class Hat(models.Model):
    id = models.AutoField(primary_key = True)
    user_name = models.CharField(max_length = 50)
    employee_id = models.CharField(max_length = 100, null = True)
    phone_number = models.CharField(max_length = 20, null = True)
    job_position = models.CharField(max_length = MAX_LEN, null = True)
    last_location_gps_lat = models.CharField(max_length = MAX_LEN, null = True, blank = True)
    last_location_gps_lng = models.CharField(max_length = MAX_LEN, null = True, blank = True)
    last_location_str = models.CharField(max_length = MAX_LEN, null = True, blank = True)
    last_connect_date = models.DateTimeField(null = True, blank = True)

class SensorValue(models.Model):
    owner = models.ForeignKey(Hat, on_delete=models.CASCADE)        # 센서 값 소유자
    recordtime = models.DateTimeField(auto_now_add=True)            # 센서 값 기록 시간
    gps = models.CharField(max_length = MAX_LEN, null = True, blank = True) # GPS값
    temperature = models.IntegerField(null = True, blank = True)    # 온도 값
    voc = models.IntegerField(null = True, blank = True)            # voc 값
    humid = models.IntegerField(null = True, blank = True)          # 습도 값
    gyro = models.CharField(max_length = MAX_LEN, null = True, blank = True)    # 자이로 센서 값



#max_temperature = SensorValue.objects.all().aggregate(Max('temperature'))
