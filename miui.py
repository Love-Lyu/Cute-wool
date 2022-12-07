import requests, json

# 小米签到
# 配置cookie 小米社区app 到签到页面抓包https://api.vip.miui.com/mtop/planet/vip/user/checkin 的cookie即可
cookie = [
    'cUserId=******'
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
    user_url = 'https://api.vip.miui.com/api/community/user/home/page'
    html = requests.get(url=url, headers=headers)
    html_user = requests.get(url=user_url, headers=headers)
    result = json.loads(html.text)
    result_user = json.loads(html_user.text)
    userId = result_user['entity']['userId']
    print('*************'+'\n'+f'开始第{i + 1}个账号签到'+'\n'+'签到结果：')
    print('userId: '+userId + ' 用户名: '+result_user['entity']['userName']+ ' 段位: '+ result_user['entity']['userGrowLevelInfo']['showLevel'])
    print(result['message'])

    unfollow_url = 'https://api.vip.miui.com/api/community/board/unfollow?boardId=558495'
    html_unfollow = requests.get(url=unfollow_url, headers=headers)
    result_unfollow = json.loads(html_user.text)
    if result_unfollow['status']==200:
        print('退出圈子成功')


    follow_url = 'https://api.vip.miui.com/api/community/board/follow?boardId=558495'
    html_follow = requests.get(url=follow_url, headers=headers)
    result_follow = json.loads(html_user.text)
    if result_follow['status']==200:
        print('加入圈子成功')

    info_url =f'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction?userId={userId}&action=BROWSE_SPECIAL_PAGES_USER_HOME'
    html_info = requests.get(url=info_url, headers=headers)
    time.sleep(12)
    result_info = json.loads(html_info.text)
    if result_info['status'] == 200:
        print('浏览主页成功，获得积分： '+str(result_info['entity']['score']))
    else:
        print(result_info['message']+'，今日已达上限')

    for a in range(3):
        watch_url = f'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction?userId={userId}&action=BROWSE_POST_10S'
        html_watch = requests.get(url=watch_url, headers=headers)
        time.sleep(12)
        result_watch = json.loads(html_watch.text)
        if result_watch['status'] == 200:
            print('浏览帖子成功，获得积分： ' + str(result_watch['entity']['score']))
        else:
            print(result_watch['message'] + '，今日已达上限')
