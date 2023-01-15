#机场签到
#环境变量 jcqd="邮箱&秘密&网址" 多账户 # 分割
import requests,time,os,sys
from datetime import datetime
from sendNotify import send
#检测账户变量
jcqd = os.environ.get("jcqd") if os.environ.get("jcqd") else ""
if not jcqd:
    print("⚠️未发现有效账户,退出程序!")
    sys.exit()
#分割账户
account = jcqd.split('#')
for i in account:
    findAccount = i.split('&')
    email = findAccount[0] 
    passwd = findAccount[1]
    url = findAccount[2]
    #print(email,passwd,url)

headers = {
    'Host': url,
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="98"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://'+url,
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://'+url+'/user/login?redirect=%%2F',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}
url = 'https://www.'+url
r = requests.post(url+'/api/token', headers=headers,
                  json={'email': email, 'passwd': passwd})
headers.update({'Access-Token': r.json()['token']})
headers['Referer'] = url+'/user/index'
time.sleep(2)
r = requests.get(url+'/api/user/checkin', headers=headers)
# 执行完毕发送通知
title = '🔁机场签到'
msgtext = f"⏰{str(datetime.now())[:19]}\n" + '✅签到成功'
send(title,msgtext)