#科技玩家-签到
#环境变量 kjwj="账户&密码"
import requests,json,re,os
#检测账号变量
kjwj = os.environ.get("kjwj") if os.environ.get("kjwj") else ""
#检测账号
if not kjwj or "&" not in kjwj:
    print("⚠️未发现有效账号,退出程序!")
    sys.exit()
test = kjwj.split('&')[0]
test2 = kjwj.split('&')[1]
username = ([test])
password = ([test2])
#print(username,password)

for i in range(len(username)):
    url = 'https://www.kejiwanjia.com/wp-json/jwt-auth/v1/token'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',
        'origin': 'https://www.kejiwanjia.com',
        'referer': 'https://www.kejiwanjia.com/'
    }
    data = {
        'username': f'{username[i]}',
        'password': f'{password[i]}'
    }
    html = requests.post(url=url, headers=headers, data=data)
    result = json.loads(html.text)
    name = result['name']
    token = result['token']
    check_url = 'https://www.kejiwanjia.com/wp-json/b2/v1/getUserMission'
    sign_url = 'https://www.kejiwanjia.com/wp-json/b2/v1/userMission'
    sign_headers = {
        'Host': 'www.kejiwanjia.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer ' + f'{token}',
        'cookie': f'b2_token={token};',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42'
    }
    html_1 = requests.post(url=check_url, headers=sign_headers)
    imfo_1 = json.loads(html_1.text)
    if imfo_1['mission']['credit'] == 0:
        print("🔁开始检查第"+str(i+1)+"个帐号"+ " " +  name)
        print("⚠️还未签到 开始签到")
        html_2 = requests.post(url=sign_url, headers=sign_headers)
        imfo_2 = json.loads(html_2.text)
        print("✅签到成功 获得" + imfo_2['mission']['credit'] + "积分")
    else:
        print("🔁帐号" + str(i + 1) + " " + name )
        print("✅今天已经签到 获得" + imfo_1['mission']['credit'] + "积分")
