#!/usr/bin/env python
# _*_coding:utf-8 _*_
# coding=utf-8
__filename__ = 'wx.py'
__author__ = 'zhang.zheng'
__description__ = ''

import sys
sys.path.append('/Library/Python/2.7/site-packages')

from flask import Flask, request
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import time
from common import *
from MenuFunc import *
import subprocess

proc = None

logfile = './logfile.txt'
weblogfile = './weblogfile.txt'

def log(s):
    s1 = '[' + time.strftime('%Y-%m-%d %H:%M:%S') + ']' + s
    s2 = '[' + time.strftime('%Y-%m-%d %H:%M:%S') + ']' + s + "\n"
    print(s1)
    f = open(logfile, 'a')
    f.write(s2)
    f.close()

def weblog(s):
    s1 = '[' + time.strftime('%Y-%m-%d %H:%M:%S') + ']' + s
    s2 = '[' + time.strftime('%Y-%m-%d %H:%M:%S') + ']' + s + "\n"
    print(s1)
    f = open(weblogfile, 'a')
    f.write(s2)
    f.close()

def query_bfx_position(id):
    '''
    可以实现你自己的查询仓位,或者其实你想干什么都行。其实微信server端这个就是用来接受消息的，接受到不同的消息，你做不同的处理，然后返回给为微信端。
    :param id:
    :return:
    '''
    msg = 'xxx'
    return msg

def query_params(id):
    '''
    这里可以查询程序的运行参数。如果你是写死在程序里面，那估计查不了，有的人可能会有一个运行参数的配置文件，程序每次启动去读配置文件，那么这个函数就可以去读那个配置文件
    :param id:
    :return:
    '''
    msg ="xxx"
    return msg


def query_bfx_trx(id):
    '''
    这里可以做一些交易记录的查询，比如你的程序把每次做的交易的汇总信息写到本地文件，这个函数就可以读取这个信息返回给微信。
    :param id:
    :return:
    '''
    msg="xxx"
    return msg

def set_running(config_id,running):
    '''
    这里大家可以对程序的暂停和恢复进行控制，具体怎么样实现，就要看你的程序了。
    :param config_id:
    :param running:
    :return:
    '''
    msg="xxx"
    return msg


def verify_message(token, key):
    weblog("============app token=%s============" % token)
    wxcpt = WXBizMsgCrypt(token, key, corpid)
    # 获取url验证时微信发送的相关参数
    sVerifyMsgSig = request.args.get('msg_signature')
    sVerifyTimeStamp = request.args.get('timestamp')
    sVerifyNonce = request.args.get('nonce')
    sVerifyEchoStr = request.args.get('echostr')
    #
    sReqMsgSig = sVerifyMsgSig
    sReqTimeStamp = sVerifyTimeStamp
    sReqNonce = sVerifyNonce
    #
    sResqMsgSig = sVerifyMsgSig
    sResqTimeStamp = sVerifyTimeStamp
    sResqNonce = sVerifyNonce
    weblog("request.method=%s" % request.method)

    weblog('token=%s' % token)
    weblog('key=%s' % key)
    weblog('corpid=%s' % corpid)
    weblog('sVerifyMsgSig=%s' % sVerifyMsgSig)
    weblog('sVerifyTimeStamp=%s' % sVerifyTimeStamp)
    weblog('sVerifyNonce=%s' % sVerifyNonce)
    weblog('sVerifyEchoStr=%s' % sVerifyEchoStr)

    # 验证url
    if request.method == 'GET':
        ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        if (ret != 0):
            # weblog("ERR: VerifyURL ret:" + str(ret))
            weblog("GET URL 验证失败,退出")
            return request.method, ret
        else:
            weblog("GET验证成功")
            return request.method, sEchoStr
    # 接收客户端消息
    if request.method == 'POST':
        sReqMsgSig = request.form.get('msg_signature')
        sReqTimeStamp = request.form.get('timestamp')
        sReqNonce = request.form.get('nonce')
        # 赋值url验证请求相同的参数，使用上面注释掉的request.form.get方式获取时，测试有问题
        sReqMsgSig = sVerifyMsgSig
        sReqTimeStamp = sVerifyTimeStamp
        sReqNonce = sVerifyNonce
        sReqData = request.data
        # weblog("sReqData=%s" %sReqData)
        ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        # weblog("sMsg=%s" %sMsg)
        if (ret != 0):
            # weblog("ERR: VerifyURL ret:" + str(ret))
            weblog("POST 当前请求不是该应用的消息,函数退出")
            return request.method, None
        else:
            weblog("POST验证成功")
            return request.method, sMsg

