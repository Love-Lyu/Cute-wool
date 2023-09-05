"""
科技玩家 v1.0

任务：签到

账号&密码填到变量 kjwj 中, 多账号#隔开
export kjwj=""

cron: 16 8,10 * * *
const $ = new Env("科技玩家");
"""

import os
import sys
import requests
import json
import time

class KejiWanjiaSign:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def sign(self):
        url = 'https://www.kejiwanjia.net/wp-json/jwt-auth/v1/token'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',
            'origin': 'https://www.kejiwanjia.net',
            'referer': 'https://www.kejiwanjia.net/'
        }
        data = {
            'username': self.username,
            'password': self.password
        }
        html = requests.post(url=url, headers=headers, data=data)
        result = json.loads(html.text)
        name = result['name']
        token = result['token']
        check_url = 'https://www.kejiwanjia.net/wp-json/b2/v1/getUserMission'
        sign_url = 'https://www.kejiwanjia.net/wp-json/b2/v1/userMission'
        sign_headers = {
            'Host': 'www.kejiwanjia.net',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'authorization': 'Bearer ' + token,
            'cookie': 'b2_token=' + token + ';',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42'
        }
        html_1 = requests.post(url=check_url, headers=sign_headers)
        imfo_1 = json.loads(html_1.text)
        if imfo_1['mission']['credit'] == 0:
            print(f"🔁账号 {self.username} | {name}")
            print("⚠️还未签到 开始签到")
            html_2 = requests.post(url=sign_url, headers=sign_headers)
            imfo_2 = json.loads(html_2.text)
            print(f"✅签到成功 获得{imfo_2['mission']['credit']}积分")
        else:
            print(f"🔁帐号 {self.username} | {name}")
            print(f"✅今天已经签到 获得{imfo_1['mission']['credit']}积分")

    def run(self):
        # 任务列表
        tasks = [
            ("签到任务", self.sign)
        ]
        # 执行任务
        for task_name, task_function in tasks:
            print(f'🔁{self.username} | 正在执行任务 | {task_name}')
            result = task_function()
            time.sleep(5)
        print('*****************************************')

if __name__ == '__main__':
    print('🔔科技玩家 | 开始')
    #检测账户变量
    kjwj = os.environ.get("kjwj")
    if not kjwj or "&" not in kjwj:
        sys.exit("⚠️未发现有效账号,退出程序!")
    #分割账户 
    accounts = [acc.split('&') for acc in kjwj.split('#')]
    # 遍历账户列表 | 为每个账户创建一个类实例并执行任务
    for username, password in accounts:
        kejiwanjia_sign = KejiWanjiaSign(username, password)
        kejiwanjia_sign.run()