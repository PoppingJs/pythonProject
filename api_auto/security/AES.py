#对称加密
from Crypto.Cipher import AES
import base64
class crypt:
    def __init__(self,key,iv):
        self.key = key.encode('utf-8')  #encode()将字符串转换为二进制数据
        self.iv=iv.encode('utf-8')
        self.length = AES.block_size  #AES加密解密将明文分成固定的分组，每个分组大小为16字节
        #创建 AES 对象 --CBC模式
        self.aes=AES.new(self.key,AES.MODE_CBC,self.iv)
    # 加密函数
    def encrypt(self, text):
        #AES算法接收的明文必须是16字节或者16字节的倍数的字节型数据，如果不够16字节需要进行补全
        # 将明文数据补全为 16 的倍数
        count=len(text.encode('utf-8'))   #二进制数据长度
        add = self.length - (count % self.length) #补全组需要加的个数
        pad = text + (chr(add)*add)       #字符串
        #进行加密
        res=self.aes.encrypt(pad.encode('utf-8'))   #加密前进行b64encode，后面需要b64decode解码
        # 使用 Base64 对加密后的数据进行编码             # 由于加密前的明文一般正常，可直接encode转换成二进制数
        msg = base64.b64encode(res).decode('utf-8') # base64.b64encode()返回的是base64二进制数据,传输可靠性强
        return msg                                  # 通过decode将二进制数据转换为字符串，或者加上str()

    # 解密函数
    def decrypt(self,text):
        # 使用 Base64 对密文由字符串解码成原始二进制数据
        de_text = base64.b64decode(text) #将经过b64encode()编码的字符串须经b64decode解码成原始二进制数据
        #CBC模式下解密需要重新创建一个aes对象
        self.aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 进行解密
        res = self.aes.decrypt(de_text).decode('utf-8')
        # 去除填充的字符
        unpad = res[:-ord(res[len(res) - 1:])]
        return unpad

#测试
if __name__ == '__main__':

    key = '0123456789abcdef'  # 密钥必须是 16、24 或 32 个字符，一般是给定的
    iv = '0123456789abcdef'  # 向量必须是 16 个字符
    text = 'my_password'
    print('=====加密=====')
    C=crypt(key, iv)
    encrypt_res=C.encrypt(text)
    print(f'加密后的密文：{encrypt_res}')
    decrypt_res=C.decrypt(encrypt_res)
    print(f'解密后的密文：{decrypt_res}')
