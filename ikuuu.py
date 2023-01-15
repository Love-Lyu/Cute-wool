#ikuuu机场-签到
#https://ikuuu.dev/user 的cookie
import requests, json,re,os,sys
from datetime import datetime
from sendNotify import send
#检测账户变量
#ikuuu = os.environ.get("ikuuu") if os.environ.get("ikuuu") else ""
#if not ikuuu:
#    print("⚠️未发现有效cookie,退出程序!")
#    sys.exit()
#分割账户
cookie = [lang=zh-cn; uid=516722; email=1489221272@qq.com; key=80b92271513a6ddc5a5fabb61e00e5ebc8df8780397dd; ip=97ed8a28bc393bbf6066efb295aab96f; expire_in=1674389105]
#print(cookie)

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
#title = '🔁ikuuu机场-签到'
#msg = f"⏰{str(datetime.now())[:19]}\n" + '✅签到成功'
#send(title,msg)