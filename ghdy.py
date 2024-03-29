"""
歌画东阳 v1.0

抓包域名: fijdzpur.act.tmuact.com 或者 wallet.act.tmuact.com
变量 account_id的值#session_id的值, 多账户&  
export bd_ghdy=""

cron: 2 10 * * *
const $ = new Env("歌画东阳");
"""

import hashlib
import random
import string
import time
import requests
from os import environ, path
from functools import partial

def get_environ(key, default="", output=True):
    def no_read():
        if output:
            print(f"未填写环境变量 {key} 请添加")
        return default
    return environ.get(key) if environ.get(key) else no_read()

def generate_random_string(length):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

class Ghdy:
    def __init__(self, ck):
        self.session = ck[1]
        self.account = ck[0]
        self.id_list = []
        self.msg = ''

    def login(self):
        try:
            a8 = generate_random_string(8)
            b4 = generate_random_string(4)
            c4 = generate_random_string(4)
            d4 = generate_random_string(4)
            e12 = generate_random_string(12)
            request = f'{a8}-{b4}-{c4}-{d4}-{e12}'
            current_timestamp = int(time.time() * 1000)
            sha = f'/api/user_mumber/account_detail&&{self.session}&&{request}&&{current_timestamp}&&FR*r!isE5W&&49'
            sha256 = hashlib.sha256()
            sha256.update(sha.encode('utf-8'))
            signature = sha256.hexdigest()
            time.sleep(0.5)
            url = "https://vapp.tmuyun.com/api/user_mumber/account_detail"
            headers = {'X-SESSION-ID': self.session, 'X-REQUEST-ID': f'{request}', 'X-TIMESTAMP': f'{current_timestamp}',
                       'X-SIGNATURE': f'{signature}', 'X-TENANT-ID': '49', 'User-Agent': '5.0.7.0.0;00000000-699e-0680-0000-000055f72c53;Xiaomi Redmi Note 8 Pro;Android;11;Release', 'X-ACCOUNT-ID': self.account,
                       'Cache-Control': 'no-cache', 'Host': 'vapp.tmuyun.com', 'Connection': 'Keep-Alive',
                       'Accept-Encoding': 'gzip'}
            r = requests.get(url, headers=headers)
            if r.json()['message'] == 'success':
                xx = f'🚀登录成功：{r.json()["data"]["rst"]["nick_name"]}'
                self.msg += xx + '\n'
                print(xx)
            elif '无效' in r.json()['message']:
                xx = f'⛔️登录失败：{r.json()["message"]}'
                self.msg += xx + '\n'
                print(xx)
        except Exception as e:
            print(e)

    def get_id(self):
        try:
            a8 = generate_random_string(8)
            b4 = generate_random_string(4)
            c4 = generate_random_string(4)
            d4 = generate_random_string(4)
            e12 = generate_random_string(12)
            request = f'{a8}-{b4}-{c4}-{d4}-{e12}'
            current_timestamp = int(time.time() * 1000)
            sha = f'/api/article/channel_list&&{self.session}&&{request}&&{current_timestamp}&&FR*r!isE5W&&49'
            sha256 = hashlib.sha256()
            sha256.update(sha.encode('utf-8'))
            signature = sha256.hexdigest()
            headers = {'X-SESSION-ID': self.session, 'X-REQUEST-ID': f'{request}', 'X-TIMESTAMP': f'{current_timestamp}',
                       'X-SIGNATURE': f'{signature}', 'X-TENANT-ID': '49', 'User-Agent': '5.0.7.0.0;00000000-699e-0680-0000-000055f72c53;Xiaomi Redmi Note 8 Pro;Android;11;Release', 'X-ACCOUNT-ID': self.account,
                       'Cache-Control': 'no-cache', 'Host': 'vapp.tmuyun.com', 'Connection': 'Keep-Alive',
                       'Accept-Encoding': 'gzip'}
            params = {'channel_id': '6254f12dfe3fc10794f7b25c', 'isDiFangHao': 'false', 'is_new': 'true',
                      'list_count': '0', 'size': '20'}
            r = requests.get('https://vapp.tmuyun.com/api/article/channel_list', params=params, headers=headers)
            if r.json()['message'] == 'success':
                r_list = r.json()['data']['article_list']
                a = 5
                for i in r_list:
                    a += 1
                    self.id_list.append(i['id'])
                random.shuffle(self.id_list)
                if self.id_list:
                    xx = "✅文章加载成功"
                    self.msg += xx + '\n'
                    print(xx)
            elif '不存在' in r.json()['message']:
                xx = f'⛔️文章加载失败：{r.json()["message"]}'
                print(xx)
                self.msg += xx + '\n'
            else:
                xx = f'⛔️请求异常：{r.json()["message"]}'
                print(xx)
                self.msg += xx + '\n'
        except Exception as e:
            print(e)

    def look(self):
        try:
            for params_id in self.id_list[:6]:
                a8 = generate_random_string(8)
                b4 = generate_random_string(4)
                c4 = generate_random_string(4)
                d4 = generate_random_string(4)
                e12 = generate_random_string(12)
                request = f'{a8}-{b4}-{c4}-{d4}-{e12}'
                current_timestamp = int(time.time() * 1000)
                sha = f'/api/article/detail&&{self.session}&&{request}&&{current_timestamp}&&FR*r!isE5W&&49'
                sha256 = hashlib.sha256()
                sha256.update(sha.encode('utf-8'))
                signature = sha256.hexdigest()
                url = 'https://vapp.tmuyun.com/api/article/detail'
                headers = {'X-SESSION-ID': self.session, 'X-REQUEST-ID': f'{request}', 'X-TIMESTAMP': f'{current_timestamp}',
                           'X-SIGNATURE': f'{signature}', 'X-TENANT-ID': '49', 'User-Agent': '5.0.7.0.0;00000000-699e-0680-0000-000055f72c53;Xiaomi Redmi Note 8 Pro;Android;11;Release', 'X-ACCOUNT-ID': self.session,
                           'Cache-Control': 'no-cache', 'Host': 'vapp.tmuyun.com', 'Connection': 'Keep-Alive',
                           'Accept-Encoding': 'gzip'}
                params = {'id': params_id}
                r = requests.get(url, params=params, headers=headers)
                if r.json()['message'] == 'success':
                    xx = f'✅浏览《{r.json()["data"]["article"]["list_title"]}》成功✅'
                    print(xx)
                    self.msg += xx + '\n'
                    time.sleep(3)
                elif '不存在' in r.json()['message']:
                    xx = f'⛔️浏览失败：{r.json()["message"]}'
                    print(xx)
                    self.msg += xx + '\n'
                else:
                    xx = f'⛔️浏览异常：{r.json()["message"]}'
                    print(xx)
                    self.msg += xx + '\n'
            xx = '✅浏览完成，准备抽红包吧！'
            print(xx)
            self.msg += xx + '\n'
        except Exception as e:
            print(e)

    def chou(self):
        try:
            url = 'https://fijdzpur.act.tmuact.com/activity/api.php'
            headers = {'Host': 'fijdzpur.act.tmuact.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
                       'Cache-Control': 'no-cache', 'Accept': 'application/json, text/plain, */*',
                       'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_dongyang;xsb_dongyang;5.0.7.0.0;native_app',
                       'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://fijdzpur.act.tmuact.com',
                       'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                       'Referer': 'https://fijdzpur.act.tmuact.com/money/index/index.html',
                       'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
            data = {'m': 'front', 'subm': 'money', 'action': 'open', 'account_id': self.account, 'session_id': self.session,
                    'token': '', 'q': 'YunSLfAkU'}
            r = requests.post(url, headers=headers, data=data)
            if r.json()['status']:
                xx = f'✅抽奖成功：{r.json()["data"]["name"]}'
                print(xx)
                self.msg += xx + '\n'
                time.sleep(3)
                self.tx()
            elif not r.json()['status']:
                if '已完' in r.json()['msg']:
                    xx = f'❌{r.json()["msg"]}'
                    print(xx)
                    self.msg += xx + '\n'
                    time.sleep(3)
                    self.tx()
                elif '阅读' in r.json()['msg']:
                    xx = f'❌{r.json()["msg"]}，即将开始阅读。'
                    print(xx)
                    self.msg += xx + '\n'
                    self.get_id()
                    self.look()
                    self.chou()
                else:
                    xx = f'❌{r.json()["msg"]}'
                    print(xx)
                    self.msg += xx + '\n'
        except Exception as e:
            print(e)

    def tx(self):
        url = "https://wallet.act.tmuact.com/activity/api.php"
        data = {'m': 'front', 'subm': 'money_wallet', 'action': 'commonchange', 'account_id': self.account,
                'session_id': self.session, 'app': 'XSB_DONGYANG'}
        h = {'Host': 'fijdzpur.act.tmuact.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
             'Cache-Control': 'no-cache', 'Accept': 'application/json, text/plain, */*', 'X-Requested-With': 'XMLHttpRequest',
             'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_dongyang;xsb_dongyang;5.0.7.0.0;native_app',
             'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://fijdzpur.act.tmuact.com',
             'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
             'Referer': 'https://fijdzpur.act.tmuact.com/money/index/index.html',
             'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
        r = requests.post(url, headers=h, data=data)
        if r.json()['status']:
            xx = f'✅提现！{r.json()["msg"]}！'
            print(xx)
        else:
            xx = f'❌{r.json()["msg"]}'
            print(xx)

if __name__ == '__main__':
    print = partial(print, flush=True)
    token = get_environ("bd_ghdy")
    cks = token.split("&")
    print("🔔检测到{}个ck记录\n🔔开始歌画东阳任务".format(len(cks)))
    for ck_all in cks:
        ck = ck_all.split("#")
        run = Ghdy(ck)
        print()
        run.login()
        run.chou()
