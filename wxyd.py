"""
微信阅读 v1.0

任务：刷文章 提现

cookie填到变量 wxyd 中, 多账户&间隔
export wxyd=""

cron: 36 8-18 * * *
const $ = new Env("微信阅读");
"""

import time
import hashlib
import requests
import random
import re
import os
import sys

# 微信阅读
class WXYD():
  # 初始化
  def __init__(self, cookie):
        # 检测条目
        self.checkDict = {
            'MzkyMzI5NjgxMA==': ['每天趣闻事', ''],
            'MzkzMzI5NjQ3MA==': ['欢闹青春', ''],
            'Mzg5NTU4MzEyNQ==': ['推粉宝助手', ''],
            'Mzg3NzY5Nzg0NQ==': ['新鲜事呦', ''],
            'MzU5OTgxNjg1Mg==': ['动感比特', ''],
            'Mzg4OTY5Njg4Mw==': ['邻居趣事闻', 'gh_60ba451e6ad7'],
            'MzI1ODcwNTgzNA==': ['麻辣资讯', 'gh_1df5b5259cba'],
        }
        
        # 授权
        self.headers = {
            'Host': '2478987.jilixczlz.ix47965in5.cloud',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh',
            'Cookie': f'gfsessionid={cookie}',
        }
        
        # 请求
        self.sec = requests.session()
        self.sec.headers = self.headers
        
        # 初始化金币
        self.remain = 0
        
  # 获取信息
  def getinfo(self, link):
    try:
        response = requests.get(link)
        html = re.sub('\s', '', response.text)
        biz = re.findall('varbiz="(.*?)"\|\|', html)
        if biz != []:
            biz=biz[0]
        if biz == '' or biz == []:
            if '__biz' in link:
                biz = re.findall('__biz=(.*?)&', link)
                if biz != []:
                    biz = biz[0]
        nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
        if nickname != []:
            nickname = nickname[0]
        user_name = re.findall('varuser_name="(.*?)";', html)
        if user_name != []:
            user_name = user_name[0]
        msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
        if msg_title != []:
            msg_title=msg_title[0]
        text=f'公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}'
        return nickname, user_name, msg_title, text, biz
    except Exception as e:
        print(e)
        print('异常')
  
  # sign算法
  def zzb_sign(self, data):
      hash = hashlib.sha256()
      hash.update(data.encode())
      sign = hash.hexdigest()
      return sign
  
  # 获取系统信息
  def msg(self):
      try:
          ts = int(time.time())
          text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
          sign = self.zzb_sign(text)
          url = f'http://2478987.jilixczlz.ix47965in5.cloud/user/msg?time={ts}&sign={sign}'
          response = self.sec.get(url)
          data = response.json()
          # print(f'系统公告:{rj.get("data").get("msg")}')
      except:
          # print(r.text)
          return False
          
  # 获取Uid
  def user_info(self):
      ts = int(time.time())
      text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
      sign = self.zzb_sign(text)
      url = f'http://2478987.jilixczlz.ix47965in5.cloud/user/info?time={ts}&sign={sign}'
      try:
          response = self.sec.get(url)
          data = response.json()
          if data.get('code') == 0:
              print(f'用户UID:{data.get("data").get("uid")}')
          else:
              print(f'获取用户信息失败，账号异常')
      except:
          print(response.text)
          print(f'获取用户信息失败,gfsessionid无效，请检测gfsessionid是否正确')
          
  # 获取用户信息
  def read_info(self):
      try:
          ts = int(time.time())
          text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
          sign = self.zzb_sign(text)
          url = f'http://2478987.jilixczlz.ix47965in5.cloud/read/info?time={ts}&sign={sign}'
          response = self.sec.get(url)
          data = response.json()
          print(f'今日已经阅读了{data.get("data").get("read")}篇文章 | 账户余额{data.get("data").get("remain")}金币')
      except:
          print(response.text)
  
  # 阅读文章
  def read(self):
    print('阅读开始')
    while True:
        print('-' * 50)
        ts = int(time.time())
        text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
        sign = self.zzb_sign(text)
        url = f'http://2478987.jilixczlz.ix47965in5.cloud/read/task?time={ts}&sign={sign}'
        response = self.sec.get(url)
        data = response.json()
        msg = data.get('message')
        print(msg)
        code = data.get('code')
        if code == 0:
            uncode_link = data.get('data').get('link')
            print('获取到阅读链接成功')
            link = uncode_link.encode().decode()
            a = self.getinfo(link)
            sleeptime = random.randint(7, 10)
            print('本次模拟阅读', sleeptime, '秒')
            time.sleep(sleeptime)
        elif code == 400:
            print('未知情况400')
            time.sleep(10)
            continue
        elif code == 20001:
            print('未知情况20001')
        else:
            return False
        # -----------------------------
        ts = int(time.time())
        finish_headers = self.sec.headers.copy()
        finish_headers.update({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Origin': 'http://2478987.jilixczlz.ix47965in5.cloud'})
        text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
        sign = self.zzb_sign(text)
        data = f'time={ts}&sign={sign}'
        url = f'http://2478987.jilixczlz.ix47965in5.cloud/read/finish'
        response = requests.post(url, headers = finish_headers, data=data)
        data = response.json()
        if data.get('code') == 0:
            if data.get('data').get('check') == False:
                gain = data.get('data').get('gain')
                self.remain = data.get("data").get("remain")
                print(f"阅读文章成功获得{gain}金币")
                print(
                    f'当前已经阅读了{data.get("data").get("read")}篇文章，账户余额{self.remain/10000}元')
            else:
                print("过检测成功")
                print(f'当前已经阅读了{data.get("data").get("read")}篇文章，账户余额{self.remain/10000}元')
        else:
            return False
        time.sleep(1)
        print('开始本次阅读')
  
  # 阅读检测
  def testCheck(self, a, link):
    if self.checkDict.get(a[4]) != None:
        for i in range(60):
            if i == '0':
                print('过检测文章已经阅读')
                return True
            elif i == '1':
                print(f'正在等待过检测文章阅读结果{i}秒。。。')
                time.sleep(1)
            else:
                print('服务器异常')
                return False
        print('过检测超时中止脚本防止黑号')
        return False
    else:
        return True
          
  # 提现
  def withdraw(self):
    if self.remain < 3000:
            print('没有达到提现标准')
            return False
    ts = int(time.time())
    text = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
    sign = self.zzb_sign(text)
    u = f'http://2478987.84.8agakd6cqn.cloud/withdraw/wechat?time={ts}&sign={sign}'
    r = self.sec.get(u, headers=self.headers)
    print('提现结果', r.text)
  
  # 运行
  def run(self):
    self.user_info()
    self.msg()
    self.read_info()
    self.read()
    time.sleep(5)
    self.withdraw()
  
if __name__ == '__main__':
    print('🔔微信阅读 | 开始')
    #检测账户变量
    wxyd = os.environ.get("wxyd") 
    if not wxyd:
        sys.exit("⚠️未发现有效cookie,退出程序!") 
    #分割账户
    if "&" not in wxyd:
        cookie = [wxyd]
    else:
        cookie = wxyd.split("&")
    # 遍历账户列表 | 为每个账户创建一个类实例并执行任务
    for account in cookie:
        wxyd_client = WXYD(account)
        wxyd_client.run()