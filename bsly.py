"""
项目 百事乐元 - 抽奖活动
最好手动抽一次，同意协议。
变量 token#l_id#备注     多账号换行  
变量名 bslycj
例如：aa084f61ece7b379cbe4515aee00d238d76,ofwefwqefhXy2_gwefwTs#88878311#大号

dhzdsx = 1/0 是 控制 组队逻辑的 默认随机组队
--------------更新/注意--说明-------------


注意 最好手动抽一次，同意协议。
1.1更新   随机组队
1.2 更新  组队判断/逻辑  time 2024年1月27日02:31:52
"""
import os
import requests
from datetime import datetime, timezone, timedelta
import json
import time
import random

#---------简化的框架--------
dhzdsx = 1 # 设置为 0 表示按顺序组队，设置为 1 表示随机组队
# 配置参数
base_url = "https://hxxxy.gov.cn"  # 已修改为实际的基础URL
user_agent = "Mozilla/5.0 (Linux; Android 11; ONEPLUS A6000 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160049 MMWEBSDK/20231201 MMWEBID/2930 MicroMessenger/8.0.45.2521(0x28002D36) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android"

# 获取北京日期的函数
def get_beijing_date():  
    beijing_time = datetime.now(timezone(timedelta(hours=8)))
    return beijing_time.date()

def dq_time():
    dqsj, dysj = int(time.time()), datetime.fromtimestamp(dqsj).strftime('%Y-%m-%d %H:%M:%S')
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
    print(f'-----------项目 百事乐元 - 抽奖活动-----脚本作者: QGh3amllamll  ------')
    return accounts

# 封装请求头
def create_headers(account_token):
    headers = {
        'host': 'pepcoinbhhpre.pepcoinbypepsico.com.cn',
        'accept': 'application/json, text/plain, */*',
        'user-agent': user_agent,
        'charset': 'utf-8',
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'token': account_token,
        'Referer': 'https://servicewechat.com/wx1a72addb7ee74f67/124/page-frame.html'
    }
    return headers

def cj(account_token):#抽奖
    url = "https://pepcoinbhhpre.pepcoinbypepsico.com.cn/mp/draw"
    headers = create_headers(account_token)
    #print(headers)
    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            #print(response.json())

            # 检查响应的code
            if response_data.get('code') == 0:
                prize_name = response_data.get('data', {}).get('name')
                if prize_name == "现金红包":
                    amount = response_data.get('data', {}).get('amount', 0)
                    print(f"获得现金红包: {amount / 100} 元")
                    # 如果需要在获得红包后继续请求，保持这个循环；如果不需要，使用 break 退出循环
                elif prize_name:
                    print(f"获得奖品: {prize_name}")
                    #break  # 收到奖品后退出循环
                else:
                    print("响应中没有奖品名称。")
                    break
            else:
                print("抽奖次数超限")
                #print("抽奖完整响应内容:", response_data)
                break

            # 暂停 3 到 5 秒后继续下一次请求
            time.sleep(random.randint(3, 5))

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None

def hql_id(account_token): #获取iid

    try:
        token = account_token.split(',')[0]
    except IndexError:
        print("Token 提取失败或格式不正确")
        return

    url = "https://pepcoinnew.pepcoinbypepsico.com.cn/api/v1/wxapp/doGetUserInfo"
    headers = {
        'Host': 'pepcoinnew.pepcoinbypepsico.com.cn',
        'Connection': 'keep-alive',
        'Content-Length': '96',
        'charset': 'utf-8',
        'user-agent': user_agent,
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'Referer': 'https://servicewechat.com/wx1a72addb7ee74f67/124/page-frame.html',
    }
    #print(headers)
    data = {
        "token": token,
        "provision": "2_0_6"
    }
    #print(data)
    try:
        response = requests.post(url, json=data, headers=headers)
        #print("响应状态码:", response.status_code)
        #print("响应内容:", response.text)

        if response.status_code == 200:
            # 解析响应内容
            response_data = json.loads(response.text)
            if response_data.get('code') == 0:
                l_id = response_data['data'].get('l_id', '未知')
                print("l_id:", l_id)
            else:
                print("操作未成功，响应 code 不为 0")
        else:
            print("请求可能遇到问题，检查状态码和响应内容")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

