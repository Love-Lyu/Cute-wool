import requests, json

# 小米签到
# 配置cookie 小米社区app 到签到页面抓包https://api.vip.miui.com/mtop/planet/vip/user/checkin 的cookie即可
cookie = [
    'cUserId*********',
    'cUserId=********'
]

for i in range(len(cookie)):
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
        'Cookie': f'{cookie[i]}'
    }
    html = requests.get(url=url, headers=headers)
    result = json.loads(html.text)
    print('*************'+'\n'+f'开始第{i + 1}个账号签到'+'\n'+'签到结果：')
    print(result['message'])
