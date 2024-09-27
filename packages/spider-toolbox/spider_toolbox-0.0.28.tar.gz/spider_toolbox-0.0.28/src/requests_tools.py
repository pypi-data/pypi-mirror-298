import time
import requests
from functools import wraps

default_ua = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 '
                  'Safari/537.36'}


def retry_on_exception(retries=5, delay=1, backoff=2,
                       exceptions=(requests.exceptions.RequestException,
                                   requests.exceptions.ConnectionError,
                                   requests.exceptions.ConnectTimeout
                                   )):
    def decorator_retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_retries = 0
            while current_retries < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if current_retries >= retries - 1:
                        raise requests.exceptions.RetryError
                    # 计算下一次重试前的等待时间
                    wait_time = delay * (backoff ** current_retries)
                    time.sleep(wait_time)
                    current_retries += 1

        return wrapper

    return decorator_retry


def get(url: str,
        headers=None,
        params=None,
        cookies=None,
        timeout: int = None,
        proxies=False):
    """
    :param cookies:
    :param url: 地址
    :param headers: 请求头
    :param params: params
    :param timeout: 超时时间
    :param proxies:
    """
    if headers is None:
        headers = default_ua

    resp = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=timeout, proxies=proxies)
    return resp


def post(url: str,
         headers=None,
         params=None,
         cookies=None,
         data=None,
         timeout: int = None):
    """
    :param data:
    :param cookies:
    :param url: 地址
    :param headers: 请求头
    :param params: params
    :param timeout: 超时时间
    """
    if headers is None:
        headers = default_ua
    resp = requests.post(url, headers=headers, cookies=cookies, params=params, timeout=timeout, data=data)
    return resp


def session():
    return requests.Session()


# def byte_downloader(url: str,
#                     workdir: str,
#                     file_name: str,
#                     file_type: str,
#                     headers=None,
#                     timeout: int = None,
#                     retry_num: int = 10,
#                     retry_sleep: int = 1) -> bool:
#     """
#     :param url:
#     :param workdir:
#     :param file_name: 文件名
#     :param file_type: 文件后缀 无需.
#     :param headers:
#     :param timeout: 超时时间
#     :param retry_num: 重试次数
#     :param retry_sleep: 重试间隔
#     :return: bool
#     # """
#     file_type = file_type.replace('.', '')
#     workdir = os.path.join(workdir, file_name) + '.' + file_type
#     resp = get(url,
#                headers=headers,
#                timeout=timeout, )
#     if resp:
#         with open(workdir, 'wb') as f:
#             f.write(resp.content)
#         return True
#     else:
#         return False


if __name__ == '__main__':
    # http = Retry_http().get(url='https://www.google.com/')
    pass
