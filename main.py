import requests#http请求
import json#json数据处理
import traceback#错误捕获
import time#延时
import websocket#ws接口链接
import base64#请求体编码
import threading
from pygments import highlight#高亮
from pygments.lexers import JsonLexer#高亮
from pygments.formatters import TerminalFormatter#高亮
from colorama import init, Fore, Back, Style#高亮

lingpai='0f2de7ac66727cd9fcec1ee11a18ad1ff314388d1c'#bot的token
bot_id='448828939389894656'#bot的id
websocket_url='wss://gateway-bot.fanbook.mobi/websocket'#websocket主机
requests_url='https://a1.fanbook.mobi/api/bot/'#fb bot api主机
post_headers={'Content-Type':'application/json'}#post请求头

init(autoreset=True)    #  初始化，并且设置颜色设置自动恢复
def addmsg(msg, color="white"):#终端彩色提示信息
    if color == "white":#默认
        print(msg)
    elif color == "red":#错误文本
        print("\033[31m" + msg + "\033[39m")
    elif color == "yellow":#警告文本
        print("\033[33m" + msg + "\033[39m")
    elif color == "green":#成功文本
        print("\033[32m" + msg + "\033[39m")
    elif color == "aqua":#绿底提示文本
        print("\033[36m" + msg + "\033[39m")

def colorprint(smg2,pcolor):#拓展的终端颜色（需要装colorama）
    if pcolor=='red':#红字
      print(Fore.RED + smg2)
    elif pcolor=='bandg':#蓝字
      print(Back.GREEN + smg2)
    elif pcolor=='d':
      print(Style.DIM + smg2)
    # 如果未设置autoreset=True，需要使用如下代码重置终端颜色为初始设置
    #print(Fore.RESET + Back.RESET + Style.RESET_ALL)  autoreset=True
    
def colorize_json(smg2,pcolor=''):#格式化并高亮json字符串
    json_data=smg2
    try:
        parsed_json = json.loads(json_data)  # 解析JSON数据
        formatted_json = json.dumps(parsed_json, indent=4)  # 格式化JSON数据

        # 使用Pygments库进行语法高亮
        colored_json = highlight(formatted_json, JsonLexer(), TerminalFormatter())

        print(colored_json)
    except json.JSONDecodeError as e:#如果解析失败，则直接输出原始字符串
        print(json_data)

