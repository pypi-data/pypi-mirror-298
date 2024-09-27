import re
import binascii
import base64
import urllib.parse
from .requests_tools import get
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from base64 import b64decode


def base64_de(data: str):
    return base64.b64decode(data).decode('utf-8').encode().decode('unicode_escape')


def escape_de(data: str):
    return urllib.parse.unquote(data.replace('%u', '\\u').encode().decode('unicode-escape'))


def unicode_de(data: str):
    return data.encode('utf-8').decode('unicode_escape')


def url_de(data: str):
    return urllib.parse.unquote(data).encode().decode('utf-8')


def aes_cbc_de(data, key: str, iv: str) -> bytes:
    def add_16(par):  # 补位到16倍数位
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    # 对key进行补位 。key，iv 进行编码，把data编码成字节
    key = add_16(key.encode('utf-8'))
    iv = iv.encode('utf-8')
    if data is str:  # 为普通字节
        data = base64.decodebytes(data.encode('utf-8'))
    elif data is bytes:
        data = data
    else:
        data = binascii.a2b_hex(data.encode('utf-8'))  # 为十六位数

    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = aes.decrypt(data)
    # decrypted_data = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', "", decrypted_data.decode('utf-8'))

    # 如果数据是PKCS7填充的，则去除填充
    try:
        unpadded_data = unpad(decrypted_data, AES.block_size)
    except ValueError:
        # 如果解密失败（例如，数据没有正确填充），则返回原始解密数据
        unpadded_data = decrypted_data
    return unpadded_data


def yinhua_de(url, key='57A891D97E332A9D'):
    """
    樱花动漫解密
    :param url: 跳转url
    :param key: 逆向获取key
    :param url:樱花动漫解析网址
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    resp = get(url, headers=headers).text
    iv = re.search('<script>var.?bt_token.?=.?"(?P<iv>.*?)";.?</script>', resp)['iv']
    data = re.search('getVideoInfo\("(?P<data>.*?)"\)', resp)['data']
    down_url = aes_cbc_de(data, key, iv)
    return down_url
