"""
1. 书亦烧仙草签到 抓包scrm-prod.shuyi.org.cn域名请求头里的auth
   脚本仅供学习交流使用, 请在下载后24h内删除
2. cron 以防cor识别出错每天运行两次左右
3. ddddocr搭建方法https://github.com/sml2h3/ocr_api_server #如果脚本里的失效请自行搭建
"""
import requests, base64, json, time, os

try:
    from Crypto.Cipher import AES
except:
    print(
        "\n未检测到pycryptodome\n需要Python依赖里安装pycryptodome\n安装失败先linux依赖里安装gcc、python3-dev、libc-dev\n如果还是失败,重启容器,或者重启docker就能解决")
    exit(0)

def setHeaders(i):
    headers = {
        "auth": cookies[i],
        "hostname": "scrm-prod.shuyi.org.cn",
        "content-type": "application/json",
        "host": "scrm-prod.shuyi.org.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; V2203A Build/SP1A.210812.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5023 MMWEBSDK/20221012 MMWEBID/1571 MicroMessenger/8.0.30.2260(0x28001E55) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android"
    }
    return headers

cookies = []
try:
    cookies = os.environ["sysxc_auth"].split("&")
    if len(os.environ["sysxc_auth"]) > 0:
        print("已获取并使用Env环境Cookie\n声明：本脚本为学习python，请勿用于非法用途\n")
            

except:
    print(
        "【提示】请先获取微信小程序[书亦烧仙草]请求头中的auth\n环境变量添加: sysxc_auth \n吹牛群：https://t.me/+yHXoi9YH_ZcyMjJl")
    exit(3)

def getVCode(headers):
    """获取滑块图片"""
    data = {
        "captchaType": "blockPuzzle",
        "clientUid": "slider-6292e85b-e871-4abd-89df-4d97709c6e0c",
        "ts": int(time.time() * 1000)
    }
    url = 'https://scrm-prod.shuyi.org.cn/saas-gateway/api/agg-trade/v1/signIn/getVCode'
    response = requests.post(url, json=data, headers=headers)
    return response.json()



def ocr(tg,bg):
    """使用自有ocr识别滑块坐标"""
    url = 'http://47.120.9.145:3001/slide/match/b64/json'
    jsonstr = json.dumps({'target_img': tg, 'bg_img': bg})
    response = requests.post(url, data=base64.b64encode(jsonstr.encode()).decode())
    return response.json()


'''
采用AES对称加密算法
'''

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def aesEncrypt(key, data):
    '''
    AES的ECB模式加密方法
    :param key: 密钥
    :param data:被加密字符串（明文）
    :return:密文
    '''
    key = key.encode('utf8')
    # 字符串补位
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf8')
    return enctext


def aesDecrypt(key, data):
    '''
    :param key: 密钥
    :param data: 加密后的数据（密文）
    :return:明文
    '''
    key = key.encode('utf8')
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)

    # 去补位
    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted


def checkVCode(pointJson, token):
    """验证"""
    try:
        data = {
            "captchaType": "blockPuzzle",
            "pointJson": pointJson,
            "token": token
        }
        url = 'https://scrm-prod.shuyi.org.cn/saas-gateway/api/agg-trade/v1/signIn/checkVCode'
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        # print(result)
        resultCode = result['resultCode']
        if resultCode == '0000':
            print('校验结果：', '成功')
        else:
            print('校验结果:', result['resultMsg'])

    except Exception as err:
        print(err)


def check_sign(pointJson):
    """签到"""
    try:
        data = {
            "captchaVerification": pointJson
        }
        url = 'https://scrm-prod.shuyi.org.cn/saas-gateway/api/agg-trade/v1/signIn/insertSignInV3'
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        resultCode = result['resultCode']
        if resultCode == '0':
            print("签到结果: 第{result['data']['days']天} 获得{result['data']['pointRewardNum']积分}")
        else:
            print('签到结果：', result['resultMsg'])
    except Exception as err:
        print(err)

def main():
    result = getVCode(headers)
    bg = result['data']['originalImageBase64']
    tg = result['data']['jigsawImageBase64']
    key = result['data']['secretKey']
    token = result['data']['token']
    print('本次口令为：', token)
    print('本次密钥为：', key)
    time.sleep(1.5)
    print("--------------------识别滑块--------------------")
    result = ocr(tg,bg)
    res = result['result']['target']
    d = (res[0])
    print('滑动距离为：', d)
    print("--------------------执行算法--------------------")
    aes_str = json.dumps({"x": d, "y": 5})
    data = aes_str.replace(' ', '')
    print('加密前：', data)
    time.sleep(1.5)
    ecdata = aesEncrypt(key, data)
    aesDecrypt(key, ecdata)
    pointJson = aesEncrypt(key, data)
    print('加密后：', pointJson)
    print("--------------------校验滑块--------------------")
    checkVCode(pointJson, token)
    print("--------------------开始签到--------------------")
    str = (token + '---' + aes_str)
    data = str.replace(' ', '')
    ecdata = aesEncrypt(key, data)
    aesDecrypt(key, ecdata)
    pointJson = aesEncrypt(key, data)
    time.sleep(0.5)
    check_sign(pointJson)

if __name__ == '__main__':

    print("--------------------任务开始--------------------")
    for i in range(len(cookies)):
        print(f"\n开始第{i + 1}个账号")
        headers = setHeaders(i)
        main()

