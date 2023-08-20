"""
快手答题 v1.0

自行捉包, 游戏页面, 抓包搜关键词game
把域名请求头里的cookie和ua填到变量 ksdt 中, 多账号&隔开
export ksdt="cookie#ua"

cron: 26 8,18 * * *
const $ = new Env("快手答题");
"""

import time
import requests
import random
import os
import json
import sys

# server data
IP1 = "119.29.118.112:20238"
IP2 = "authentication.pearsons.live:35003"

# get environment variable
def ger_env(key):
  cookies = os.getenv(key)
  if cookies:
    cookies = cookies.split("&")
    return cookies
  else:
    print("获取账号失败")
    sys.stdout.flush()
    
# print account
def printf(text):
  print(f"[账号{i}]-{text}")
  sys.stdout.flush()
  
# Kwai answer clase
class KS:
  # initialization
  def __init__(self, cookie):
    cookie_list = cookie.split("#")
    self.cookie = cookie_list[0]
    self.ua = cookie_list[1]
  # Kwai answer run
  def run(self):
    roundId, index, question, options = self.get_question()
    while roundId:
      time.sleep(0.5)
      answer_index = self.search(question, options)
      time.sleep(random.randint(3, 5))
      roundId, index, question, options = self.reply(roundId, index, question, options, answer_index)
      if roundId is None:
        break
  # get Kwai answer topic
  def get_question(self):
    url = "https://encourage.kuaishou.com/rest/n/encourage/game/quiz/round/kickoff?reKickoff=false&sigCatVer=1"
    header = {
      "Host": "encourage.kuaishou.com",
      "User-Agent": self.ua,
      "X-Requested-With": "com.kuaishou.nebula",
      "Sec-Fetch-Site": "same-origin",
      "Sec-Fetch-Dest": "empty",
      "Cookie": self.cookie,
      "content-type": "application/x-www-form-urlencoded;charset=UTF-8"
      }
    try:
      response = requests.get(url=url, headers=header)
      if response.json().get("result") == 1 and response.json().get("data").get("roundId"):
        roundId = response.json().get("data").get("roundId")
        questionDetail = response.json().get("data").get("questionDetail")
        index = questionDetail.get("index")
        question = questionDetail.get("question")
        options = questionDetail.get("options")
        current_amount = response.json().get("data").get("amount").get("current")
        printf(f"当前金币 | {current_amount}")
        sys.stdout.flush()            
        printf(f"开始答题 | {question}")
        sys.stdout.flush()
        printf(f"选项 | {options}")
        sys.stdout.flush()
        return roundId, index, question, options
      elif response.json().get("result") == 103703:
        printf("今日题目已答完")
        sys.stdout.flush()
        printf(f"-----------------------------------------")
        sys.stdout.flush()
        return None, None, None, None
    except:
      print("未知错误")
      sys.stdout.flush()
      return None, None, None, None
  
  # search Kwai answer server
  def search(self, question, options):
    try:
      printf("开始数据库查找答案")
      sys.stdout.flush()
      url1 = f"http://{IP1}/search?question={question}"
      url2 = f"http://{IP2}/search?question={question}"
      response1 = requests.get(url=url1)
      if response1.json().get("status") == "200":
        printf("找到答案了")
        sys.stdout.flush()
        answer = response1.json().get("content")
        answer_index = options.index(answer)
        return answer_index
      else:
        response2 = requests.get(url=url2)
        if response2.json().get("status") == "200":
          printf("找到答案啦")
          sys.stdout.flush()
          answer = response2.json().get("content")
          answer_index = options.index(answer)
          self.upload(IP1, question, answer)
          return answer_index
        else:
          printf("没有找到答案,随便选一个吧")
          sys.stdout.flush()
          return 4
    except:
      return 4
  
  # reply Kwai answer server
  def reply(self, roundId, index, question, options, answer_index):
    url = "https://encourage.kuaishou.com/rest/n/encourage/game/quiz/round/answer/upload?sigCatVer=1"
    header = {
      "Host": "encourage.kuaishou.com",
      "User-Agent": self.ua,
      "Accept": "*/*",
      "Origin": "https://encourage.kuaishou.com",
      "X-Requested-With": "com.kuaishou.nebula",
      "Sec-Fetch-Site": "same-origin",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Dest": "empty",
      "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
      "Cookie": self.cookie,
      "content-type": "application/json"
      }
    payload = {
      "roundId": roundId,
      "index": index,
      "answer": answer_index
      }
    if answer_index == 4:
      payload = {
        "roundId": roundId,
        "index": index,
        "answer": random.randint(0, 3)
        }
      payload = json.dumps(payload)
      response = requests.post(url=url, headers=header, data=payload)
      if answer_index == 4:
        question = question
        correctAnswerIndex = response.json().get("data").get("answerDetail").get("correctAnswerIndex")     
        correct_answer = options[correctAnswerIndex]
        self.upload(IP1, question, correct_answer)
        time.sleep(0.5)
        if response.json().get("data").get("answerDetail").get("correct") and response.json().get("result") == 1:
          amount = response.json().get("data").get("amount").get("reward")
          current_amount = response.json().get("data").get("amount").get("current")
          printf(f"第[{int(index) + 1}]题回答正确 | 获取金币{amount} | 当前金币{current_amount}")
          sys.stdout.flush()
          printf(f"-----------------------------------------")
          sys.stdout.flush()
          if index == 9:
            return None, None, None, None
          else:
            questionDetail = response.json().get("data").get("nextQuestionDetail").get("questionDetail")
            index = questionDetail.get("index")
            roundId = response.json().get("data").get("nextQuestionDetail").get("roundId")
            question = questionDetail.get("question")
            options = questionDetail.get("options")
            printf(f"开始答题 | {question}")
            sys.stdout.flush()
            printf(f"选项 | {options}")
            sys.stdout.flush()
            return roundId, index, question, options
        else:
          printf(f"第[{int(index) + 1}]题回答错误")
          sys.stdout.flush()
          printf(f"-----------------------------------------")
          sys.stdout.flush()
          return None, None, None, None
  
  # update Kwai answer server
  def upload(self, ip, question, answer):
    try:
      printf("开始上传题目和答案")
      sys.stdout.flush()
      url = f"http://{ip}/upload"
      payload = {
        "question": question,
        "answer": answer
        }
      response = requests.post(url=url, data=payload)
      if response.json().get("status") == 200:
        printf("上传成功")
        sys.stdout.flush()
    except:
      pass
        

if __name__ == "__main__":
  cookies = ger_env("ksdt")
  num_accounts = len(cookies)
  print(f"快手答题共获取到{num_accounts}个账号\n")
  i = 0
  for cookie in cookies:
    i += 1
    KS(cookie).run()