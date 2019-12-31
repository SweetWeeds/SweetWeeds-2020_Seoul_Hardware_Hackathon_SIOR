from __future__ import absolute_import, unicode_literals
from celery.decorators import task
import os
from mbed_cloud import ConnectAPI
from django.contrib.auth.models import User
from dashboard.models import Hat, SensorValue
import threading
import time
"""
# `celery` 프로그램을 작동시키기 위한 기본 장고 세팅 값을 정한다. 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sior.settings')
 
app = Celery('sior')
 
# namespace='CELERY'는 모든 셀러리 관련 구성 키를 의미한다. 반드시 CELERY라는 접두사로 시작해야 한다. 
app.config_from_object('django.conf:settings', namespace='CELERY')
 
# 장고 app config에 등록된 모든 taks 모듈을 불러온다. 
app.autodiscover_tasks()

#@app.task
#def add(x, y):
#    return x + y
"""

RESOURCE_PATH_NAME = \
    {"/3303/0/5700":"temperature", \
        "/3304/0/5700":"humid", \
        "/3313/0/5702":"accelX", \
        "/3313/0/5703":"accelY", \
        "/3313/0/5704":"accelZ", \
        "/3323/0/5700":"pressure", \
        "/3330/0/5700":"distance", \
        "/3334/0/5702":"gyroX", \
        "/3334/0/5703":"gyroY", \
        "/3334/0/5704":"gyroZ", \
        "/3336/0/5702":"gps_lat", \
        "/3336/0/5703":"gps_lng", \
        "/3336/0/5704":"gps_alt", \
        "/10313/0/5700":"voc", \
        "/10313/0/5701":"air_quality"
    }
class PelionSync():
    initialized = False
    devices = None
    api = None
    value = dict()
    def Init(self):
        print("Pelion sync initializing start")
        self.api = ConnectAPI()
        self.api.start_notifications()
        self.devices = self.api.list_connected_devices().data
        if not self.devices:
            print("[PELION] There is no registered device in Pelion!!")
            return False
        print("[PELION] Device detected!!")
        self.initialized = True
        return True
    def Query(self):
        self.devices = self.api.list_connected_devices().data
        for device in self.devices:
            try:
                hat = Hat.objects.get(device_id = device.id)
            except:
                print("New device id!:{}\nAdd new hat!".format(device.id))
                hat = Hat.objects.create(device_id = device.id)
            """
            sv = SensorValue.objects.create(owner = hat)
            sv.update(temperature = self.api.get_resource_value(device.id, "/3303/0/5700"))
            sv.update(humid = self.api.get_resource_value(device.id, "/3304/0/5700"))
            sv.update(accelX = self.api.get_resource_value(device.id, "/3313/0/5702"))
            sv.update(accelY = self.api.get_resource_value(device.id, "/3313/0/5703"))
            sv.update(accelZ = self.api.get_resource_value(device.id, "/3313/0/5704"))
            sv.update(pressure = self.api.get_resource_value(device.id, "/3323/0/5700"))
            sv.update(distance = self.api.get_resource_value(device.id, "/3330/0/5700"))
            sv.update(gyroX = self.api.get_resource_value(device.id, "/3334/0/5702"))
            sv.update(gyroY = self.api.get_resource_value(device.id, "/3334/0/5703"))
            sv.update(gyroZ = self.api.get_resource_value(device.id, "/3334/0/5704"))
            sv.update(gps_lat = self.api.get_resource_value(device.id, "/3336/0/5702"))
            sv.update(gps_lng = self.api.get_resource_value(device.id, "/3336/0/5703"))
            sv.update(gps_alt = self.api.get_resource_value(device.id, "/3336/0/5704"))
            sv.update(voc = self.api.get_resource_value(device.id, "/10313/0/5700"))
            sv.update(air_quality = self.api.get_resource_value(device.id, "/10313/0/5701"))
            sv.save()
            """

syncInst = PelionSync()
syncInst.Init()
@task(name='sync')
def sync():
    if syncInst.initialized == True:
        syncInst.Query()
    print('Not initialized!!')

"""
@task(name='test')
def test():
    print('Hello World!')
    return 'test'
"""