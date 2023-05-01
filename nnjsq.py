"""
nn加速器 v1.0

任务：未知

账号&密码填到变量 nnjsq 中, 多账号#隔开
export nnjsq=""

cron: 5 0 * * *
const $ = new Env("nn加速器");
"""

import hashlib
import json
from time import sleep
import requests
import os,sys
import notify

#检测账户变量
nnjsq = os.environ.get("nnjsq") 
if not nnjsq or "&" not in nnjsq:
    sys.exit("⚠️未发现有效账号,退出程序!") 
    
#分割账户
accounts = {}
for i, account in enumerate(nnjsq.split('#'), 1):
    phone_key = f"nn_user{i}"
    pwd_key = f"nn_pwd{i}"
    phone = os.environ.get(phone_key)
    password = os.environ.get(pwd_key)
    if not phone or not password:
        sys.exit(f"⚠️未发现有效账号{i},退出程序!")
    accounts[f"account{i}"] = {"phone": account.split('&')[0], "passwd": account.split('&')[1]}

# 登录
def login(phone, passwd):
    messages = ''
    print(phone)
    messages = messages + '\n' + phone
    # notify.go_cqhttp("nn加速器", phone)
    _url = 'https://opapi.nnraytheon.com/u-mobile/pwdLogin'
    _data = {
        "countryCode": 86,
        "telNum": phone,
        "pwdEncry": hashlib.md5(bytes(passwd, encoding='utf-8')).hexdigest()
    }
    headers = {
        "Host": "opapi.nnraytheon.com",
        "token": "",
        "appid": "nnMobileIm_6z0g3ut7",
        "timestamp": "1675096362942",
        "signtype": "1",
        "sign": "",
        "version": "108",
        "reqchannel": "2",
        "deviceid": "d4uud558697ada1ec",
        "appname": "leigod_accelerator",
        "osversion": "12",
        "longitude": "0.0",
        "latitude": "0.0",
        "platform": "2",
        "registercanal": "common",
        "busitype": "nn_aksjfdasoifnkls",
        "content-type": "application/json; charset=UTF-8",
        "content-length": "87",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.3"
    }
    login_status = requests.post(url=_url, data=json.dumps(_data), headers=headers).json()
    print(login_status['retMsg'])
    messages = messages + '\n' + login_status['retMsg']
    # notify.go_cqhttp("nn加速器", login_status['retMsg'])
    if login_status['retMsg'] != '该用户不存在':
        headers['token'] = login_status['retData']['token']
        _data = {
            "taskIds": [
                12,
                13,
                16,
                17,
                18,
                24,
                25,
                27,
                28,
                29,
                30
            ],
            "userId": login_status['retData']['userId']
        }
        get_num = \
            requests.post(url='https://opapi.nnraytheon.com/nn-assist/taskPoints/findUserTaskInfo',
                          data=json.dumps(_data),
                          headers=headers).json()['retData']
        for i in get_num:
            for e in range(10):
                _data = {
                    "point": 1,
                    "taskId": i['taskId'],
                    "taskName": "",
                    "userId": login_status['retData']['userId']
                }
                result = requests.post(url='https://opapi.nnraytheon.com/nn-assist/taskPoints/pointCallBack',
                                       data=json.dumps(_data), headers=headers).json()
                print(result['retMsg'])
                messages = messages + '\n' + result['retMsg']
                # notify.go_cqhttp("nn加速器", result['retMsg'])
                if result['retMsg'] == '当天完成任务已上限':
                    break
                else:
                    sleep(0)
                    pass
    notify.send("【nn加速器】", messages)
    
for account in accounts:
    print(f"Logging in to {account}...")
    login(accounts[account]["phone"], accounts[account]["passwd"])