def add_tmrw(account_token):#天猫会员任务
    url = "https://pepcoinbhhpre.pepcoinbypepsico.com.cn/mp/addTMallMember"
    headers = create_headers(account_token)
    #print(account_token)
    try:
        response = requests.get(url, headers=headers)  # 尝试使用GET方法
        response_data = response.json()  # 解析响应为JSON
        #print(response_data)  # 打印响应的JSON数据

        # 根据返回的code和data字段判断操作结果
        if response_data.get("code") == 0:
            if response_data.get("data") == 1:
                print("添加天猫会员任务成功，增加抽奖机会+1。")
            else:
                print("添加天猫会员任务失败。")
        else:
            print("请求异常，响应内容：" + str(response_data))

    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")

def zd_jh(account_token):  # 判断组队机会
    url = "https://pepcoinbhhpre.pepcoinbypepsico.com.cn/mp/getMyTeam"
    headers = create_headers(account_token)

    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()  # 解析响应为JSON
        if response_json.get('code') == 0:  # 根据 code 的值进行判断
            data = response_json.get('data', {})
            teamCount = data.get('teamCount', 0)  # 确保默认值为0
            # 其他信息可以根据需要返回
            return {"teamCount": teamCount}
        else:
            print("不是0 打印", response_json)
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None


