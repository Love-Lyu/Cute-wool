#科技玩家-签到
#环境变量 kjwj="账户&密码" 多账户 # 分割
import requests,json,re,os,sys
from datetime import datetime
from sendNotify import send
#检测账户变量
kjwj = os.environ.get("kjwj") 
if not kjwj or "@" not in kjwj:
   sys.exit("⚠️未发现有效账号,退出程序!") 
#分割账户
accounts = kjwj.split('#')
username,password = zip(*(i.split('&') for i in accounts))
#print(username,password)
zh,zh_1 = username[:2]
#print(zh,zh_1)
#主程序
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
        title = '🔁科技玩家-签到'
        print(title)
        print("🔁环境变量[ kjwj ]加载成功")
        print("🔁找到第" + str(i+1) + "个账号")
        print('*************')
        print("🔁开始检查第"+str(i+1)+"个帐号"+ " " +  name)
        print("⚠️还未签到 开始签到")
        html_2 = requests.post(url=sign_url, headers=sign_headers)
        imfo_2 = json.loads(html_2.text)
        print("✅签到成功 获得" + imfo_2['mission']['credit'] + "积分")
        msg = f"⏰{str(datetime.now())[:19]}\n" + '🔁' + str(zh) + '\n' + "✅签到成功 获得" + imfo_2['mission']['credit'] + "积分" + '\n' + '🔁' + str(zh_1) + '\n' + "✅签到成功 获得" + imfo_2['mission']['credit'] + "积分"
        print('*************')
    else:
        title = '🔁科技玩家-签到'
        print(title)
        print("🔁环境变量[ kjwj ]加载成功")
        print("🔁找到第" + str(i+1) + "个账号")
        print('*************')
        print("🔁帐号" + str(i + 1) + " " + name )
        print("✅今天已经签到 获得" + imfo_1['mission']['credit'] + "积分")
        msg = f"⏰{str(datetime.now())[:19]}\n" + '🔁' + str(zh) + '\n' + "✅今天已经签到 获得" + imfo_1['mission']['credit'] + "积分" + '\n' + '🔁' + str(zh_1) + '\n' + "✅今天已经签到 获得" + imfo_1['mission']['credit'] + "积分"
        print('*************')
# # 执行完毕发送通知
print('🔁开始发送通知')
send(title,msg)