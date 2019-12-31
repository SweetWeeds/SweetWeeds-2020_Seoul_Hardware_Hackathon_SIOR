# ---------------------------------------------------------------------------
# Pelion Device Management SDK
# (C) COPYRIGHT 2017 Arm Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------
"""Example showing basic usage of the webhook functionality.
from mbed_cloud import ConnectAPI
import time

BUTTON_RESOURCE = "/5002/0/1"


def _main():
    api = ConnectAPI()
    devices = api.list_connected_devices().data
    if len(devices) == 0:
        raise Exception("No endpints registered. Aborting")
    # Delete device subscriptions
    api.delete_device_subscriptions(devices[0].id)
    # First register to webhook
    api.update_webhook("https://webhook.site/6468f765-be2a-4053-8a53-cd0951cb9529")
    time.sleep(2)
    api.add_resource_subscription(devices[0].id, BUTTON_RESOURCE)
    while True:
        print("Webhook registered. Listening to button updates for 10 seconds...")

        time.sleep(10)
        break

    api.delete_webhook()
    print("Deregistered and unsubscribed from all resources. Exiting.")


if __name__ == '__main__':
    _main()
"""
from mbed_cloud import ConnectAPI
import time
BUTTON_RESOURCE = "/3313/0/5702"


def _current_val(value):
    # Print the current value
    print("Current value: %r" % (value))


def _subscription_handler(device_id, path, value):
    print("Device: %s, Resoure path: %s, Current value: %r" % (device_id, path, value))


def _main():
    api = ConnectAPI()
    # calling start_notifications is required for getting/setting resource synchronously
    #api.start_notifications()
    devices = api.list_connected_devices().data
    if not devices:
        raise Exception("No connected devices registered. Aborting")

    # Synchronously get the initial/current value of the resource
    value = api.get_resource_value(devices[0].id, BUTTON_RESOURCE)
    _current_val(value)

    # Register a subscription for new values
    #api.add_resource_subscription_async(devices[0].id, BUTTON_RESOURCE, _subscription_handler)

    # Run forever
    while True:
        value = api.get_resource_value(devices[0].id, BUTTON_RESOURCE)
        svtemperature = api.get_resource_value(devices[0].id, "/3303/0/5700")
        print(svtemperature)
        svhumid = api.get_resource_value(devices[0].id, "/3304/0/5700")
        print(svhumid)
        svaccelX = api.get_resource_value(devices[0].id, "/3313/0/5702")
        svaccelY = api.get_resource_value(devices[0].id, "/3313/0/5703")
        svaccelZ = api.get_resource_value(devices[0].id, "/3313/0/5704")
        svpressure = api.get_resource_value(devices[0].id, "/3323/0/5700")
        svdistance = api.get_resource_value(devices[0].id, "/3330/0/5700")
        svgyroX = api.get_resource_value(devices[0].id, "/3334/0/5702")
        svgyroY = api.get_resource_value(devices[0].id, "/3334/0/5703")
        svgyroZ = api.get_resource_value(devices[0].id, "/3334/0/5704")
        print("gyroz:{}".format(svgyroZ))
        svgps_lat = api.get_resource_value(devices[0].id, "/3336/0/5702")
        print(svgps_lat)
        svgps_lng = api.get_resource_value(devices[0].id, "/3336/0/5703")
        svgps_alt = api.get_resource_value(devices[0].id, "/3336/0/5704")
        svvoc = api.get_resource_value(devices[0].id, "/10313/0/5700")
        svair_quality = api.get_resource_value(devices[0].id, "/10313/0/5701")
        time.sleep(5)
        #pass


if __name__ == "__main__":
    _main()