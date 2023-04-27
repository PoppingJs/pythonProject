import requests
from Crypto.PublicKey import RSA
from api_auto.security.rsa import rsa2

url='http://mall.lemonban.com:8107/login'  #不是加密接口

with open('public.pem','r') as f:
    pub_key=f.read()
public_key = RSA.importKey(pub_key)     #注意要用RSA.importKey(存储的公钥)，不是直接调用
S= rsa2()
crypt_1=S.encrypt('15755808681',public_key)
crypt_2=S.encrypt('123456',public_key)
data={
	"principal": crypt_1,
	"credentials": crypt_2,
	"appType": 3,
	"loginType": 0
    }
print(data)
headers = {'Content-Type':'application/json',
                'Accept': 'application/json'}
res=requests.request(method='POST',
					 headers=headers,
					 json=data,
					 url=url)
print(res.json())