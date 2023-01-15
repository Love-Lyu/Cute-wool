#ikuuu机场-签到
#https://ikuuu.dev/user 的cookie
#环境变量 ikuuu="cookie" 多账户 # 分割
import requests, json,re,os,sys
from datetime import datetime
from sendNotify import send
#检测账户变量
ikuuu = os.environ.get("ikuuu") if os.environ.get("ikuuu") else ""
if not ikuuu:
    print("⚠️未发现有效cookie,退出程序!")
    sys.exit()
#分割账户
account = ikuuu.split('#')
for i in account:
    findAccount = i.split('#')
    cookie = findAccount[0]
    #print(cookie)
#主程序
url_info = 'https://ikuuu.dev/user/profile'
url = 'https://ikuuu.dev/user/checkin'
headers = {
    'cookie': f'{cookie}',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
}
html_info = requests.get(url=url_info, headers=headers).text
html = requests.post(url=url, headers=headers)
result = json.loads(html.text)['msg']
info = "".join(re.findall('<div class="d-sm-none d-lg-inline-block">(.*?)</div>', html_info, re.S))
print(info+'\n'+result)
# 执行完毕发送通知
title = '🔁ikuuu机场-签到'
msgtext = f"⏰{str(datetime.now())[:19]}\n" + '✅签到成功'
send(title,msgtext)