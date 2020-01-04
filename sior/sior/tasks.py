from __future__ import absolute_import, unicode_literals
#from celery.decorators import task
from .celery import app
from celery import Task
import os
import sys
from mbed_cloud import ConnectAPI
from django.contrib.auth.models import User
from dashboard.models import Hat, SensorValue


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
class PelionSync(Task):
    devices = None
    api = None
    value = dict()
    def __init__(self):
        self.rate_limit = 5
        self.time_limit = 10
        try:
            print("Pelion sync initializing start")
            self.api = ConnectAPI()
            self.devices = self.api.list_connected_devices().data
            if not self.devices:
                print("[PELION] There is no registered device in Pelion!!")
                print(self.devices)
            print("[PELION] Device detected!!")
        except:
            print("[PELION] Initializing Faield!!")

@app.task(base=PelionSync)
def sync():
    try:
        sync.devices = sync.api.list_connected_devices().data
    except:
        return "[PELION] ERROR! There is no device!!"
    for device in sync.devices:
        if not device:
            return
        try:
            hat = Hat.objects.get(device_id = device.id)
        except:
            print("[PELION] New device id!:{}\nAdd new hat!".format(device.id))
            hat = Hat.objects.create(device_id = device.id)
            hat.save()
        try:
            sv = SensorValue(owner = hat, \
            temperature = sync.api.get_resource_value(device.id, "/3303/0/5700"), \
            humid = sync.api.get_resource_value(device.id, "/3304/0/5700"), \
            accelX = sync.api.get_resource_value(device.id, "/3313/0/5702"), \
            accelY = sync.api.get_resource_value(device.id, "/3313/0/5703"), \
            accelZ = sync.api.get_resource_value(device.id, "/3313/0/5704"), \
            pressure = sync.api.get_resource_value(device.id, "/3323/0/5700"), \
            distance = sync.api.get_resource_value(device.id, "/3330/0/5700"), \
            gyroX = sync.api.get_resource_value(device.id, "/3334/0/5702"), \
            gyroY = sync.api.get_resource_value(device.id, "/3334/0/5703"), \
            gyroZ = sync.api.get_resource_value(device.id, "/3334/0/5704"), \
            gps_lat = 37.29503524, \
            gps_lng = 126.9748767, \
            #gps_alt = sync.api.get_resource_value(device.id, "/3336/0/5704"), \
            #voc = sync.api.get_resource_value(device.id, "/10313/0/5700"), \
            #air_quality = sync.api.get_resource_value(device.id, "/10313/0/5701"), \
            )
            sv.save()
        except Exception as e:
            _, _ , tb = sys.exc_info() # tb -> traceback object
            print("[PELION:lineno.{}] ERROR!! Cannot get value!!".format(tb.tb_lineno))
            return e