def send_data_to_fb(chatid=0,biaoti="标题",ik=[],text='文本',type="card") -> str:#发送数据
    """
    发送消息
    Args:
        chatid (int): 频道id
        biaoti (str): 标题
        ik (list): 键盘列表
        text (str): 正文文本
        type (str): 类型，card(消息卡片)或text(文本)
        
    Returns:
        str: 返回json字符串
    """
    if biaoti=='获取成功':
        color='#11A675'
    else:
        color='FF6100'
    url = f"https://a1.fanbook.mobi/api/bot/{lingpai}/sendMessage"
    if type=="card":
        text1="{\"width\":null,\"height\":null,\"data\":\"{\\\"tag\\\":\\\"column\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"12,7\\\",\\\"child\\\":{\\\"tag\\\":\\\"text\\\",\\\"data\\\":\\\""+biaoti+"\\\",\\\"style\\\":{\\\"color\\\":\\\""+color+"\\\",\\\"fontSize\\\":16,\\\"fontWeight\\\":\\\"medium\\\"}},\\\"backgroundColor\\\":\\\"ddeeff\\\"},{\\\"tag\\\":\\\"container\\\",\\\"child\\\":{\\\"tag\\\":\\\"column\\\",\\\"padding\\\":\\\"12\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"0,8,0,0\\\",\\\"child\\\":{\\\"tag\\\":\\\"markdown\\\",\\\"data\\\":\\\""+text+"\\\"}}]},\\\"backgroundColor\\\":\\\"ffffff\\\"}],\\\"crossAxisAlignment\\\":\\\"stretch\\\"}\",\"notification\":null,\"come_from_icon\":null,\"come_from_name\":null,\"template\":null,\"no_seat_toast\":null,\"type\":\"messageCard\"}"
        pm="Fanbook"
    else:
        text1=text
        pm=None
    payload = json.dumps({
    "chat_id": int(chatid),
    "text": text1,
    "parse_mode": pm,
    "reply_markup": {
        "inline_keyboard": [ik]
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    
    
def edit_data_to_fb(chatid:int,biaoti:str,ik:list,text:str,messageid:int) -> str:#发送数据
    """
    修改消息
    Args:
        chatid (int): 频道id
        biaoti (str): 标题
        ik (list): 键盘列表
        text (str): 正文文本
        messageid (int): 消息id
    Returns:
        str: 返回json字符串
    """
    url = f"https://a1.fanbook.mobi/api/bot/{lingpai}/editMessageText"
    if biaoti=='获取成功':
        color='#11A675'
    else:
        color='FF6100'
    payload = json.dumps({
    "chat_id": int(chatid),
    "message_id": int(messageid),
    "text": "{\"width\":null,\"height\":null,\"data\":\"{\\\"tag\\\":\\\"column\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"12,7\\\",\\\"child\\\":{\\\"tag\\\":\\\"text\\\",\\\"data\\\":\\\""+biaoti+"\\\",\\\"style\\\":{\\\"color\\\":\\\""+color+"\\\",\\\"fontSize\\\":16,\\\"fontWeight\\\":\\\"medium\\\"}},\\\"backgroundColor\\\":\\\"ddeeff\\\"},{\\\"tag\\\":\\\"container\\\",\\\"child\\\":{\\\"tag\\\":\\\"column\\\",\\\"padding\\\":\\\"12\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"0,8,0,0\\\",\\\"child\\\":{\\\"tag\\\":\\\"markdown\\\",\\\"data\\\":\\\""+text+"\\\"}}]},\\\"backgroundColor\\\":\\\"ffffff\\\"}],\\\"crossAxisAlignment\\\":\\\"stretch\\\"}\",\"notification\":null,\"come_from_icon\":null,\"come_from_name\":null,\"template\":null,\"no_seat_toast\":null,\"type\":\"messageCard\"}",
    "parse_mode": "Fanbook",
    "reply_markup": {
        "inline_keyboard": [ik]
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    
def get_data(word:str,range:int) ->dict:
    """通过qq音乐获取

    Args:
        word (str): 关键词
        range (str): 页面

    Returns:
        dict: 返回json转化的字典
    """
    data=requests.get(url=f'https://api.lolimi.cn/API/yiny/?word={word}&n={range}')
    return json.loads(data.text)

def answerCallback(callback_id:str,text='ok',userid:str='1234',channelid:str='1234') ->str:
    """结束键盘按钮加载态

    Args:
        callback_id (str, 响应id): _description_. Defaults to str.
        text (str, 提示文本): _description_. Defaults to 'ok'.
        userid (str, 用户id): _description_. Defaults to str.
        channelid (str, 频道id): _description_. Defaults to str.

    Returns:
        str: 返回的json字符串
    """
    url = f"https://a1.fanbook.mobi/api/bot/{lingpai}/v2/answerCallback"

    payload = json.dumps({
    "callback_id": callback_id,
    "text": text,
    "user_id": userid,
    "channel_id": channelid
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def get_data_for_wyy(word:str,range:int) ->dict:
    """获取音乐在网易云

    Args:
        word (str): 关键词
        range (str): 页面

    Returns:
        dict: 返回json转化的字典，失败为None
    """
    r=requests.get(url=f'https://api.lolimi.cn/API/wydg/api.php?msg={word}&n={range}')
    try:
        r=json.loads(r.text)
        if r==6:r=None
    except:r=None
    return r
    
false=False
def on_message(ws, message):#当收到消息
    # 处理接收到的消息
    addmsg('收到消息',color='green')
    colorize_json(message)#格式化并高亮显示json字符串
    message=json.loads(message)#将json字符串转换为python对象
    #以下代码可以自行修改
    if message["action"] =="push":#如果是推送消息（忽略心跳消息）
        if message["data"]["author"]["bot"] == false:#如果不是机器人发送的消息（忽略机器人消息）
            content = json.loads(message["data"]["content"])#获取消息内容
            if "${@!"+bot_id+"}" in content['text']:#获取消息内容里面的纯文本内容，并判断有没有@该机器人（如果不是纯文本或者是其他消息会报错，不触发请查看bot id是否填写正确）
                print(content['text'])#输出全部消息
                print(content['text'][23:])#输出去掉@以后的消息
                # 在这里添加你希望执行的操作
                msg=content['text'][23:].split()
                cmd= msg[0]#获取命令
                if cmd=='/get':
                    d=get_data(word=msg[1],range=1)
                    if d['code']==202 or d['code']==400:
                        text=f'查询失败，无结果'
                        send_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text))#发送消息
                    else:
                        durl=d['data']['url']
                        if durl=='':
                            durl='请稍后重试'
                        text=f'音乐名：{d["data"]["song"]}  \\\\n{d["data"]["subtitle"]}  \\\\n歌手/作者：{d["data"]["singer"]}  \\\\n专辑：{d["data"]["album"]}  \\\\nBPM：{d["data"]["bpm"]}  \\\\n音质：{d["data"]["quality"]}  \\\\n发行日期：{d['data']['time']}  \\\\n封面图链接：{d['data']['cover']}  \\\\n时长：{d['data']['interval']}  \\\\n大小：{d['data']['size']}  \\\\n比特率：{d['data']['kbps']}  \\\\n下载链接：{durl}  \\\\n第1页'
                        send_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='获取成功',ik=[{"text":"flac转mp3","url":"https://www.freeconvert.com/zh/flac-to-mp3"},{"text":"下一页","callback_data":"{\"type\":\"next\",\"index\":2,\"msg\":\""+msg[1]+"\"}"}],text=str(text))#发送消息
                elif cmd=='/get2':
                    d=get_data_for_wyy(word=msg[1],range=1)
                    if d==None:
                        text=f'查询失败，无结果'
                        send_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text))#发送消息
                    else:
                        if d['code']==202 or d['code']==400:
                            text=f'查询失败，无结果'
                            send_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text))#发送消息
                        else:
                            durl=d["mp3"]
                            if durl=='':
                                durl='请稍后重试'
                            try:
                                review=d['review']
                                txt=review['content'].split('\n')
                                txt2=f'热评：  \\\\n**{review['nickname']}**  {review['timeStr']}  \\\\n'
                                for i in txt:
                                    txt2+=i+'  \\\\n'
                            except:
                                txt2=''
                            text=f'音乐名：{d["name"]}  \\\\n歌手/作者：{d["author"]}  \\\\n时长：{d["market"]}  \\\\n封面图链接：{d['img']}  \\\\n下载链接：{durl}  \\\\n{txt2}  \\\\n第1页'
                            send_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='获取成功',ik=[{"text":"下一页","callback_data":"{\"type\":\"next2\",\"index\":2,\"msg\":\""+msg[1]+"\"}"},{"text":"查看歌词","callback_data":"{\"type\":\"lyric2\",\"index\":1,\"msg\":\""+msg[1]+"\"}"}],text=str(text))#发送消息
                    
    elif message["action"] =="miniPush":#键盘
        #tnnd反人类设计
        channelid=message['data']['channel_id']
        messageid=message['data']['message_id']
        userid=message['data']['user_id']
        data=json.loads(message['data']['content'])
        cmd=json.loads(data['callback_query']['data'])
        messageid=data['callback_query']['inline_message_id']
        callback_id=data['callback_query']['id']
        msg=cmd['msg']
        answerCallback(callback_id=callback_id,userid=userid,channelid=channelid,text='正在获取，请稍等')
        if cmd['type'] =="next":#如果是下一页
            idx=cmd['index']
            d=get_data(word=msg,range=idx)
            if d['code']==202 or d['code']==400 or d['code']==203:
                text=f'查询失败，无结果或者页数超出范围'
                edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text),messageid=messageid)#发送消息
            else:
                durl=d['data']['url']
                if durl=='':
                    durl='请稍后重试'
                text=f'音乐名：{d["data"]["song"]}  \\\\n{d["data"]["subtitle"]}  \\\\n歌手/作者：{d["data"]["singer"]}  \\\\n专辑：{d["data"]["album"]}  \\\\nBPM：{d["data"]["bpm"]} \\\\n音质：{d["data"]["quality"]}  \\\\n发行日期：{d['data']['time']}  \\\\n封面图链接：{d['data']['cover']}  \\\\n时长：{d['data']['interval']}  \\\\n大小：{d['data']['size']}  \\\\n比特率：{d['data']['kbps']}  \\\\n下载链接：{durl}  \\\\n第{idx}页'
                edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='获取成功',ik=[{"text":"flac转mp3","url":"https://www.freeconvert.com/zh/flac-to-mp3"},{"text":"上一页","callback_data":"{\"type\":\"up\",\"index\":"+str(idx-1)+",\"msg\":\""+msg+"\"}"},{"text":"下一页","callback_data":"{\"type\":\"next\",\"index\":"+str(idx+1)+",\"msg\":\""+msg+"\"}"}],text=str(text),messageid=int(messageid))
                
        elif cmd['type'] =="up":#如果是上一页
            idx=cmd['index']
            d=get_data(word=msg,range=idx)
            if d['code']==202 or d['code']==400:
                text=f'查询失败，无结果'
                edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text),messageid=messageid)#发送消息
            else:
                durl=d['data']['url']
                if durl=='':
                    durl='请稍后重试'
                text=f'音乐名：{d["data"]["song"]}  \\\\n{d["data"]["subtitle"]}  \\\\n歌手/作者：{d["data"]["singer"]}  \\\\n专辑：{d["data"]["album"]}  \\\\nBPM：{d["data"]["bpm"]}\\\\n音质：{d["data"]["quality"]}  \\\\n发行日期：{d['data']['time']}  \\\\n封面图链接：{d['data']['cover']}  \\\\n时长：{d['data']['interval']}  \\\\n大小：{d['data']['size']}  \\\\n比特率：{d['data']['kbps']}  \\\\n下载链接：{durl}  \\\\n第{idx}页'
                edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='获取成功',ik=[{"text":"flac转mp3","url":"https://www.freeconvert.com/zh/flac-to-mp3"},{"text":"上一页","callback_data":"{\"type\":\"up\",\"index\":"+str(idx-1)+",\"msg\":\""+msg+"\"}"},{"text":"下一页","callback_data":"{\"type\":\"next\",\"index\":"+str(idx+1)+",\"msg\":\""+msg+"\"}"}],text=str(text),messageid=int(messageid))
        if cmd['type'] =="next2":
            idx=cmd['index']
            d=get_data_for_wyy(word=msg,range=idx)
            if d==None:
                text=f'查询失败，无结果'
                edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text),messageid=messageid)#发送消息
            else:
                if d['code']==202 or d['code']==400:
                    text=f'查询失败，无结果'
                    edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text),messageid=messageid)#发送消息
                else:
                    durl=d["mp3"]
                    if durl=='':
                        durl='请稍后重试'
                    try:
                        review=d['review']
                        txt=review['content'].split('\n')
                        txt2=f'热评：  \\\\n**{review['nickname']}**  {review['timeStr']}  \\\\n'
                        for i in txt:
                            txt2+=i+'  \\\\n'
                    except:
                        txt2=''
                    text=f'音乐名：{d["name"]}  \\\\n歌手/作者：{d["author"]}  \\\\n时长：{d["market"]}  \\\\n封面图链接：{d['img']}  \\\\n下载链接：{durl}  \\\\n{txt2}  \\\\n第{idx}页'
                    edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='获取成功',ik=[{"text":"上一页","callback_data":"{\"type\":\"up2\",\"index\":"+str(idx-1)+",\"msg\":\""+msg+"\"}"},{"text":"下一页","callback_data":"{\"type\":\"next2\",\"index\":"+str(idx+1)+",\"msg\":\""+msg+"\"}"},{"text":"查看歌词","callback_data":"{\"type\":\"lyric2\",\"index\":1,\"msg\":\""+msg+"\"}"}],text=str(text),messageid=messageid)
        if cmd['type'] =="up2":
            idx=cmd['index']
            d=get_data_for_wyy(word=msg,range=idx)
            if d==None:
                text=f'查询失败，无结果'
                edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text),messageid=messageid)
            else:
                if d['code']==202 or d['code']==400:
                    text=f'查询失败，无结果'
                    edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text),messageid=messageid)
                else:
                    durl=d["mp3"]
                    if durl=='':
                        durl='请稍后重试'
                    try:
                        review=d['review']
                        txt=review['content'].split('\n')
                        txt2=f'热评：  \\\\n**{review['nickname']}**  {review['timeStr']}  \\\\n'
                        for i in txt:
                            txt2+=i+'  \\\\n'
                    except:
                        txt2=''
                    text=f'音乐名：{d["name"]}  \\\\n歌手/作者：{d["author"]}  \\\\n时长：{d["market"]}  \\\\n封面图链接：{d['img']}  \\\\n下载链接：{durl}  \\\\n{txt2}  \\\\n第{idx}页'
                    edit_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='获取成功',ik=[{"text":"上一页","callback_data":"{\"type\":\"up2\",\"index\":"+str(idx-1)+",\"msg\":\""+msg+"\"}"},{"text":"下一页","callback_data":"{\"type\":\"next2\",\"index\":"+str(idx+1)+",\"msg\":\""+msg+"\"}"},{"text":"查看歌词","callback_data":"{\"type\":\"lyric2\",\"index\":1,\"msg\":\""+msg+"\"}"}],text=str(text),messageid=messageid)
        if cmd['type'] =="lyric2":
            idx=cmd['index']
            d=get_data_for_wyy(word=msg,range=idx)
            if d==None:
                text=f'查询失败，无结果'
                send_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text))
            else:
                if d['code']==202 or d['code']==400:
                    text=f'查询失败，无结果'
                    send_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='无结果',ik=[],text=str(text))
                else:
                    try:
                        lyric=d['lyric']
                        txt2=f''
                        for i in lyric:
                            txt2+="["+i['time']+']'+' '+i["name"]+'\n'
                    except:
                        txt2=''
                    text=f'歌词列表：\n{txt2}'
                    send_data_to_fb(chatid=int(message["data"]["channel_id"]),biaoti='获取成功',ik=[],text=str(text),type='text')
        answerCallback(callback_id=callback_id,userid=userid,channelid=channelid,text='获取完成')
                
