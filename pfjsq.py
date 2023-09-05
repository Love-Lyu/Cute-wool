"""
泡芙加速器 v1.0

任务：签到 刷视频

cookie填到变量 pfjsq 中, 多账户&间隔
export pfjsq=""

cron: 16 9,14 * * *
const $ = new Env("泡芙加速器");
"""

import requests
import time
import os
import sys

class PuffAccelerator:
    def __init__(self, pfjsq):
        # 检测账户变量
        self.pfjsq = pfjsq

        # 授权密钥
        self.headers = {
            "Host": "api-admin-js.paofujiasu.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2007J1SC Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5075 MMWEBSDK/20230405 MMWEBID/8380 MicroMessenger/8.0.35.2360(0x2800235B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
            "content-type": "application/json",
            "token": self.pfjsq,
            "tokenType": "applet",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wx5bf04507567e9d72/14/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br"
        }

    # 查询用户信息
    def get_pfjsq_acceleration_time(self):
        url = 'https://api-admin-js.paofujiasu.com/api/v1/user/gw/userinfo'
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data['info'] == '查询成功':
                accelerate_time = data['data']['remain_accelerate_time']
                result = f'✅加速时间 | {accelerate_time}'
                return result
            else:
                return '⚠️cookie过期'
        else:
            return '⚠️cookie过期'
    
    # 查询用户信息
    def get_pfjsq_user(self):
        url = 'https://api-admin-js.paofujiasu.com/api/v1/user/gw/userinfo'
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data['info'] == '查询成功':
                user_account = data['data']['user_account']
                return user_account
            else:
                return '⚠️cookie过期'
        else:
            return '⚠️cookie过期'

    # 查询用户金币信息
    def get_pfjsq_coins(self):
        url = 'https://api-admin-js.paofujiasu.com/client/api/v1/virtual_currency/species_quantity'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data['info'] == '请求成功':
                user_coins = data['data']['remaining_quantity']
                result = f'✅当前金币 | {user_coins}'
                return result
            else:
                return '⚠️cookie过期'
        else:
            return '⚠️cookie过期'

    # 用户签到
    def get_pfjsq_check(self):
        url = 'https://api-admin-js.paofujiasu.com/client/api/v1/virtual_currency/sign_in_for_species'
        data = {'res_type': 1}
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            data = response.json()
            if data['info'] == '请求成功':
                return '✅签到成功'
            else:
                return '⚠️cookie过期'
        elif response.status_code == 400:
            data = response.json()
            if data['info'] == '每天最多签到1次哦~':
                return '✅今日已签到'
            else:
                return '⚠️cookie过期'
        else:
            return '⚠️cookie过期'

    # 刷视频
    def get_pfjsq_video(self):
        url = 'https://api-admin-js.paofujiasu.com/client/api/v1/virtual_currency/look_ad_for_species'
        data = {'res_type': 1}
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            data = response.json()
            if data['info'] == '请求成功':
                return '✅刷视频成功'
            else:
                return '⚠️cookie过期'
        elif response.status_code == 400:
            data = response.json()
            if data['info'] == '每天最多3次看广告激励哦~':
                return '✅刷视频已上限'
            else:
                return '⚠️cookie过期'
        else:
            return '⚠️cookie过期'

    # 主程序
    def run(self):
        # 任务列表
        tasks = [
            ("每日签到", self.get_pfjsq_check),
            ("第一次刷视频", self.get_pfjsq_video),
            ("第二次刷视频", self.get_pfjsq_video),
            ("第三次刷视频", self.get_pfjsq_video),
            ("查询时间", self.get_pfjsq_acceleration_time),
            ("查询金币", self.get_pfjsq_coins)
        ]
        # 执行任务
        for task_name, task_function in tasks:
            if self.get_pfjsq_user() == '⚠️cookie过期':
                print(self.get_pfjsq_user())
                break
            print(f'🔁{self.get_pfjsq_user()} | 正在执行任务 | {task_name}')
            result = task_function()
            if result == '⚠️cookie过期':
                print(result)
                break
            print(result)
            time.sleep(5)
        print('*****************************************')

if __name__ == '__main__':
    print('🔔泡芙加速器 | 开始')
    #检测账户变量
    pfjsq = os.environ.get("pfjsq") 
    if not pfjsq:
        sys.exit("⚠️未发现有效账号,退出程序!") 
    #分割账户
    if "&" not in pfjsq:
        accounts = [pfjsq]
    else:
        accounts = pfjsq.split("&")
    # 遍历账户列表 | 为每个账户创建一个类实例并执行任务
    for account in accounts:
        paofujiasu_client = PuffAccelerator(account)
        paofujiasu_client.run()