from django.db import models
from django.db.models import DateTimeField
MAX_LEN = 100

# Create your models here.
# worked by hangyeol
class Hat(models.Model):
    id = models.AutoField(primary_key = True)
    user_name = models.CharField(max_length = 50)
    last_connect_date = models.DateTimeField(null = True, blank = True)

class SensorVal(models.Model):
    owner = models.ForeignKey(Hat, on_delete=models.CASCADE)        # 센서 값 소유자
    recordtime = models.DateTimeField(auto_now_add=True)            # 센서 값 기록 시간
    gps = models.CharField(max_length = MAX_LEN, null = True, blank = True) # GPS값
    temperature = models.IntegerField(null = True, blank = True)    # 온도 값
    voc = models.IntegerField(null = True, blank = True)            # voc 값
    humid = models.IntegerField(null = True, blank = True)          # 습도 값
    gyro = models.CharField(max_length = MAX_LEN, null = True, blank = True)    # 자이로 센서 값