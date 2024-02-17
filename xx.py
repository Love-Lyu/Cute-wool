"""
心喜 v1.0

变量 sso#备注, 多账户换行或空格
export XSSONF=""

cron: 48 11,16 * * *
const $ = new Env("心喜");
"""

import os
import requests
import random
from datetime import datetime, timezone, timedelta
import time
import sys
import io

# 控制是否启用通知的变量
enable_notification = 1

# 只有在需要发送通知时才尝试导入notify模块
if enable_notification == 1:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。它不是一个依赖项，请勿错误安装。程序将退出。")
        sys.exit(1)

#---------简化的框架--------
# 配置参数
BASE_URL = "https://api.xinc818.com/mini/"

# 获取北京日期的函数
def get_beijing_date():  
    beijing_time = datetime.now(timezone(timedelta(hours=8)))
    return beijing_time.date()

def dq_time():
    # 获取当前时间戳
    dqsj = int(time.time())
    # 将时间戳转换为可读的时间格式
    dysj = datetime.fromtimestamp(dqsj).strftime('%Y-%m-%d %H:%M:%S')
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
    print(f'----------项目：心喜小程序-----------')
    return accounts

# 封装请求头
def create_headers(sso):
    headers = {
        'Host': 'api.xinc818.com',
        'Connection': 'keep-alive',
        'sso': sso,
        'xweb_xhr': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090819) XWEB/8531',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    return headers

def rwlb(sso):  # 任务列表
    urlrw = BASE_URL + 'dailyTask/daily'  # 确保字符串连接正确
    headers = create_headers(sso)
    try:
        response = requests.get(urlrw, headers=headers)
        response_data = response.json()

        if response_data["code"] != 0 or response_data["data"] is None:
            print("错误响应或数据为空，跳过当前账号")
            return None

        for task in response_data["data"]:
            task_id = task.get("id")
            task_name = task.get("name")
            task_status = task.get("status")

            # 跳过不需要处理的任务
            if task_name in ["完善个人资料", "购买商城商品", "参加活动", "申请试用", "提交反馈建议"]:
                print(f"🚫🚫'{task_name}' ⛔⛔⛔跳过❌❌。")
                continue

         
            if task_status:  # 如果任务状态为 True (已完成)
                print(f"任务 '{task_name}' 已完成。")
            #elif task_name == "参与讨论":  # 测试bug
            #    selected_post = fetch_posts_data(sso)
            #    if selected_post:
            #        post_id = selected_post[0]  # 假设列表的第一个元素是 post_id
            #        cytl(sso, post_id)
                continue




            print(f"任务 '{task_name}' 尚未完成。进行处理...")
            if task_name == "分享心喜":
                fx_xx(sso)
            elif task_name == "签到打卡":
                sign_dk(sso, task_id)  
            elif task_name == "想要商品":
                xysp(sso)              
            elif task_name == "大转盘抽奖":
                dzp_cj(sso, task_id)      
            elif task_name == "去商城浏览30秒":
                ll_sp(sso, task_id)   
            elif task_name == "发帖":
                hitokoto_content = fetch_hitokoto()  # 获取一言内容
                if hitokoto_content and not hitokoto_content.startswith("请求一言失败"):
                    rw_post(sso, hitokoto_content, task_id)  # 使用一言内容作为发帖内容
                else:
                    print("未能获取有效的一言内容，无法执行发帖操作。跳过此任务。")
            elif task_name == "点赞用户":
                selected_post = fetch_posts_data(sso)
                if selected_post:
                    post_id = selected_post[0]  # 从选中的帖子中获取 post_id
                    like_post(sso, post_id)  # 执行点赞操作
                else:
                    print("未能获取帖子数据，无法执行点赞操作。")
            elif task_name == "关注用户":
                selected_post = fetch_posts_data(sso)
                if selected_post:
                    follow_user_id = selected_post[1]  # 假设使用帖子的发布者ID作为关注对象
                    gz_user(sso, follow_user_id)
                else:
                    print("未能获取帖子数据，无法执行关注操作。")
            elif task_name == "参与讨论":
                selected_post = fetch_posts_data(sso)
                if selected_post:
                    post_id = selected_post[0]  # 假设列表的第一个元素是 post_id
                    cytl(sso, post_id)
                else:
                    print("未能获取帖子数据，无法参与讨论。")
            elif task_name == "给主播留言":
                selected_anchor = zb_list(sso)
                if selected_anchor:
                    circle_id, related_id = selected_anchor
                    add_comment(sso, circle_id, related_id, task_id)
                else:
                    print("未能获取主播数据，无法执行留言操作。")

            # 在任务之间停止 1 到 3 秒
            time.sleep(random.randint(1, 2))

        return response_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except ValueError:
        print("响应内容不是有效的 JSON 格式")
        return None

