"""
小米社区 v1.0

任务：日常任务

export xiaomi="账户&密码" 多账户 # 分割

cron: 5 9,15,20 * * *
const $ = new Env("小米社区");
"""

import os
import sys
import requests
import json
import hashlib
import base64
import binascii
import time

class XiaomiSign:
    # 初始化
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.userId = None  
        self.cookie = None  
        self.html_user = None
        
    # 获取cookie
    def get_cookie(self, account, password):
        md5 = hashlib.md5()
        md5.update(password.encode())
        Hash = md5.hexdigest()
        url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2007J17C Build/SKQ1.211006.001) APP/xiaomi.vipaccount APPV/220301 MK/UmVkbWkgTm90ZSA5IFBybw== PassportSDK/3.7.8 passport-ui/3.7.8",
            "Cookie": "deviceId=X0jMu7b0w-jcne-S; pass_o=2d25bb648d023d7f; sdkVersion=accountsdk-2020.01.09",
            "Host": "account.xiaomi.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        data = {
            "cc": "+86",
            "qs": "%3F_json%3Dtrue%26sid%3Dmiui_vip%26_locale%3Dzh_CN",
            "callback": "https://api.vip.miui.com/sts",
            "_json": "true",
            "user": account,
            "hash": Hash.upper(),
            "sid": "miui_vip",
            "_sign": "ZJxpm3Q5cu0qDOMkKdWYRPeCwps%3D",
            "_locale": "zh_CN"
        }
        Auth = requests.post(url=url, headers=headers, data=data).text.replace("&&&START&&&", "")
        Auth = json.loads(Auth)
        ssecurity = Auth["ssecurity"]
        nonce = Auth["nonce"]
        sha1 = hashlib.sha1()
        Str = "nonce=" + str(nonce) + "&" + ssecurity
        sha1.update(Str.encode("utf-8"))
        clientSign = base64.encodebytes(binascii.a2b_hex(sha1.hexdigest().encode("utf-8"))).decode(encoding="utf-8").strip()
        nurl = Auth["location"] + "&_userIdNeedEncrypt=true&clientSign=" + clientSign

        sts = requests.get(url=nurl)
        cookies = requests.utils.dict_from_cookiejar(sts.cookies)
        cookie_str = '; '.join([f'{key}={value}' for key, value in cookies.items()])
        return cookie_str

    # 签到任务
    def sign_in(self):
        max_retries = 10
        retries = 0

        while retries < max_retries:
            cookie = self.get_cookie(self.account, self.password)
            self.cookie = cookie
            url = 'https://api.vip.miui.com/mtop/planet/vip/user/checkin'
            headers = {
                'Host': 'api.vip.miui.com',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; zh-cn; M2007J1SC Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/15.7.22 app/vipaccount',
                'Accept': '*/*',
                'Origin': 'https://web.vip.miui.com',
                'X-Requested-With': 'com.xiaomi.vipaccount',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.220804',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': f'{cookie}'
            }
            user_url = 'https://api.vip.miui.com/api/community/user/home/page'
        
            html = requests.get(url=url, headers=headers)
            html_user = requests.get(url=user_url, headers=headers)
            self.html_user = html_user
            
            result = json.loads(html.text)
            try:
                result_user = json.loads(html_user.text)
                userId = result_user['entity']['userId']
                self.userId = userId
                return '⚠️签到失败'
                #print('✅' + result['message'])
                #print('✅userId | ' + userId + ' 用户名 | ' + result_user['entity']['userName'] + ' 段位 | ' + result_user['entity']['userGrowLevelInfo']['showLevel'])
                break
            except KeyError:
                retries += 1
                time.sleep(3) 

    # 点赞任务
    def like_post(self):
        for _ in range(2):
            like_url = 'https://api.vip.miui.com/mtop/planet/vip/content/announceThumbUp'
            headers = {
                'Host': 'api.vip.miui.com',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; zh-cn; M2007J1SC Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/15.7.22 app/vipaccount',
                'Accept': '*/*',
                'Origin': 'https://web.vip.miui.com',
                'X-Requested-With': 'com.xiaomi.vipaccount',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.220804',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': f'{self.cookie}'
            }
            data = {
                'postId': '36625780',
                'sign': '36625780',
                'timestamp': int(round(time.time() * 1000))
            }
            response = requests.get(url=like_url, headers=headers, params=data)
            result = json.loads(response.text)
            if result['status'] == 200:
                return '✅点赞帖子成功'
            else:
                return '⚠️点赞帖子失败'
    
    # 加入圈子
    def join_group(self):
        unfollow_url = 'https://api.vip.miui.com/api/community/board/unfollow?boardId=558495'
        headers = {
            'Host': 'api.vip.miui.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; zh-cn; M2007J1SC Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/15.7.22 app/vipaccount',
            'Accept': '*/*',
            'Origin': 'https://web.vip.miui.com',
            'X-Requested-With': 'com.xiaomi.vipaccount',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.220804',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': f'{self.cookie}'
        }
        response_unfollow = requests.get(url=unfollow_url, headers=headers)
        result_unfollow = json.loads(self.html_user.text)
        if result_unfollow['status']==200:
            unfollow_message = '✅退出圈子成功'
        else:
            unfollow_message = '⚠️退出圈子失败'

        follow_url = 'https://api.vip.miui.com/api/community/board/follow?boardId=558495'
        response_follow = requests.get(url=follow_url, headers=headers)
        result_follow = json.loads(self.html_user.text)
        if result_follow['status']==200:
            follow_message = '✅加入圈子成功'
        else:
            follow_message = '⚠️加入圈子失败'
        # 返回
        return f'{unfollow_message}\n{follow_message}'
        
    # 浏览主页
    def browse_home(self):
        info_url = f'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction?userId={self.userId}&action=BROWSE_SPECIAL_PAGES_USER_HOME'
        headers = {
            'Host': 'api.vip.miui.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; zh-cn; M2007J1SC Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/15.7.22 app/vipaccount',
            'Accept': '*/*',
            'Origin': 'https://web.vip.miui.com',
            'X-Requested-With': 'com.xiaomi.vipaccount',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.220804',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': f'{self.cookie}'
        }
        response = requests.get(url=info_url, headers=headers)
        result = json.loads(response.text)
        if result['status'] == 200:
            return '✅浏览主页成功，获得积分： '+str(result['entity']['score'])
        else:
            return '⚠️今日已达上限'
        
    # 浏览专题
    def browse_special_pages(self):
        llzt_url = f'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction?userId={self.userId}&action=BROWSE_SPECIAL_PAGES_SPECIAL_PAGE'
        headers = {
            'Host': 'api.vip.miui.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; zh-cn; M2007J1SC Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/15.7.22 app/vipaccount',
            'Accept': '*/*',
            'Origin': 'https://web.vip.miui.com',
            'X-Requested-With': 'com.xiaomi.vipaccount',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.220804',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': f'{self.cookie}'
        }
        response = requests.get(url=llzt_url, headers=headers)
        result = json.loads(response.text)
        if result['status'] == 200:
            return '✅浏览主页成功，获得积分： '+str(result['entity']['score'])
        else:
            return '⚠️今日已达上限'
    
    # 浏览帖子
    def browse_posts(self):
        for _ in range(3):
            watch_url = f'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction?userId={self.userId}&action=BROWSE_POST_10S'
            headers = {
                'Host': 'api.vip.miui.com',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; zh-cn; M2007J1SC Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/15.7.22 app/vipaccount',
                'Accept': '*/*',
                'Origin': 'https://web.vip.miui.com',
                'X-Requested-With': 'com.xiaomi.vipaccount',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.220804',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': f'{self.cookie}'
            }
            response = requests.get(url=watch_url, headers=headers)
            result = json.loads(response.text)
            if result['status'] == 200:
                return '✅浏览主页成功，获得积分： '+str(result['entity']['score'])
            else:
                return '⚠️今日已达上限'
        
    def run(self):
        self.sign_in() 
        # 任务列表
        tasks = [
            ("签到任务", self.sign_in),
            ("点赞任务", self.like_post),
            ("加入圈子", self.join_group),
            ("浏览主页", self.browse_home),
            ("浏览专题", self.browse_special_pages),
            ("浏览帖子", self.browse_posts)
        ]
        # 执行任务
        for task_name, task_function in tasks:
            print(f'🔁{self.userId} | 正在执行任务 | {task_name}')
            result = task_function()
            print(result)
            time.sleep(5)
        print('*****************************************')

if __name__ == '__main__':
    print('🔔小米社区 | 开始')
    #检测账户变量
    xiaomi_accounts = os.environ.get("xiaomi")
    if not xiaomi_accounts or "&" not in xiaomi_accounts:
        sys.exit("⚠️未发现有效账号,退出程序!")
    #分割账户 
    accounts = [acc.split('&') for acc in xiaomi_accounts.split('#')]
    # 遍历账户列表 | 为每个账户创建一个类实例并执行任务
    for account, password in accounts:
        xiaomi_signer = XiaomiSign(account, password)
        xiaomi_signer.run()
