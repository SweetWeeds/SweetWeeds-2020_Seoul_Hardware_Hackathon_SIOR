from mbed_cloud import ConnectAPI
from django.contrib.auth.models import User
from dashboard.models import Hat, SensorValue
import threading
import time

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
    devices = None
    api = None
    value = dict()
    def Init(self):
        print("Pelion sync initializing start")
        self.api = ConnectAPI()
        self.api.start_notifications()
        self.devices = api.list_connected_devices().data
        if not self.devices:
            return False
        return True
    def Query(self):
        self.devices = api.list_connected_devices().data
        for device in devices:
            try:
                hat = Hat.objects.get(device_id = device.id)
            except:
                print("New device id!:{}\nAdd new hat!".format(device.id))
                hat = Hat.objects.create(device_id = device.id)
            sv = SensorValue.objects.create(owner = hat,\
                temperature = api.get_resource_value(device.id, "/3303/0/5700"),\
                humid = api.get_resource_value(device.id, "/3304/0/5700"), \
                accelX = api.get_resource_value(device.id, "/3313/0/5702"), \
                accelY = api.get_resource_value(device.id, "/3313/0/5703"), \
                accelZ = api.get_resource_value(device.id, "/3313/0/5704"), \
                pressure = api.get_resource_value(device.id, "/3323/0/5700"), \
                distance = api.get_resource_value(device.id, "/3330/0/5700"), \
                gyroX = api.get_resource_value(device.id, "/3334/0/5702"), \
                gyroY = api.get_resource_value(device.id, "/3334/0/5703"), \
                gyroZ = api.get_resource_value(device.id, "/3334/0/5704"), \
                gps_lat = api.get_resource_value(device.id, "/3336/0/5702"), \
                gps_lng = api.get_resource_value(device.id, "/3336/0/5703"), \
                gps_alt = api.get_resource_value(device.id, "/3336/0/5704"), \
                voc = api.get_resource_value(device.id, "/10313/0/5700"), \
                air_quality = api.get_resource_value(device.id, "/10313/0/5701"))

def sync():
    syncInst = PelionSync()
    syncInst.Init()
    while True:
        syncInst.Query()
        time.sleep(5)
