import requests
from ast import literal_eval
URL = 'https://api.us-east-1.mbedcloud.com/v2/endpoints/016f46e17b5f000000000001001e59dc'
headers = {
    'Authorization': 'Bearer ak_1MDE2ZjA3Zjk1NWEzYWUzY2U2MGZlZWU4MDAwMDAwMDA016f084eb876925aab47482d0000000088LlSQgw7Yq2b8r8M260VQhbZn17bCqu',
}
#response1 = requests.post(URL, headers=headers, params=params)
response2 = requests.get(URL + '/3304/0/5700', headers=headers)
params = {
    'cacheOnly':'false'
}
response2 = requests.get(URL + '/3304/0/5700', headers=headers, params=params)
print(response2)
print(response2.text)