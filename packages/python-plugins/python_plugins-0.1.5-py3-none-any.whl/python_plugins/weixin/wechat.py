import hashlib
import time
from python_plugins.convert import xml2dict
from .wechat_crypt import MessageCrypt

XML_TEXT_TEMPLATE = """<xml>
<ToUserName><![CDATA[{touser}]]></ToUserName>
<FromUserName><![CDATA[{fromuser}]]></FromUserName>
<CreateTime>{createtime}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>"""


class Wechat:

    def __init__(self, name=None):
        self.name = name
        self.app = self.get_app()

    # 获取app
    def get_app(self) -> dict:
        raise NotImplementedError()

    # 记录信息
    def log_data(self):
        return

    def verify(self, args):
        signature = args["signature"]
        timestamp = args["timestamp"]
        nonce = args["nonce"]
        echostr = args["echostr"]
        token = self.app["token"]
        tmpstr = "".join(sorted([token, timestamp, nonce])).encode("utf8")
        if hashlib.sha1(tmpstr).hexdigest() == signature:
            return echostr
        else:
            return

    def chat(self, args, content):
        self.openid = args.get("openid")
        msg_signature = args.get("msg_signature", "")
        timestamp = args.get("timestamp", "")
        nonce = args.get("nonce", "")
        # 加密标记
        encrypt_type = args.get("encrypt_type")
        xml_dict = xml2dict(content)

        if not encrypt_type:
            # 未加密
            result = self.dispatch(xml_dict)
            xml_reponse = self.responseText(result)
        else:
            # 解密
            mc = MessageCrypt(self.app["appid"], self.app["token"], self.app["aeskey"])
            xml_decrypted = mc.decrypt_msg(
                timestamp, nonce, xml_dict["Encrypt"], msg_signature
            )
            decrypted_dict = xml2dict(xml_decrypted)
            result = self.dispatch(decrypted_dict)
            unencrypted_xml = self.responseText(result)
            # 加密
            xml_reponse = mc.encrypt_msg(unencrypted_xml, timestamp, nonce)

        return xml_reponse

    def responseText(self, content):
        data = {
            "touser": self.fromUser,
            "fromuser": self.toUser,
            "createtime": int(time.time()),
            "content": content,
        }
        return XML_TEXT_TEMPLATE.format(**data)

    def dispatch(self, data):
        self.toUser = data["ToUserName"]
        self.fromUser = data["FromUserName"]
        msgType = data["MsgType"]

        if msgType == "text":
            keyword = data["Content"]
        elif msgType == "event":
            event = data["Event"]
            if event == "subscribe":
                # self.onSubscribe()
                keyword = "subscribe"
            elif event == "unsubscribe":
                # self.onUnsubscribe()
                keyword = "unsubscribe"
            elif event == "CLICK":
                eventKey = data["EventKey"]
                keyword = eventKey
            else:
                keyword = "<event:{event}>"
        elif msgType == "image":
            keyword = f"<{msgType}>"
        elif msgType == "voice":
            keyword = f"<{msgType}>"
        elif msgType == "video":
            keyword = f"<{msgType}>"
        elif msgType == "shortvideo":
            keyword = f"<{msgType}>"
        elif msgType == "location":
            location_x = data["location_x"]
            location_y = data["location_y"]
            keyword = f"<{msgType}({location_x},{location_y})>"
        elif msgType == "link":
            keyword = f"<{msgType}>"
        else:
            keyword = f"<{msgType}>"

        self.keyword = keyword
        answer = self.answer()

        # 返回前记录下日志，如果实现记录日志的话
        self.log_data()

        return self.responseText(answer)

    def answer(self):
        q = self.keyword
        if q == "subscribe":
            r = f"您好,欢迎关注[{self.app['name']}]!"
        else:
            r = q
        return r
