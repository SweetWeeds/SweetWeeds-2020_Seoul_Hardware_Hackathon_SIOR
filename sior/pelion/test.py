from mbed_cloud import ConnectAPI
connectApi = ConnectAPI()
import time
# List all connected devices
#devices = connectApi.list_connected_devices()

# Get the first connected device
#device = devices.data[0]

# Get resources of the first connected endpoint
device_id='016f46e17b5f000000000001001e59dc'

resources = connectApi.list_resources(device_id)

# Get resources which are observable
observable = list(filter(lambda r: r.observable, resources))
#print(observable[0].path)

# Subscribe to observable resource
connectApi.add_resource_subscription(device_id, observable[0].path)

# Register a webhook to send all updates to
#connectApi.update_webhook(WEBHOOK_URL)

# Remove webhook, and now use notifications instead
#connectApi.delete_webhook()
connectApi.start_notifications()

# Read the current resource value by blocking
resource_value = connectApi.get_resource_value(device_id, observable[0].path)

# Get next one, but do it async waiting for it to finish
async_handler = connectApi.get_resource_value_async(device_id, observable[0].path)
while not async_handler.is_done:
  time.sleep(1)
if async_handler.error:
  raise Exception("Something went wrong: %s" % (async_handler.error))
resource_value = async_handler.value