from django.db import models
from django.db.models import DateTimeField
MAX_LEN = 100

# Create your models here.
class Hat(model.Model):
    id = models.AutoField(primary_key = True)
    user_name = models.CharField(max_length = 50)
    gps = models.CharField(max_length = MAX_LEN, null = True, blank = True)
    temperature = models.IntegerField(null = True, blank = True)
    voc = models.IntegerField(null = True, blank = True)
    tof = models.IntegerField(null = True, blank = True)
    humid = models.IntegerField(null = True, blank = True)
    gyro = models.CharField(max_length = MAX_LEN, null = True, blank = True)
    last_connect_date = models.DateTimeField(null = True, blank = True)