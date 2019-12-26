from django.shortcuts import render
from django.shortcuts import redirect
from .models import Hat, SensorValue
from django.db.models import Max

# Create your views here.
def isauth(request):
    if request.user.is_authenticated:
        #print('auth')
        return redirect('../home')
    else:
        #print('no')
        return redirect('accounts/login')

def home(request):
    SensorValues = SensorValue.objects
    if not request.user.is_authenticated:
        return redirect('../accounts/login')
    else:
        return render(request, 'home.html', {'SensorValues' : SensorValues})


def location(request):
    Hats = Hat.objects
    return render(request, 'location.html', {'Hats': Hats})


def statistics(request):
    SensorValues = SensorValue.objects
    max_temperature = SensorValue.objects.all().aggregate(Max('temperature'))
    return render(request, 'statistics.html', {'SensorValues' : SensorValues})

''' 혁수가 보기 편할려고 추가함.
    class Hat(models.Model):
    id = models.AutoField(primary_key = True)
    user_name = models.CharField(max_length = 50)
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
'''