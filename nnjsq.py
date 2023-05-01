# 变量nn_user1，nn_pwd1，nn_user2，nn_pwd2，依次类推，代码更改在71行下面
# 定时推荐  1 0 * * *     每天凌晨12点刷新任务，可自行设置定时

import hashlib
import json
from time import sleep
import requests
import os
import notify


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


# 这里是多账号设置地方，单个账号就把账号2注释掉，多个账号自行增加代码
accounts = {
    # 账号1
    "account1": {
        "phone": os.environ['nn_user1'],
        "passwd": os.environ['nn_pwd1']
    },
    # 账号2
    "account2": {
        "phone": os.environ['nn_user2'],
        "passwd": os.environ['nn_pwd1']
    },

    # 账号3
    #"account3": {
    #    "phone": os.environ['nn_user3'],
    #    "passwd": os.environ['nn_pwd3']
    #},

}

for account in accounts:
    print(f"Logging in to {account}...")
    login(accounts[account]["phone"], accounts[account]["passwd"])