def fx_xx(sso):  # 分享心喜
    headers = create_headers(sso)
    urlfx = BASE_URL + 'dailyTask/share'
    try:
        response = requests.get(urlfx, headers=headers)
        if response.status_code == 200:
            response_data = response.json()  # 解析 JSON 响应
            #print("分享心喜完整响应内容: ", response_data)

            # 检查 data 是否存在
            if response_data.get('data'):
                task_name = response_data['data'].get('taskName', '未知任务')
                single_reward = response_data['data'].get('singleReward', '未知奖励')
                print(f"完成🎉 {task_name},🥂奖励: {single_reward}")
                print()
            else:
                #print("分享心喜任务完成，但未获取到详细信息。")
                print("🤡🤡分享心喜任务🤡🤡。")
            time.sleep(3)
        else:
            print(f"请求失败，状态码：{response.status_code}, 响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

def sign_dk(sso, task_id):  # 签到打卡
    sign_in_url = BASE_URL + f'sign/in?dailyTaskId={task_id}'  # 构造签到 URL
    headers = create_headers(sso)  # 使用 create_headers 函数创建 headers
    try:
        response = requests.get(sign_in_url, headers=headers)  # 使用 GET 方法签到
        if response.status_code == 200:
            response_data = response.json()
            #print(f"签到成功！响应内容: {response.text}")

            # 在访问 taskResult 之前检查它是否存在
            if response_data.get('data') and response_data['data'].get('taskResult'):
                task_name = response_data['data']['taskResult'].get('taskName', '未知任务')
                single_reward = response_data['data']['taskResult'].get('singleReward', '未知奖励')
                print(f"  🎉: {task_name}, 奖励: {single_reward}")
                print()
            else:
                print("签到成功，但未获取到任务结果。")
            return True  # 签到成功
        else:
            print(f"签到失败，状态码：{response.status_code}, 响应内容: {response.text}")
            return False  # 签到失败
    except requests.exceptions.RequestException as e:
        print(f"签到请求失败: {e}")
        return False  # 请求失败


def xysp(sso):  # 想要商品
    headers = {
        'sso': sso,
        'Host': 'cdn-api.xinc818.com'  # 注意这里的 Host
    }

    random_page_num = random.randint(1, 15)
    url_desire_goods = f'https://cdn-api.xinc818.com/mini/integralGoods?orderField=sort&orderScheme=DESC&pageSize=10&pageNum={random_page_num}'

    try:
        response = requests.get(url_desire_goods, headers=headers)
        print(f"随机选择的页数为: {random_page_num}")

        if response.status_code == 200:
            response_json = response.json()
            goods_list = response_json.get('data', {}).get('list', [])
            if goods_list:
                random_id = random.choice(goods_list)['id']
                print("随机选取的商品ID:", random_id)

                headers['Host'] = 'api.xinc818.com'  # 更新headers为 api.xinc818.com
                url_specific_good = f'https://api.xinc818.com/mini/integralGoods/{random_id}?type'
                response_specific = requests.get(url_specific_good, headers=headers)

                if response_specific.status_code == 200:
                    response_specific_json = response_specific.json()
                    outer_id = response_specific_json.get('data', {}).get('outerId', '')
                    print(f"提取的outerId: {outer_id}")

                    # 新的POST请求
                    url_submit = 'https://api.xinc818.com/mini/live/likeLiveItem'
                    data = {
                        "isLike": True,
                        "dailyTaskId": 20,
                        "productId": outer_id
                    }
                    print(data)
                    submit_response = requests.post(url_submit, headers=headers, json=data)

                    if submit_response.status_code == 200 and submit_response.headers.get('Content-Type') == 'application/json':
                        response_data = submit_response.json()
                        #print(submit_response.json())
                        if response_data is None:
                            print(f"响应的JSON数据为空，原始响应内容: {submit_response.text}")
                            return  # 退出当前任务
                        if response_data.get("data"):
                            task_name = response_data["data"].get("taskName", "未知任务")
                            single_reward = response_data["data"].get("singleReward", 0)
                            print(f"  🎉: {task_name}，奖励: {single_reward}")
                        else:
                            print("想要商品 请求成功但未完成任务，响应码或数据内容不正确")
                            return  # 退出当前任务
                    else:
                        print(f"POST请求失败，状态码：{submit_response.status_code}, 响应内容: {submit_response.text}")
                        return  # 退出当前任务

            else:
                print("商品列表为空，跳过当前账号")
                return  # 退出当前任务
        else:
            print(f"获取商品列表失败，状态码：{response.status_code}, 响应内容: {response.text}")
            return  # 退出当前任务

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return  # 退出当前任务


def dzp_cj(sso, task_id):#大转盘抽奖
    try:
        headers = create_headers(sso)

        # 获取抽奖活动列表
        activity_list_url = BASE_URL + 'lottery/list'
        activity_response = requests.get(activity_list_url, headers=headers)
        if activity_response.status_code != 200:
            print('获取活动列表失败，状态码：', activity_response.status_code)
            return
        activity_data = activity_response.json()

        # 查找“幸运大转盘抽奖”的id
        activity_id = None
        for activity in activity_data['data']:
            if activity['activityName'] == "幸运大转盘抽奖":
                activity_id = activity['id']
                break
        
        if activity_id is None:
            print("没有找到‘幸运大转盘抽奖’活动")
            return
        print(f"找到‘幸运大转盘抽奖’活动, ID: {activity_id}")

        # 检查抽奖次数
        lottery_url = BASE_URL + f'lottery/{activity_id}/freeNum'
        lottery_response = requests.get(lottery_url, headers=headers)
        if lottery_response.status_code != 200:
            print('检查抽奖次数失败，状态码：', lottery_response.status_code)
            return
        lottery_data = lottery_response.json()
        print('抽奖次数：', lottery_data['data'])

        if lottery_data['data'] == 0:
            print("没有抽奖机会，过程跳过。")
            return

        # 获取用户id
        user_url = BASE_URL + 'user'
        user_response = requests.get(user_url, headers=headers)
        if user_response.status_code != 200:
            print("获取用户ID失败，状态码： ", user_response.status_code)       
            return
        user_data = user_response.json()
        user_id = user_data['data']['id']
        print(f"用户ID获取成功: {user_id}")

        # 抽奖
        lottery_draw_url = BASE_URL + 'lottery/draw'
        payload = {
            "activityId": activity_id,
            "batch": False,
            "isIntegral": False,
            "userId": user_id,
            "dailyTaskId": task_id  # 使用变量task_id作为dailyTaskId
        }
        #print(payload)
        lottery_draw_response = requests.post(lottery_draw_url, headers=headers, json=payload)
        if lottery_draw_response.status_code == 200:
            #print("抽奖成功!")
            lottery_result = lottery_draw_response.json()
            lottery_result_list = lottery_result['data']['lotteryResult']
            if lottery_result_list:
                prize_name = lottery_result_list[0].get('prizeName', '未知奖品')
                print("中奖奖品🎉：", prize_name)
            else:
                print("未获取到抽奖结果")
        else:
            print("抽奖失败，状态码：", lottery_draw_response.status_code)

        time.sleep(3)

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

def ll_sp(sso, task_id):  # 浏览商品30秒
    browse_url = BASE_URL + f'dailyTask/browseGoods/{task_id}'
    headers = create_headers(sso)  
    print(browse_url)
    try:
        # 模拟浏览前的准备请求
        pre_browse_response = requests.get(browse_url, headers=headers)
        if pre_browse_response.status_code != 200:
            print(f"浏览前的请求失败，状态码：{pre_browse_response.status_code}")
            return False

        # 模拟用户浏览30秒
        time.sleep(3)  # 注意这里应该是30秒，但现在是3秒

        # 模拟浏览后的完成请求
        post_browse_response = requests.get(browse_url, headers=headers)
        if post_browse_response.status_code == 200:
            print("成功模拟浏览商品30秒")
            # 打印响应内容，如果需要
            print(post_browse_response.json())  # 更正的行
            print(f"浏览后的响应内容: {post_browse_response.text}")
            return True
        else:
            print(f"浏览后的请求失败，状态码：{post_browse_response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return False

def fetch_posts_data(sso):#获取帖子数据并提取 点赞用户id 和 关注用户publisherId，然后随机选择一个
    url = "https://cdn-api.xinc818.com/mini/posts/sorts?sortType=SPAM&pageNum=1&pageSize=10&groupClassId=0"
    headers = {
        "Host": "cdn-api.xinc818.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "sso": sso
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data', {}).get('list', [])
            extracted_data = [(item['id'], item['publisherId']) for item in data]

            if extracted_data:
                # 随机选择一个帖子
                selected_post = random.choice(extracted_data)
                return selected_post
            else:
                print("没有找到帖子数据")
                return None
        else:
            print(f"请求失败，状态码：{response.status_code}, 响应内容: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None

def like_post(sso, post_id):  # 点赞用户
    url = BASE_URL + "posts/like"  
    headers = create_headers(sso)  
    payload = {
        "postsId": str(post_id),  
        "decision": True
    }

    try:
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"💨成功点赞帖子，帖子ID: {post_id}")
            #print(f"点赞帖子 完整响应内容: {response.text}") 
            response_json = response.json()

            # 检查 response_json['data'] 是否存在
            if response_json.get('data'):
                task_name = response_json['data'].get('taskName', '未知任务')
                single_reward = response_json['data'].get('singleReward', '未知奖励')
                print(f"任务名称: {task_name}, 单次奖励: {single_reward}")
                print()
            else:
                #print("点赞成功，但未获取到任务详情。")
                #print("👻👻点赞👻👻。")
                print()
        else:
            print(f"点赞失败，状态码：{response.status_code}")
            print(f"完整响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")


def gz_user(sso, follow_user_id):  # 关注用户
    url = BASE_URL + "user/follow"  
    headers = create_headers(sso)  
    payload = {
        "decision": True,
        "followUserId": follow_user_id
    }

    try:
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"成功关注💗用户，用户ID: {follow_user_id}")
            #print(f"完整响应内容: {response.text}")  # 打印完整的响应内容

            response_json = response.json()

            # 检查 response_json['data'] 是否存在
            if response_json.get('data'):
                task_name = response_json['data'].get('taskName', '未知任务')
                single_reward = response_json['data'].get('singleReward', '未知奖励')
                print(f"  🎉: {task_name}, 奖励: {single_reward}")
                print()
            else:
                #print("关注成功，但未获取到任务详情。")
                print()
        else:
            print(f"关注用户失败，状态码：{response.status_code}")
            print(f"完整响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")


def user_info(sso):#"获取用户信息ID   积分
    url = BASE_URL + "user"  
    headers = create_headers(sso)  
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            user_data = response_json.get('data', {})
            user_id = user_data.get('id', '')
            integral = user_data.get('integral', '')
            history_integral = user_data.get('historyIntegral', '')

            print(f"用户ID: {user_id}, 当前积分: {integral}, 历史积分: {history_integral}")
            
            return user_id  # 返回用户ID
        else:
            print(f"获取用户信息失败，状态码：{response.status_code}, 响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
    return None  # 如果请求失败或异常，返回None

def cytl(sso, post_id):  # "参与讨论，对指定帖子发表随机评论
    url = BASE_URL + "postsComments"
    headers = create_headers(sso)
    user_info_result = user_info(sso)  # 获取用户信息的结果

    # 定义一个评论内容的字典
    comments = [
        "非常好！",
        "我同意！",
        "这确实很重要。",
        "我从这个评论学到了很多。",
        "加油，",
        "为你打call！",
        "今天也要加油哦！",
        "很有见地！",
        "太精彩了！",
        "赞同这个观点。",
        "好好",
        "真的很棒！",
        "这个我喜欢！",
        "太赞了！",
        "很有帮助！",
        "这是我见过的最好的观点！",
        "太有创意了！",
        "这让我思考良多。",
        "绝对同意！",
        "讲得太好了！",
        "这才是重点！",
        "我刚想到这个！",
        "太同意了！",
        "这解释得太清楚了！",
        "这个分析很到位！",
        "你抓住了核心！",
        "这个角度很独特！",
        "没想到这样的观点，太棒了！"
        "情感丰富，真实感人！",
        "每次看到你的评论都很期待！",
        "你的观点总能给人启发！",
        "你的评论总是那么独到！",
        "期待你更多的分享！",
        "你的观点太有深度了！",
        "每次看到你的评论都很受益！",
        "这分析太透彻了！",
        "你的评论总能点亮我的思考！",
        "看到你的评论，我的心情都好了！"
        "这让我看到了不同的视角！",
        "每个人的看法都很有意思！",
        "太有创造力了，我喜欢！",
        "这个讨论很有价值！",
        "你的见解让人耳目一新！",
        "这是一个很棒的开始！",
        "从你的评论中学到了很多！",
        "你的想法很有启发性！",
        "这个观点很有趣，赞一个！",
        "你的理解深度让我佩服！",
        "这确实是个好问题，值得探讨。",
        "谢谢分享，我受益匪浅！",
        "这种观点很难得，很欣赏！",
        "你的分析很到位，赞同！",
        "这样的讨论太精彩了，期待更多！"
    ]
    content = random.choice(comments)  # 随机选择一个评论内容

    if user_info_result:
        user_id = user_info_result[0]  # 仅提取 user_id
        payload = {
            "customizeImages": [],
            "content": content,
            "postsId": post_id,
            "publisherId": user_id,  # 使用提取的 user_id
            "floorId": "",
            "voice": ""
        }
        #print(payload)
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print(f"🙋参与讨论，帖子ID: {post_id}, 内容: '{content}'")
                # 解析响应内容以获取taskName和singleReward
                response_json = response.json()
                #print("参与讨论完整响应内容: ", response_json)
                task_name = response_json.get('data', {}).get('taskResult', {}).get('taskName', '')
                single_reward = response_json.get('data', {}).get('taskResult', {}).get('singleReward', '')
                print(f"完成🎉{task_name}, 奖励: {single_reward}🔝🔝🔝")
                print()
            else:
                print(f"参与讨论失败，状态码：{response.status_code}, 响应内容: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
    else:
        print("未能获取用户ID，无法参与讨论。")

def zb_list(sso):  # 主播列表
    url = BASE_URL + "groups/defaultGroupList"
    headers = create_headers(sso)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            group_list = response.json()

            # 提取所有主播的id和associatedAnchorId
            anchors = [(group.get('id'), group.get('associatedAnchorId')) for group in group_list.get('data', [])]

            # 随机选择一个主播
            if anchors:
                selected_anchor = random.choice(anchors)
                group_id, associated_anchor_id = selected_anchor
                #print(f"随机选取的群组ID: {group_id}, 关联主播ID: {associated_anchor_id}")
                return group_id, associated_anchor_id  # 返回随机选取的群组ID和关联主播ID
            else:
                print("没有可用的主播列表。")
                return None, None
        else:
            print(f"获取主播列表失败，状态码：{response.status_code}, 响应内容: {response.text}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None, None

def add_comment(sso, circle_id, related_id, daily_task_id):#给主播留言
    """在指定圈子中对指定主播添加评论"""
    url = BASE_URL + "anchorComment/addComment"
    headers = create_headers(sso)

    # 预定义的评论列表
    comments = [
        "加油，我们支持你！",
        "你是最棒的！",
        "永远支持你！",
        "我们在这里，永远爱你！",
        "你总是能给我们带来欢笑！",
        "你的直播太棒了！",
        "你总是能够打动我们！",
        "你的笑容真的很治愈！",
        "我们是你坚强的后盾！",
        "为你打call！",
        "今天也要加油哦！",
        "一直在你身后支持你！",
        "你是最亮的星！",
        "很高兴认识你！",
        "你的努力我们都看到了！",
        "每一次直播都是一次享受！",
        "你的粉丝们都在这里！",
        "继续前进，我们会一直在这里！",
        "你总是那么有活力！",
        "我们看到的不只是努力的你！",
        "每次看你的直播都很开心！",
        "你的每一次努力我们都看在眼里！",
        "你的直播总能给我带来好心情！",
        "你的才华无人能及！",
        "你的直播是我一天中最期待的时刻！",
        "你的魅力真的无法抗拒！",
        "在你的直播中总能找到快乐！",
        "你的每个瞬间都充满了惊喜！",
        "你的努力值得每一份赞赏！",
        "你的存在让这个平台更加精彩！",
        "期待你的每一次直播！",
        "你的每个直播都值得反复观看！",
        "你总是能带给我们满满的正能量！",
        "你的每一次分享都很有价值！",
        "每次看你的直播都能学到很多东西！",
        "你的直播里总有无限的乐趣！",
        "你的直播总是那么充满活力！",
        "你的直播是我们的快乐源泉！",
        "感谢你带来这么多美好的直播时光！",
        "你的每一场直播都是一场视听盛宴！",
        "你的每场直播都是我们的心灵鸡汤！",
        "看到你的努力，我们都非常感动！",
        "你的笑声太迷人了，每次听都很开心！",
        "你的才华横溢，每场直播都令人期待！",
        "感谢你总是带给我们这么多正能量！",
        "你的每一次直播都给我留下深刻印象！",
        "你是我们的超级明星，永远支持你！",
        "你在直播中的每一刻都是那么的真实可爱！",
        "你的直播是我一天中最放松的时光！",
        "每次看到你，都觉得世界变得更美好了！",
        "你的直播充满了温暖和力量！",
        "你的存在就是我们的幸运！",
        "你的直播总是那么富有创造力和想象力！",
        "你是那么的不同凡响，总能带来惊喜！",
        "你的直播是我的精神食粮！",
        "看着你的成长和进步，我们都为你感到骄傲！",
        "你总是那么的充满魅力和活力！",
        "你的每一次直播都是一次美好的旅行！",
        "你的存在让我们的生活充满了乐趣！",
        "你是我们心中的英雄，永远支持你！",    
        "你的直播总是能点亮我们的生活！",
        "每次听你说话都特别有感染力！",
        "你的直播总是那么有趣，让人忍不住一直看！",
        "你的每一次表演都是那么精彩，无法挪开眼！",
        "你的直播总是给我带来好心情，谢谢你！",
        "每次看你直播都有新的收获，真的很棒！",
        "你的直播里总有无尽的正能量，真的很喜欢！",
        "你的直播总是那么温馨，感觉像回到家一样！",
        "你是我们的快乐小天使，每次看到你都特别开心！",
        "你的每一次直播都是我们的期待！",
        "你的直播中总有许多惊喜，让人意犹未尽！",
        "每次看你的直播都能感受到你的用心！",
        "你的直播就像一股清泉，沁人心脾！",
        "你的每一次直播都是我们的精神食粮！",
        "你的直播总能带给我不一样的感受，太棒了！",
        "你的直播充满了智慧和趣味，真是太有才了！",
        "你的直播总是能给我们带来欢乐和知识，感谢你！",
        "每次看你直播都有种被治愈的感觉！",
        "你的直播总是那么充满活力，真是太赞了！",
        "你的直播给了我们很多快乐，永远支持你！",           
    ]

    # 随机选择一个评论内容
    content = random.choice(comments)

    payload = {
        "content": content,
        "circleId": circle_id,
        "relatedId": related_id,
        "contentType": 0,  # contentType固定为0
        "dailyTaskId": daily_task_id,
        "topCommentId": 0,  # topCommentId固定为0
    }
    #print(payload)  # 打印请求内容
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            print(f"💬评论成功，圈子ID: {circle_id}, 主播ID: {related_id}, ✍️: '{content}'")
            #print(f"评论 完整响应内容: {response_data}")  # 打印完整的响应内容

            # 检查 response_data['data'] 和 response_data['data']['taskResult'] 是否存在
            if response_data.get('data') and response_data['data'].get('taskResult'):
                task_name = response_data['data']['taskResult'].get('taskName', '未知任务')
                single_reward = response_data['data']['taskResult'].get('singleReward', '未知奖励')
                print(f"  🎉: {task_name}, 奖励: {single_reward}")
                print()
            else:
                #print("评论成功，但未获取到任务详情。")
                print()
        else:
            print(f"评论失败，状态码：{response.status_code}, 响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")

def user_info(sso):
    url = BASE_URL + "user"  
    headers = create_headers(sso)  
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            user_data = response_json.get('data', {})
            if user_data is None:  # 检查 user_data 是否为 None
                #print(f"未能获取到 {sso} 的用户数据。")
                return None

            user_id = user_data.get('id', '')
            integral = user_data.get('integral', '')
            history_integral = user_data.get('historyIntegral', '')

            #print(f"用户ID: {user_id}, 当前积分: {integral}, 历史积分: {history_integral}")
            
            return user_id, integral, history_integral  # 以元组形式返回
        else:
            print(f"获取用户信息失败，状态码：{response.status_code}, 响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")

    return None  # 如果请求失败或异常，返回None


def fetch_hitokoto(): #一言
    url_hitokoto = 'https://v1.hitokoto.cn/'
    # 设置请求参数
    params = {
        'c': 'k',         # 类型为哲学
        'min_length': 10  # 设置返回句子的最小长度为 10
    }
    try:
        response_hitokoto = requests.get(url_hitokoto, params=params)
        if response_hitokoto.status_code == 200:
            data = response_hitokoto.json()
            return data.get('hitokoto')
        else:
            # 主要 API 请求失败，尝试备用 API
            return fetch_hitokoto_backup()
    except requests.exceptions.RequestException:
        # 主要 API 请求异常，尝试备用 API
        return fetch_hitokoto_backup()

def fetch_hitokoto_backup(): #  备用一言
    url_backup = 'https://api.7585.net.cn/yan/api.php?charset=utf-8'
    try:
        response_backup = requests.get(url_backup)
        if response_backup.status_code == 200:
            return response_backup.text.strip()  # 返回备用 API 的响应内容
        else:
            return f"备用API请求失败，状态码：{response_backup.status_code}"
    except requests.exceptions.RequestException as e:
        return f"备用API请求异常: {e}"

def rw_post(sso, content, task_id):  # 发帖
    headers = create_headers(sso)
    url = BASE_URL + "posts"
    sid = int(time.time() * 1000)  # 生成时间戳

    data = {
        "topicNames": [],
        "content": content,
        "groupId": 0,
        "groupClassifyId": 0,
        "attachments": [],
        "voteType": 0,
        "commentType": "0",
        "dailyTaskId": task_id,
        "platform": "android",
        "sid": sid
    }
    #print(data)

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_json = response.json()
            print(f"💬发帖成功，✍️{content}, 任务ID: {task_id}, 时间戳: '{sid}'")

            # 检查 response_json['data'] 是否存在
            if response_json.get('data'):
                task_name = response_json['data'].get('taskName', '未知任务')
                single_reward = response_json['data'].get('singleReward', '未知奖励')
                print(f"  🎉: {task_name}, 单次奖励: {single_reward}")
                print()
            else:
                #print("发帖成功，但未获取到任务详情。")
                print()
            #print(f"发帖完整响应内容: {response.text}")
        else:
            print(f"发帖请求失败，状态码：{response.status_code}")
            print(f"完整响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")


def hqjljl(sso):  # 奖励记录 积分
    """获取奖励记录，并返回当天的积分总和"""
    records_url = BASE_URL + f'user/integralRecord?pageNum=1&pageSize=20'
    headers = create_headers(sso)  # 使用 create_headers 函数创建 headers

    try:
        response = requests.get(records_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            total_points_today = 0
            today = datetime.now(timezone(timedelta(hours=8))).date()  # 获取当前日期

            for record in data.get('data', {}).get('list', []):
                # 提取 remark、changeValue 和 changeTime
                remark = record.get('remark')
                change_value = record.get('changeValue')
                change_time = record.get('changeTime')

                # 将时间戳转换为北京时间
                beijing_time = datetime.fromtimestamp(change_time / 1000, timezone(timedelta(hours=8)))
                formatted_time = beijing_time.strftime('%Y-%m-%d %H:%M:%S')

                # 判断记录是否为当天的
                if beijing_time.date() == today:
                    total_points_today += change_value

                # 在循环内部打印每条记录的详细信息
                #print(f"任务: {remark}, 积分: {change_value}, 时间: {formatted_time}")

            print(f"今日积分: {total_points_today}")

            return total_points_today  # 返回当天的积分总和

        else:
            print(f"获取奖励记录失败，状态码：{response.status_code}, 响应内容: {response.text}")
            return None  # 获取失败时返回 None

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None  # 请求异常时返回 None


#本地测试用 

os.environ['XSSONF1'] = '''
Wmeimob_eyJ0ebGciOiJIUzI1NiJ9.eyJzdWIiOiIx#大号
'''




class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()  # 确保及时输出

    def flush(self):
        for file in self.files:
            file.flush()
# 主函数
def main():
    var_name = 'XSSONF'
    tokens = get_env_variable(var_name)
    if not tokens:
        return

    yxsl = len(tokens)  # 账号总数



    # 首先对每个账号运行 rwlb(sso)
    for i, token in enumerate(tokens):
        parts = token.split('#')
        if len(parts) < 2:
            print("令牌格式不正确。跳过处理。")
            continue

        sso = parts[0]
        account_no = parts[1]

        print(f'------账号 {i+1}/{yxsl} {account_no} -------')
        rwlb(sso)  # 任务列表
    # 设置Tee类实例并开始捕获输出
    original_stdout = sys.stdout  # 保存原始stdout
    string_io = io.StringIO()     # 创建StringIO对象以捕获输出
    sys.stdout = Tee(sys.stdout, string_io)  # 将stdout重定向

    # 所有账号运行完 rwlb(sso) 后再统一运行 hqjljl(sso) 和 user_info(sso)

    for i, token in enumerate(tokens):
        parts = token.split('#')
        if len(parts) < 2:
            continue  # 如果令牌格式不正确，继续下一个

        sso = parts[0]
        account_no = parts[1]

        print(f'---账号{i+1}/{yxsl} {account_no}---')
        user_info_result = user_info(sso)  # 获取 user_info 函数的返回值
        if user_info_result is None:
            print(f"由于某些原因/过期/不正确 跳过此账号。")
            continue  # 跳过此次循环的剩余部分

        # 解包 user_info 函数返回的元组
        user_id, integral, history_integral = user_info_result
        print(f"🎊当前积分: {integral}, 历史积分: {history_integral}")  # 打印积分信息

        hqjljl(sso)  # 处理奖励
    # 捕获完成后，重置sys.stdout并获取内容
    sys.stdout = original_stdout  # 重置stdout
    output_content = string_io.getvalue()  # 获取捕获的输出

    # 如果需要发送通知
    if enable_notification == 1:
        send("心喜-通知", output_content)

if __name__ == "__main__":
    main()