def on_error(ws, error):
    # 处理错误
    #获取错误详细信息
    traceback.print_exc()
    
    addmsg("发生错误:"+str(error),color='red')
def on_close(ws):
    # 连接关闭时的操作
    addmsg("连接已关闭",color='red')
def on_open(ws):
    # 连接建立时的操作
    addmsg("连接已建立",color='green')
    # 发送心跳包
    def send_ping():
        print('发送：{"type":"ping"}')
        ws.send('{"type":"ping"}')
    send_ping()  # 发送第一个心跳包
    # 定时发送心跳包
# 替换成用户输入的BOT令牌
lingpai = lingpai
url = requests_url+f"{lingpai}/getMe"
# 发送HTTP请求获取基本信息
response = requests.get(url)
data = response.json()
def send_data_thread():
    while True:
        # 在这里编写需要发送的数据
        time.sleep(25)
        ws.send('{"type":"ping"}')
        addmsg('发送心跳包：{"type":"ping"}',color='green')
if response.ok and data.get("ok"):
    user_token = data["result"]["user_token"]#获取user token以建立连接
    device_id = "your_device_id"
    version_number = "1.6.60"
    #拼接base64字符串
    super_str = base64.b64encode(json.dumps({
        "platform": "bot",
        "version": version_number,
        "channel": "office",
        "device_id": device_id,
        "build_number": "1"
    }).encode('utf-8')).decode('utf-8')
    ws_url = websocket_url+f"?id={user_token}&dId={device_id}&v={version_number}&x-super-properties={super_str}"#准备url
    threading.Thread(target=send_data_thread, daemon=True).start()#启动定时发送心跳包的线程
    # 建立WebSocket连接
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
else:
    addmsg("无法获取BOT基本信息，请检查令牌是否正确。",color='red')
