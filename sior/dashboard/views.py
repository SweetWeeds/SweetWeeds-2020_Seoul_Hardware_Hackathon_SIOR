from django.shortcuts import render
from django.shortcuts import redirect
from .models import Hat, SensorValue
from django.db.models import Max
import requests

# Create your views here.
def isauth(request):
    if request.user.is_authenticated:
        #print('auth')
        return redirect('../home')
    else:
        #print('no')
        return redirect('accounts/login')

def home(request):
    #여기부터 날씨 때문에 추가함.
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=08a543cc6623032ae7fe6365a5c9b994'
    city = 'Republic of Korea'
    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    weather = {
        'city' : city,
        'temperature' : round((city_weather['main']['temp']-32)*(5/9),2), #섭씨 -> 화씨 (0°F − 32) × 5/9 
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }
    #여기까지 내가 추가함.

    SensorValues = SensorValue.objects
    max_temperature = SensorValue.objects.all().aggregate(Max('temperature'))
    max_voc = SensorValue.objects.all().aggregate(Max('voc'))
    max_humid = SensorValue.objects.all().aggregate(Max('humid'))
    if not request.user.is_authenticated:
        return redirect('../accounts/login')
    else:
        return render(request, 'home.html', {'SensorValues' : SensorValues, 'weather' : weather, 'max_temperature' : max_temperature, 'max_voc' : max_voc, 'max_humid' : max_humid})

def oauth(request): #for kakao api
    code = request.GET['code']
    print('code = ' + str(code))

    return redirect('../home')


def location(request):
    Hats = Hat.objects
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=08a543cc6623032ae7fe6365a5c9b994'
    city = 'Republic of Korea'
    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    weather = {
        'city' : city,
        'temperature' : round((city_weather['main']['temp']-32)*(5/9),2), #섭씨 -> 화씨 (0°F − 32) × 5/9 
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }
    return render(request, 'location.html', {'weather' : weather, 'Hats': Hats})


def statistics(request):
    SensorValues = SensorValue.objects
    max_temperature = SensorValue.objects.all().aggregate(Max('temperature'))
    max_voc = SensorValue.objects.all().aggregate(Max('voc'))
    max_humid = SensorValue.objects.all().aggregate(Max('humid'))
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=08a543cc6623032ae7fe6365a5c9b994'
    city = 'Republic of Korea'
    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    weather = {
        'city' : city,
        'temperature' : round((city_weather['main']['temp']-32)*(5/9),2), #섭씨 -> 화씨 (0°F − 32) × 5/9 
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }
    return render(request, 'statistics.html', {'SensorValues' : SensorValues, 'weather' : weather, 'max_temperature' : max_temperature, 'max_voc' : max_voc, 'max_humid' : max_humid})


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