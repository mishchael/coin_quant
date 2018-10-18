# _*_coding:utf-8 _*_
# coding=utf-8

import requests, json
from datetime import datetime

# quant
corpid = 'wwc682c605338cd3b3'
quant_agentid = '1000002'
quant_app_key = 'cJ0fTJ3E6wpHHh3HQQkAmBWE6rU52NQ7_roEdeQ3ubk'

quant_app_receive_token = 'Ox4peQ1bZPSqqWw8reV6btnEZ7TVJN'
quant_app_receive_key = 'Rt715OC9D67z189TiUBKmFvU3FniRyEOVceJR2CCRtu'


class Send_Message:
    def __init__(self):
        self.agentid = quant_agentid
        self.app_key = quant_app_key

    def get_media_ID(self):
        img_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload'
        payload_img = {
            'access_token': '%s' % self.token,
            'type': 'image'
        }
        # print payload_img
        data = {'media': open(self.path, 'rb')}
        r = requests.post(url=img_url, params=payload_img, files=data)
        d = r.json()
        # print d
        return d['media_id']

    def send_image(self, touser, path):
        self.touser = touser
        self.path = path
        self.token = self.Token()
        self.image_id = self.get_media_ID()
        data = {"touser": self.touser,
                "toparty": " PartyID1 | PartyID2 ",
                "totag": " TagID1 | TagID2 ",
                "msgtype": "image",
                "agentid": self.agentid,
                "image": {
                    "media_id": "%s" % (self.image_id)
                },
                "safe": 0
                }
        # json.dumps在解析格式时，会使用ascii字符集，所以解析后的数据无法显示中文，ensure_ascii不解析为ascii字符集，使用原有字符集
        value = json.dumps(data, ensure_ascii=False)

        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (self.token)
        r = requests.post(url, data=value)
        return r.text

    def send_message(self, touser, text):
        self.touser = touser
        self.text = text
        self.token = self.Token()
        self.text = text
        print(text)
        data = {"touser": self.touser,
                "toparty": " PartyID1 | PartyID2 ",
                "totag": " TagID1 | TagID2 ",
                "msgtype": "text",
                "agentid": self.agentid,
                "text": {
                    "content": "%s" % (self.text)
                },
                "safe": 0
                }
        # json.dumps在解析格式时，会使用ascii字符集，所以解析后的数据无法显示中文，ensure_ascii不解析为ascii字符集，使用原有字符集
        value = json.dumps(data, ensure_ascii=False)

        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (self.token)
        r = requests.post(url, data=value.encode('utf-8'))
        return r.text

    def Token(self):  # 发送到“查询余额”
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        # corpid,corpsecret 为微信端获取
        params = {'corpid': corpid,
                  'corpsecret': self.app_key
                  }
        r = requests.get(url=url, params=params)
        token = json.loads(r.text)['access_token']
        return token

    def try_send_message(self,text):
        try:
            now = datetime.now().replace(microsecond=0)
            text=str(now)+"\n"+text
            self.send_message( "@all", text.encode("utf-8").decode("latin1"))
        except:
            pass


