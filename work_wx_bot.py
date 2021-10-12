# coding=UTF-8  
import requests
import json
import os
import sys
import getopt

"""
使用说明：
请在企微里拉好机器人并获得对应key后再使用该脚本
使用方法为运行该脚本时携带对应的key、发送文本、发送文件相对路径
或直接调用
如：
python3 company_wx_bot.py -k [key] -t [text] -f[file]
python3 company_wx_bot.py -k [key] -t [text]
python3 company_wx_bot.py -k [key] -f [file]
其中-k参数为必填项
-t参数为要发送的文本，可选填
-f参数为要发送的文件的相对路径，可选填
"""

def robot(key, data):
    txt = sys.argv[1:]
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="+key
    headers = headers = {'content-type': 'application/json'}
    r = requests.post(webhook, headers=headers, data=json.dumps(data))
    r.encoding = 'uft-8'
    return r.text

def bot_push(key, data):
    try:
        res = robot(key, data)
        # print('webhook发出完毕:',res)
        return res
    except Exception as e:
        print(e)

def bot_push_text(key, msg):
    # 发送文本消息
    webhook_data = {
        "msgtype":"text",
        "text":{
            "content": msg
        }

    }
    bot_push(key, webhook_data)

    return None
def bot_upload_file(key, file_path):
    # 上传文件获得media_id，请注意上传文件需大于5个字节且小于20MB
    if os.path.getsize(file_path)>20971520:
        bot_push_text("文件过大,请自行去服务器提取")
        return 0
    webhook_file = key+'&type=file'  # 上传文件接口地址
    data = {'file': open(file_path, 'rb')}  # post jason
    r = requests.post(url=webhook_file, files=data)  # post 请求上传文件
    json_res = r.json()  # 返回转为json
    print(json_res)
    try:
        media_id = json_res['media_id']  # 提取返回ID
        return media_id
    except Exception as e:
        print(e)


def bot_push_file(key, file):
    # 发送文件
    media_id = bot_upload_file(key, file)
    webhook_data = {
        "msgtype":"file",
        "file":{
            "media_id":media_id
        }
    }
    bot_push(key, webhook_data)

def input():
    # 获取输入参数
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "k:t:f:")
        if opts[0][0] == '-k':
            key = opts[0][1]
            for opt, arg in opts:
                if opt in ['-t']:
                    bot_push_text(key, arg)
                elif opt in ['-f']:
                    bot_push_file(str(key, arg))
        else:
            print("需要输入key！")
    except:
        print("Error")
        print("请检查您的参数确认输入无误")

if __name__ =='__main__':
    input()


