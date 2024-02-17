"""
霸王茶姬集卡 v1.0

变量 authorization, 多账户换行或空格
export bjjkck=""

cron: 24 13,18 * * *
const $ = new Env("霸王茶姬集卡");
"""

import os
import requests
from datetime import datetime, timezone, timedelta

import json
import time
import requests
import json


#---------简化的框架--------
# 配置参数
tmid = "1755164227988152321"  # 正确答案ID     自己更新 
#13号 1755161779339538433
#14号 1755164227988152321
#activity_id = "1755164226767609858"  # 自定义EXAM 类型的题目ID  算了 还是写一个函数  自动获取


# 获取北京日期的函数
def get_beijing_date():  
    beijing_time = datetime.now(timezone(timedelta(hours=8)))
    return beijing_time.date()

def dq_time():
    # 获取当前时间戳
    dqsj = int(time.time())

    # 将时间戳转换为可读的时间格式
    dysj = datetime.fromtimestamp(dqsj).strftime('%Y-%m-%d %H:%M:%S')
    #print("当前时间戳:", dqsj)
    #print("转换后的时间:", dysj)

    return dqsj, dysj

# 获取环境变量
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        print(f'环境变量{var_name}未设置，请检查。')
        return None
    accounts = value.strip().split('\n')
    num_accounts = len(accounts)
    print(f'-----------本次账号运行数量：{num_accounts}-----------')
    print(f'-----------霸王茶姬集卡-1.02----------')
    return accounts


#-------------------------------封装请求-------------


def create_headers(token):
    headers = {
        "Host": "wxh5.icc.link",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "authorization": token,
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; COR-AL10 Build/HUAWEICOR-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20231201 MMWEBID/7516 MicroMessenger/8.0.45.2521(0x28002D3D) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "X-Requested-With": "com.tencent.mm",
        "Referer": "https://wxh5.icc.link/play/signin331713/?activityId=1755105287353331713&sourceActivityId=1755161061191380994",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        #"Cookie": f"token={token}"  # 正确的格式
    }
    return headers


chip_to_zodiac = {
    0: "万能碎片",  
    1: "鼠",
    2: "牛",
    3: "虎",
    4: "兔",
    5: "龙",
    6: "蛇",
    7: "马",
    8: "羊",
    9: "猴",
    10: "鸡",
    11: "狗",
    12: "猪"
}
#-------------------------------封装请求-------------

def send_sp(token):  # 查询碎片
    url = "https://wxh5.icc.link/play/rest/activity/blind-box/detail"
    headers = create_headers(token)
    payload = {
        "activityId": "1755105287353331713",
        "exchangeId": "",
        "giveId": ""
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # 检查响应码是否为200系列
        response_data = response.json()  # 返回JSON响应体
        
        # 提取 getChip 内容
        if response_data.get("successful") and "data" in response_data:
            data = response_data["data"]
            if "getChip" in data:
                get_chip_content = data["getChip"]
                for chip in get_chip_content:
                    chip_number = chip['chipNumber']
                    chip_sum = chip['chipSum']
                    # 假设 chip_to_zodiac 是一个已定义的映射
                    zodiac_name = chip_to_zodiac.get(chip_number, "未知生肖")
                    print(f"碎片 {chip_number}号 - {zodiac_name} - 数量{chip_sum}")
            
            # 提取 universalChip 中的 count
            if "universalChip" in data:
                universal_chip_count = data["universalChip"].get("count", 0)
                print(f"万能碎片数量: {universal_chip_count}")

        return response_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"请求异常: {err}")
    return None

#                 领取碎片 逻辑
def pd_sp_cs(token):
    url = "https://wxh5.icc.link/play/rest/activity/blind-box/detail"
    headers = create_headers(token)
    data = {
        "activityId": "1755105287353331713",
        "exchangeId": "",
        "giveId": ""
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

        remain_receive_count = response_data.get('data', {}).get('remainReceiveCount', 0)
        #print(f"剩余领取碎片次数: {remain_receive_count}")

        if remain_receive_count > 0:
            for _ in range(remain_receive_count):
                qd_ck(token)  # 根据剩余次数领取碎片

        return remain_receive_count
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"请求异常: {err}")
    return None



def qd_ck(token):  # 领取卡片
    url = "https://wxh5.icc.link/play/rest/activity/blind-box/receive-chip"
    headers = create_headers(token)
    data = {
        "activityId": "1755105287353331713",
        "memberId": "18382056209",  
        "wxGroupId": "",
        "source": "SHARE",
        "longitude": "",
        "latitude": "",
        "sourceActivityId": ""
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

        message = response_data.get('data', {}).get('message', '未知信息')
        selection_number = response_data.get('data', {}).get('selectionNumber')

        print("领取卡片 消息内容:", message)
        if selection_number is not None:
            # 假设chip_to_zodiac是一个字典，将selectionNumber映射到相应的生肖名称
            zodiac_name = chip_to_zodiac.get(selection_number, "未知生肖")
            print(f"恭喜您获得 {selection_number}号碎片: {zodiac_name}")

        return response_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"请求异常: {err}")
    return None

#                 领取碎片 逻辑  完


