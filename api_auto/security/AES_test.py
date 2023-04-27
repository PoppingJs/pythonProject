import requests
from api_auto.security.AES import crypt
url='http://mall.lemonban.com:8107/login'  #不是加密接口
key = '0123456789higklm'   #同加密接口同一个密钥
iv = '0123456789abcdef'
C= crypt(key,iv)
crypt_1=C.encrypt('15755808681')
crypt_2=C.encrypt('123456')
data={
	"principal": crypt_1,
	"credentials": crypt_2,
	"appType": 3,
	"loginType": 0
    }
# print(data)  #{'principal': 'f2A9ftCG//vrpZMIJ8JvcQ==', 'credentials': '8xCzUKEmiSqb84U1MUReAw==', 'appType': 3, 'loginType': 0}
headers = {'Content-Type':'application/json',
                'Accept': 'application/json'}
res=requests.request(method='POST',
					 headers=headers,
					 json=data,
					 url=url)
print(res.json())
#运行报错是因为接口没有设置读取解码AES加密后的账号密码



