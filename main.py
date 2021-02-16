import numpy as np
import requests
import time
import hashlib
import json
import os

timestamp = 0
post_url_http = "http://api.zzzmh.cn/bz/getJson"
post_url_https = "https://api.zzzmh.cn/bz/getJson"
img_url = 'https://w.wallhaven.cc/full/{}/wallhaven-{}.jpg'
img_dir = './img'

class Img:
    t = ''
    x = ''
    i = ''
    y = ''
    def __init__(self, t, x, i, y):
        self.t = t
        self.x = x
        self.i = i
        self.y = y


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100103 Firefox/84.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Host': 'api.zzzmh.cn',
        "Referer": 'https://bz.zzzmh.cn/',
        'Origin': 'https://bz.zzzmh.cn',
        'Sign': '74eef0d7802462e248a36941b0d8076f',
        'Timestamp':'1608294616853',
        'Access':'52aa6ce63efce33f61bcdd236eba1a6cbfe455d7173500223aae1e2c899a065b',
        'Location':'bz.zzzmh.cn',
        'Connection': 'close',
    }
def make_dir():
    if os.path.exists(img_dir) == False:
        os.mkdir(img_dir)

def request_download(img_id):
    import requests
    r = requests.get(img_url.format(img_id[:2], img_id))
    img = open(file=img_dir+'/'+img_id+'.jpg', mode='wb')
    img.write(r.content)

def get_timestamp():
    now_time = time.time()
    now_time = int(now_time*1000)
    return now_time

def sha256(code):
    s = hashlib.sha256()  # Get the hash algorithm.
    s.update(code.encode("utf-8"))  # Hash the data.
    return s.hexdigest()  # Get he hash value.

def get_access():
    contentType = 'application/json'
    location = 'bz.zzzmh.cn'
    sign = '74eef0d7802462e248a36941b0d8076f'
    res = sha256(contentType + location + sign + str(timestamp))
    return res

def get_img_id():
    img_list = []
    post_data = {
        "target": "index",
        "pageNum": 1,
    }
    post_data = json.dumps(post_data)
    timestamp = get_timestamp()
    access = get_access()
    headers['Timestamp'] = str(timestamp)
    headers['Access'] = get_access()
    proxies = {
        "http": '127.0.0.1:9090',
        'https': '127.0.0.1:9090',
    }
    session = requests.session()
    response = requests.post(post_url_http, headers=headers, data=post_data, proxies=proxies, verify=False)
    #response = requests.post(post_url_https, headers=headers, data=post_data)
    print(response.text)
    response_text = response.text
    response_text = json.loads(response_text)
    all_img = response_text['result']['records']
    for k in range(len(all_img)):
        t = all_img[k]['t']
        x = all_img[k]['x']
        i = all_img[k]['i']
        y = all_img[k]['y']
        img_list.append(Img(t, x, i, y))
    print(len(img_list))
    print(response_text)
    # print(response.status_code)
    # print(response.text)
    return img_list
    #print(response.content)

if __name__ == '__main__':
    img_list = get_img_id()
    # make_dir()
    # for l in range(len(img_list)):
    #     img_id = img_list[l].i
    #     request_download(img_id)



