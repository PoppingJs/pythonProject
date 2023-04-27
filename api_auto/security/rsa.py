#非对称加密
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
# 秘钥的位数，可以自定义指定，一般长度  1024,2048
key = RSA.generate(1024)

#生成私钥
private_key = key.export_key()
with open('private.pem','wb') as f:
    f.write(private_key)

#生成公钥
public_key = key.publickey().export_key()
with open('public.pem', 'wb') as f:
    f.write(public_key)

# 读取公钥私钥，赋值变量存储 --注：调用要经过RSA.importKey(pub_key)转换
with open('public.pem','r') as f:
    pub_key=f.read()

with open('private.pem','r') as f:
    pri_key=f.read()


#封装自己生成公钥密钥
class rsa:
    def __init__(self,key_length=1024):
        self.private_key=RSA.generate(key_length)    #实际应用公钥密钥是固定的，开发分配公钥给测试
        self.public_key=self.private_key.publickey() #测试拿到公钥后public_pem，用pub_key变量存储调用


    def encrypt(self,text):
        cipher = PKCS1_v1_5.new(self.public_key)   #cipher作用：将明文转换为密文，并将密文转换为明文
        res = cipher.encrypt(text.encode('utf-8'))
        msg=base64.b64encode(res).decode('utf-8')
        return msg

    def decrypt(self,text):
        de_text = base64.b64decode(text)
        cipher = PKCS1_v1_5.new(self.private_key)
        res = cipher.decrypt(de_text,None).decode('utf-8')
        return res

#他人（开发）生成公钥密钥，拿取公钥测试,私钥解密
class rsa2:
    def encrypt(self,text,public_key):
        cipher = PKCS1_v1_5.new(public_key)
        res = cipher.encrypt(text.encode('utf-8'))
        msg=base64.b64encode(res).decode('utf-8')
        return msg

    def decrypt(self,text,private_key):
        de_text = base64.b64decode(text)
        cipher = PKCS1_v1_5.new(private_key)
        res = cipher.decrypt(de_text,None).decode('utf-8')
        return res
#测试
if __name__ == '__main__':
    text='不是没想过'
    R=rsa()
    encrypt_res = R.encrypt(text)
    print(f'加密后的密文：{encrypt_res}')
    decrypt_res=R.decrypt(encrypt_res)
    print(f'解密后的密文：{decrypt_res}')