# get_xml_tree_result
def get_xml_tree_result(xml_tree):
    weblog("begin to resolve content or eventkey")
    try:
        content = xml_tree.find("Content").text
        weblog("Content=%s" % content)
    except:
        content = None
    try:
        eventkey = xml_tree.find("EventKey").text
        weblog("EventKey=%s" % eventkey)
    except:
        eventkey = None
    return content, eventkey


def get_fromuser(xml_tree):
    try:
        # weblog("trying to resolve FromUserName from data")
        FromUserName = xml_tree.find("FromUserName").text
        weblog("FromUserName=%s" % FromUserName)
    except:
        FromUserName = "ZhangShiChao"
        weblog("cannot get FromUserName,using default :%s" % FromUserName)
    return FromUserName


app = Flask(__name__)


@app.route('/index', methods=['GET', 'POST'])
def index():

    # 接受quant端的消息
    method, Msg = verify_message(quant_app_receive_token, quant_app_receive_key)
    if method == 'POST' and Msg != None:
        xml_tree = ET.fromstring(Msg)
        content, eventkey = get_xml_tree_result(xml_tree)
        touser = get_fromuser(xml_tree)
        username = touser.lower()

        if eventkey == '1':
            weblog("begin to query balance")
            msg = get_bfx_balance()
            weblog('msg=%s' % msg)
            s = Send_Message()
            s.send_message(username, msg)
            weblog('username=%s' % username)
        elif eventkey == '2':
            weblog("begin to query params")
            msg = query_params(1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '3':
            weblog("begin to query trade history")
            msg = query_trx(1)
            msg = "BITMEX ETHUSD\n"+msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '4':
            weblog("begin to set running=0")
            msg = set_running(1,0)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '5':
            weblog("begin to set running=0")
            msg = set_running(1,1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '6':
            weblog("begin to set running=0")
            msg = set_running(1,1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '7':
            weblog("begin to set running=0")
            msg = set_running(1,1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '8':
            weblog("begin to set running=0")
            msg = set_running(1,1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '9':
            weblog("begin to start strategy")
            pid = strategy_start('script_detect')
            if pid:
                msg = '策略已启动,pid：%s' % pid
                s = Send_Message()
                s.send_message(username, msg)
        elif eventkey == '10':
            weblog("begin to set running=0")
            msg1 = strategy_stop(name = 'script_detect')
            msg2 = strategy_stop(name = 'bfx_main')
            s = Send_Message()
            s.send_message(username, msg1)
            s.send_message(username, msg2)
        elif eventkey == '11':
            weblog("begin to set running=0")
            msg = set_running(1,1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '12':
            weblog("begin to set running=0")
            msg = set_running(1,1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '13':
            weblog("begin to set running=0")
            msg = set_running(1,1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '14':
            weblog("begin to set running=0")
            msg = set_running(1,1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)
        elif eventkey == '15':
            weblog("begin to set running=0")
            msg = set_running(1,1)
            msg = "BITMEX ETHUSD\n" + msg
            s = Send_Message()
            s.send_message(username, msg)

    elif method == 'GET':
        return Msg

    if Msg != None:
        return Msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)






