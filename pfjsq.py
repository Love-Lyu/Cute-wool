"""
泡芙加速器 v1.0

任务：签到 刷视频

cookie填到变量 pfjsq 中
export pfjsq=""

cron: 16 9,14 * * *
const $ = new Env("泡芙加速器");
"""

import requests
import time
import os
import sys

#检测账户变量
pfjsq = os.environ.get("pfjsq")
if not pfjsq:
    print("⚠️未发现有效cookie,退出程序!")
    sys.exit()

# 授权密钥
headers = {
    "Host": "api-admin-js.paofujiasu.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2007J1SC Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5075 MMWEBSDK/20230405 MMWEBID/8380 MicroMessenger/8.0.35.2360(0x2800235B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
    "content-type": "application/json",
    "token": pfjsq,
    "tokenType": "applet",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wx5bf04507567e9d72/14/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br"
}

# 查询用户信息
def get_pfjsq_user():
    url = 'https://api-admin-js.paofujiasu.com/api/v1/user/gw/userinfo'
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['info'] == '查询成功':
            # 用户账号
            user_account = data['data']['user_account']
            # 剩余加速时间
            accelerate_time = data['data']['remain_accelerate_time']
            # 构建返回
            result = f'{user_account} | {accelerate_time}'
            return result
        else:
            return 'cookie过期'
    else:
        return 'cookie过期'

# 查询用户金币信息
def get_pfjsq_coins():
    url = 'https://api-admin-js.paofujiasu.com/client/api/v1/virtual_currency/species_quantity'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['info'] == '请求成功':
            # 用户剩余金币
            user_coins = data['data']['remaining_quantity']
            # 构建返回
            result = f'当前金币 | {user_coins}'
            return result
        else:
            return 'cookie过期'
    else:
        return 'cookie过期'
    
# 用户签到
def get_pfjsq_check():
    url = 'https://api-admin-js.paofujiasu.com/client/api/v1/virtual_currency/sign_in_for_species'
    data = {'res_type': 1}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()
        if data['info'] == '请求成功':
            return '签到成功'
        else:
            return 'cookie过期'
    elif response.status_code == 400:
        data = response.json()
        if data['info'] == '每天最多签到1次哦~':
            return '今日已签到'
        else:
            return 'cookie过期'
    else:
        return 'cookie过期'

# 刷视频
def get_pfjsq_video():
    url = 'https://api-admin-js.paofujiasu.com/client/api/v1/virtual_currency/look_ad_for_species'
    data = {'res_type': 1}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()
        if data['info'] == '请求成功':
            return '刷视频成功'
        else:
            return 'cookie过期'
    elif response.status_code == 400:
        data = response.json()
        if data['info'] == '每天最多3次看广告激励哦~':
            return '刷视频已上限'
        else:
            return 'cookie过期'
    else:
        return 'cookie过期'
    
# 主程序
def main():
    print('🔔泡芙加速器 | 开始')
    # 签到
    check_result = get_pfjsq_check()
    if check_result == 'cookie过期':
        return check_result
    print(check_result)
    # 刷视频
    for k in range(3):
        video_result = get_pfjsq_video()
        if video_result == 'cookie过期':
            return video_result
        print(video_result)
        time.sleep(5)
    # 返回账号&剩余时间
    user_result = get_pfjsq_user()
    if user_result == 'cookie过期':
        return user_result
    print(get_pfjsq_user())
    # 返回当前金币
    coins_result = get_pfjsq_coins()
    if coins_result == 'cookie过期':
        return coins_result
    print(get_pfjsq_coins())

main()