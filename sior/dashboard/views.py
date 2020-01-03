from django.shortcuts import render
from django.shortcuts import redirect
from .models import Hat, SensorValue
from django.db.models import Max
import requests
import json
from accounts.models import Token
from mbed_cloud import ConnectAPI

# Create your views here.
def isauth(request):
    if request.user.is_authenticated:
        #print('auth')
        return redirect('../home')
    else:
        #print('no')
        return redirect('accounts/login')

def home(request):
    #kakao 때문에 추가함.
    Hats = Hat.objects
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
        return render(request, 'home.html', {'Hats' : Hats, 'SensorValues' : SensorValues, 'weather' : weather, 'max_temperature' : max_temperature, 'max_voc' : max_voc, 'max_humid' : max_humid})

def oauth(request): #for kakao api
    code = request.GET['code']
    print('code = ' + str(code))
    client_id = '2a681354f8c8188ede46e69db97dcaaa'
    redirect_uri = 'http://sior.koreasouth.cloudapp.azure.com:8000/home/oauth/'

    access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
 
    access_token_request_uri += "client_id=" + client_id
    access_token_request_uri += "&redirect_uri=" + redirect_uri
    access_token_request_uri += "&code=" + code
 
    print(access_token_request_uri)

    access_token_request_uri_data = requests.get(access_token_request_uri)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']
    print(access_token)

    user_profile_info_uri = "https://kapi.kakao.com/v1/api/talk/profile?access_token="
    user_profile_info_uri += str(access_token)
    #user_json_data 이걸 저장해서 가지고 있어야 함.
    user_profile_info_uri_data = requests.get(user_profile_info_uri)
    user_json_data = user_profile_info_uri_data.json()
    nickName = user_json_data['nickName']
    profileImageURL = user_json_data['profileImageURL']
    thumbnailURL = user_json_data['thumbnailURL']
 
    print("nickName = " + str(nickName))
    print("profileImageURL = " + str(profileImageURL))
    print("thumbnailURL = " + str(thumbnailURL))

    template_dict_data = str({
        "object_type": "feed",
        "content": {
            "title": "긴급상황 발생!!!",
            "description": "공사장 내 긴급상황 발생, 즉시 이탈할것",
            "image_url": "https://cdn.pixabay.com/photo/2013/06/09/09/07/explosion-123690_1280.jpg",
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": "http://www.daum.net",
                "mobile_web_url": "http://m.daum.net",
                "android_execution_params": "contentId=100",
                "ios_execution_params": "contentId=100"
            }
        },
        
        "social": {
            "like_count": 100,
            "comment_count": 200,
            "shared_count": 300,
            "view_count": 400,
            "subscriber_count": 500
            
        },
        
        "buttons": [
            {
                "title": "공사장 상황확인",
                "link": {
                    "web_url": "http://www.daum.net",
                    "mobile_web_url": "http://m.daum.net"
                }
            },
            {
                "title": "앱으로 이동",
                "link": {
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
            }
        ]
    })
    
    kakao_to_me_uri = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer " + access_token,
    }
    
    template_json_data = "template_object=" + str(json.dumps(template_dict_data))

    template_json_data = template_json_data.replace("\"", "")
    template_json_data = template_json_data.replace("'", "\"")
 
    response = requests.request(method="POST", url=kakao_to_me_uri, data=template_json_data, headers=headers)
    print(response.json())
    return redirect('/home')

def alert(request):
    """ Pelion 전송 """
    api = ConnectAPI()
    devices = api.list_connected_devices().data
    WRITEABLE_RESOURCE = ""
    for device in devices:
        api.set_resource_value(device_id=device.id,
                               resource_path=WRITEABLE_RESOURCE,
                               resource_value='1')
    """ Pelion 전송 """

    """ 안드로이드 앱 푸시알람 전송 """
    # fcm 푸시 메세지 요청 주소
    url = 'https://fcm.googleapis.com/fcm/send'
    ids = Token.objects.values_list('registration_token')
    ids_result = []
    for id in ids:
        ids_result.append(id[0])
    title = '위험상황 발생!'
    body = '현장 인원들은 빠르게 대피해주십시오!!'
    # 인증 정보(서버 키)를 헤더에 담아 전달
    headers = {
        'Authorization': 'key=AAAAc-2tnwg:APA91bGdyyt5YGO1gWQBYwRo0wuj1ettZn0LLGZHw6zEKg_2OWIMQdYqktsaD9t1qDR-37tHx_D1LyabvhPY32rLo1IOx9VN7ILnsOGCIhr9URdY3mr5Je72aR_dJCu-LmNu0LboBsAV',
        'Content-Type': 'application/json; UTF-8',
    }

    # 보낼 내용과 대상을 지정
    content = {
        'registration_ids': ids_result,
        'notification': {
            'title': title,
            'body': body
        }
    }
    # json 파싱 후 requests 모듈로 FCM 서버에 요청
    requests.post(url, data=json.dumps(content), headers=headers)
    """ 안드로이드 앱 푸시알람 전송 """

    """ 카카오 알람 전송 """
    # 카카오 알람 전송 - made by 혁수 #
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'

    client_id = '2a681354f8c8188ede46e69db97dcaaa'
    redirect_uri = 'http://sior.koreasouth.cloudapp.azure.com:8000/home/oauth/'
 
    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code&scope=talk_message'
    #login_request_uri += '&response_type=code'
    """ 카카오 알람 전송 """

    return redirect(login_request_uri)


def location(request):
    Hats = Hat.objects
    SensorValues = SensorValue.objects
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=08a543cc6623032ae7fe6365a5c9b994'
    city = 'Republic of Korea'
    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    weather = {
        'city' : city,
        'temperature' : round((city_weather['main']['temp']-32)*(5/9),2), #섭씨 -> 화씨 (0°F − 32) × 5/9 
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }
    return render(request, 'location.html', {'weather' : weather, 'Hats': Hats, 'SensorValues':SensorValues})


def statistics(request):
    SensorValues = SensorValue.objects.order_by('-recordtime')[:10]
    max_temperature = SensorValue.objects.aggregate(Max('temperature'))
    max_voc = SensorValue.objects.aggregate(Max('voc'))
    max_humid = SensorValue.objects.aggregate(Max('humid'))
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

def device_list(request):
    Hats = Hat.objects
    return render(request, 'device_list.html', {'Hats':Hats})

def device_info(request, hat_id):
    hat = Hat.objects.all().filter(id = hat_id)
    return render(request, 'device_info.html', {'hat':hat})

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

def criteria(request):
    return render(request, 'criteria.html', {})