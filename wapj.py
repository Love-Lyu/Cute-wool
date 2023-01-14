#吾爱破解-签到
#抓取 https://www.52pojie.cn/forum.php 整段cookie
import requests, os, sys
from bs4 import BeautifulSoup
from datetime import datetime
from sendNotify import send
#检测账户变量
wapj = os.environ.get("wapj") if os.environ.get("wapj") else ""
if not wapj:
    print("⚠️未发现有效账号,退出程序!")
    sys.exit()
#分割账户
cookie = [wapj]
#print(cookie)

for i in range(len(cookie)):
    print(f'🔁开始第{i+1}个帐号签到')
    headers = {
        "Cookie": f'{cookie[i]}',
        "ContentType": "text/html;charset=gbk",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }
    requests.session().put(
        "https://www.52pojie.cn/home.php?mod=task&do=apply&id=2", headers=headers
    )
    fa = requests.session().put(
        "https://www.52pojie.cn/home.php?mod=task&do=draw&id=2", headers=headers
    )
    fb = BeautifulSoup(fa.text, "html.parser")
    fc = fb.find("div", id="messagetext").find("p").text
    if "⚠️您需要先登录才能继续本操作" in fc:
        print("⚠️Cookie 失效")
        msg1 = '⚠️Cookie 失效'
    elif "✅恭喜" in fc:
        print("✅签到成功")
        msg2 = '✅签到成功'
    elif "⚠️不是进行中的任务" in fc:
        print("✅今日已签到")
    else:
        print("⚠️签到失败")
        msg3 = '⚠️签到失败'
# 执行完毕发送通知
title = '🔁吾爱破解-签到'
msg = f"⏰{str(datetime.now())[:19]}\n" + (msg1) + (msg2) + (msg3)
send(title,msg)