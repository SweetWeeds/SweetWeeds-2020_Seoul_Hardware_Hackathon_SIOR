import requests

URL = 'https://api.us-east-1.mbedcloud.com/v2'
API_KEY = 'ak_1MDE2ZjA3Zjk1NWEzYWUzY2U2MGZlZWU4MDAwMDAwMDA016f084eb876925aab47482d0000000088LlSQgw7Yq2b8r8M260VQhbZn17bCqu'
DEVICE_ID = ['016f46e17b5f000000000001001e59dc']

class PelionSync:
    def PostValue():
        return 
    def GetValue():
        return val
headers = {
    'Authorization': 'Bearer {}'.format(),
}

response = requests.get('https://api.us-east-1.mbedcloud.com/v2/endpoints/', headers=headers)

print(response.text)