#            天天抽奖  
def djcj(token):  # 点击抽奖
    url = "https://wxh5.icc.link/api/app/play/new-dazhuanpan/draw"
    headers = create_headers(token)
    data = {
        "activityId": "1755151820108652545",
        "source": "BLIND_BOX",
        "sourceActivityId": "1755105287353331713"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 检查响应码是否为200系列
        response_data = response.json()  # 返回JSON响应体
        #print("点击抽奖 完整响应内容:", response.text)

        # 提取message, prizeActivityCount, 和 prizeName
        message = response_data.get('data', {}).get('message', '无消息')
        prize_activity_count = response_data.get('data', {}).get('prizeActivityCount', 0)  # 默认值为0
        prize_name = response_data.get('data', {}).get('prizeName', '无奖品名称')

        #
        print(f"天天抽奖  内容: {message}, 奖品名称: {prize_name}")

        return response_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"请求异常: {err}")
    return None

def ttcjjh(token):  # 抽奖机会判断
    url = "https://wxh5.icc.link/api/app/play/new-dazhuanpan/activity"
    headers = create_headers(token)
    data = {
        "activityId": "1755151820108652545",
        "wxChatGroupId": "",
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 检查响应码是否为200系列
        response_data = response.json()  # 返回JSON响应体

        # 提取times
        times = response_data.get('data', {}).get('times', 0)  # 如果没有times字段，默认为0
        #print(f"天天 抽奖次数为: {times}")

        if times > 0:
            print("有抽奖次数，即将进行抽奖...")
            djcj(token)  # 如果有抽奖次数，调用抽奖函数

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"请求异常: {err}")
#            天天抽奖     完



def query_exam(token, tmid, EXAMid): #判断问题
    url = "https://wxh5.icc.link/play/rest/activity/exam/query"
    headers = create_headers(token)
    data = {
        "id": EXAMid,
        "wxChatGroupId": ""
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

        answer_keyword = response_data.get('data', {}).get('answerKeyword', None)
        if answer_keyword is None:
            print("尚未回答问题")
            question_list = response_data.get('data', {}).get('questionList', [])
            for question in question_list:
                option_list = question.get('optionList', [])
                for option in option_list:
                    option_id = option.get('id')

                    if option_id == tmid.strip():
                        print(f"找到匹配的选项ID: {tmid}")
                        print(f"选项键: {option.get('optionKey')}")
                        submit_answer(token, option.get('optionKey'), EXAMid)  
        else:
            #print(f"已经回答过问题，答案关键字: {answer_keyword}")
            pass

        return response_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"请求异常: {err}")



def submit_answer(token, optionKey, EXAMid):
    """提交答案"""
    url = "https://wxh5.icc.link/play/rest/activity/exam/submit"
    headers = create_headers(token)
    data = {
        "answerKeyword": optionKey, 
        "id": EXAMid,  
        "wxChatGroupId": "",
        "source": "BLIND_BOX",
        "memberId": "18382056209"
    }
    print(data)  # 打印提交的数据，便于调试
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        response_data = response.json()
        #print(response_data)  # 打印响应数据，便于调试

        # 根据响应数据判断是否成功
        if response_data.get("successful") and response_data["data"].get("isSuccess"):
            print("答案提交成功")
        elif not response_data["data"].get("isSuccess"):
            message = response_data["data"].get("message", "未知错误")
            print(f"答案提交失败: {message}")
        else:
            print("提交失败，原因未知")
        return response_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"请求异常: {err}")


#         重写  回答问题      #  算了吧 放弃  就提取EXAM
def tqEXAMid(token):
    url = "https://wxh5.icc.link/api/app/play/common/relative/relative_activity_list"
    headers = create_headers(token)
    payload = {
        "memberId": "18382056209",
        "sourceActivityId": "1755105287353331713"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data["code"] == "200" and data["message"] == "操作成功":
            for activity in data["data"]["activityList"]:
                if activity["playCategoryCode"] == "EXAM":
                    #print({"EXAMid": activity["activityId"]})
                    return {"EXAMid": activity["activityId"]}
            print("没有找到指定类型 EXAM 的活动")
        else:
            print("响应错误，完整响应内容:", data)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"请求异常: {err}")









#本地测试用 
os.environ['cscs'] = '''

'''



def main():
    var_name = 'bjjkck'
    tokens = get_env_variable(var_name)
    if not tokens:
        print(f'环境变量{var_name}未设置，请检查。')
        return
    total_accounts = len(tokens)
    for i, token in enumerate(tokens, start=1):
        parts = token.split('#')
        if len(parts) < 1:
            print("令牌格式不正确。跳过处理。")
            continue

        token = parts[0]  # 使用令牌
        account_no = parts[1] if len(parts) > 1 else ""  
        print(f'------账号 {i}/{total_accounts}    {account_no}   -------')

        exam_activity_info = tqEXAMid(token)  # 提取题目ID
        if exam_activity_info:
            EXAMid = exam_activity_info.get('EXAMid')
            if EXAMid:
                query_exam_result = query_exam(token, tmid, EXAMid)  # 回答问题
                ttcjjh(token) #天天抽奖判断
                pd_sp_cs(token)#领取碎片判断
                send_sp(token)  # 查询碎片
            else:
                print("没有找到EXAM类型的活动ID。")
        else:
            print("未能获取活动信息。")

if __name__ == "__main__":
    main()