def post_join_team(dc_iid, zd_token, account_no):  # 组队逻辑
    url = "https://pepcoinbhhpre.pepcoinbypepsico.com.cn/mp/postJoinTeam"
    headers = create_headers(zd_token)
    data = {"inviteUser": dc_iid}  # 使用轮流作队长的IID

    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()  # 解析响应为JSON
   
        code = response_data.get("code")
        data_value = response_data.get("data")
        #print(data_value)
        if code == 0:
            if isinstance(data_value, dict) and 'name' in data_value:
                name = data_value['name']
                if name == '现金红包' and 'amount' in data_value:
                    amount = data_value['amount'] / 100
                    print(f"组队奖品: 现金红包  {amount}元")
                else:
                    print(f"组队奖品: {name}")

            elif data_value == 5:
                print(f"{account_no} 不能加入自己的队伍。")
            elif data_value == 4:
                #print(f"{account_no} 已经在{dc_iid} 队伍里了。")     
                print(f"{account_no} 已经在队伍里了。")              
            elif data_value == 3:
                #print(f"{account_no} 和{dc_iid}组过队了，组队失败。")     
                print(f"{account_no} 和组过队了，组队失败。")            

            elif data_value == 2:
                print(f"组长没有次数，退出帮组队")
                return False  # 当组长没有次数时返回 False
            elif data_value == 1:
                print(f"{account_no} 今天组队次数已经使用完。退出工具人列表")
                return "yddm"  # 当队员没有次数时返回特定标识

            elif data_value == 0:
                print(f"{account_no} 加入队伍  成功。")
            else:
                print(f"未知响应数据: {response_data}")
        else:
            print(f"未知响应: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

    # 每次请求后暂停 1 到 2 秒
    time.sleep(random.randint(1, 2))
    return True  # 函数成功完成



def cj_prizes(account_token, page=1):  # 抽奖的奖品信息
    """获取我的奖品信息"""
    total_cash = 0
    url = f"https://pepcoinbhhpre.pepcoinbypepsico.com.cn/mp/getMyPrizes?page={page}"
    headers = create_headers(account_token)
    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()  # 解析响应为JSON

        if response_data.get("code") == 0 and "data" in response_data:
            prizes = response_data["data"]
            for prize in prizes:
                act_time = prize.get("actTime")
                prize_name = prize.get("prizeName")
                # 特别判断现金红包
                if "现金红包" in prize_name:
                    cash_amount = float(prize_name.split('元')[0])  # 提取现金金额
                    total_cash += cash_amount
                    print(f"抽奖 ：{prize_name}，时间：{act_time}")

        else:
            print("获取奖品信息失败或没有奖品。")
        return total_cash  # 正常情况下返回总金额

    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
        return total_cash  # 异常情况下返回总金额

def zd_prize(account_token):  # 获取团队奖品信息
    """获取团队奖品信息"""
    total_cash = 0
    url = "https://pepcoinbhhpre.pepcoinbypepsico.com.cn/mp/getTeamPrize"
    headers = create_headers(account_token)
    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()  # 解析响应为JSON

        if response_data.get("code") == 0 and "data" in response_data:
            team_prizes = response_data["data"]
            for prize in team_prizes:
                prize_name = prize.get("prizeName") or "未知奖品"
                grant_time = prize.get("grantTime")
                if "现金红包" in prize_name:
                    cash_amount = float(prize_name.split('元')[0])  # 提取现金金额
                    total_cash += cash_amount
                    print(f"组队 ：{prize_name}，时间：{grant_time}")
        else:
            print("获取团队奖品信息失败或没有奖品。")
        return total_cash  # 正常情况下返回总金额

    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
        return total_cash  # 异常情况下返回总金额


#本地测试用 
os.environ['bslyccscscsj'] = '''

a2433423324234ac40eb234r23238d76,oKW23242TP42wTs#8882141#大号

'''
#本地测试用 
def main():  #这个没有问题
    var_name = 'bslycj'
    tokens = get_env_variable(var_name)
    if not tokens:
        print(f'环境变量{var_name}未设置，请检查。')
        return

    total_accounts = len(tokens)
    team_counts = {}  # 存储每个账号的团队数量
    accounts_with_teams = []  # 存储团队数量大于0的账号

    # 首先遍历所有账号执行抽奖逻辑和获取团队数量
    for i in range(total_accounts):
        parts = tokens[i].split('#')
        account_token = parts[0]
        dc_iid = parts[1]
        account_no = parts[2]  # 提取账号名称

        # 抽奖逻辑
        print(f'------账号 {i+1}/{total_accounts} {account_no} 抽奖-------')
        #add_tmrw(account_token)
        cj(account_token)

        # 获取团队数量
        # 获取团队数量
        team_info = zd_jh(account_token)
        print(f"账号 {account_no} 的组队信息: {team_info}")  # 调试打印

        if team_info and 'teamCount' in team_info:
            team_count = team_info['teamCount']
            team_counts[account_no] = team_count
            if team_count > 0:
            #if team_count > -1:
                accounts_with_teams.append(account_no)  # 仅存储团队数量大于0的账号

        print(f"当前账号 {account_no} 处理后的 可以组队id: {accounts_with_teams}")  # 调试打印
    print()
    print()
    print()
    print("所有账号的抽奖和团队数量检查完成，开始组队操作")


    # 组队操作
    print("开始组队操作")

    for account_no in accounts_with_teams:  # 队长按顺序进行
        i = [i for i, part in enumerate(tokens) if part.split('#')[2] == account_no][0]
        parts = tokens[i].split('#')
        account_token = parts[0]
        dc_iid = parts[1]

        print(f'------账号 {i+1}/{total_accounts} {account_no}组长{dc_iid} 开始组队-------')

        # 创建除了当前队长之外的账号列表
        other_accounts = [t.split('#')[2] for t in tokens if t.split('#')[2] != account_no]
        
        # 根据 dhzdsx 的值决定队友选择方式
        if dhzdsx == 1:
            random.shuffle(other_accounts)  # 如果 dhzdsx 为 1，随机排序队友

        # 尝试与排序后的其他账号组队
        for zd_account_no in other_accounts:
            if zd_account_no in accounts_with_teams:
                result = post_join_team(dc_iid, [part for part in tokens if part.split('#')[2] == zd_account_no][0].split('#')[0], zd_account_no)
                if result == "yddm":
                    accounts_with_teams.remove(zd_account_no)  # 移除已用完次数的账号
                elif result is False:
                    break  # 如果组长没有次数，终止循环

    print("所有账号的组队操作完成")

    for i in range(total_accounts):
        parts = tokens[i].split('#')
        account_token = parts[0]
        account_no = parts[2]

        # 查看奖品
        print()
        print(f'------账号 {i+1}/{total_accounts} {account_no} 查看奖品-------')
        cj_cash = cj_prizes(account_token, 1)
        zd_cash = zd_prize(account_token)

        #print(f"账号 {account_no} 抽奖现金红包金额：{cj_cash}元")
        #print(f"账号 {account_no} 组队现金红包金额：{zd_cash}元")
        #print(f"账号 {account_no} 总计现金红包金额：{cj_cash + zd_cash}元")
        print(f"账号 {account_no} 抽奖{round(cj_cash, 2)}元 组队{round(zd_cash, 2)}元 总计：{round(cj_cash + zd_cash, 2)}元")


if __name__ == "__main__":
    main()
