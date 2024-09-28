import pytest
import time
import hashlib
from python_plugins.weixin.wechat import Wechat
from python_plugins.random import rand_digit, rand_letter


test_wechat_app = {
    "name": "test",
    "appid": "wx2c2769f8efd9abc2",
    "token": "spamtest",
    "aeskey": "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG",
    "appsecret": "45658c05647671e481d75b6fa23e6add",
}


class MyWechat(Wechat):
    def get_app(self) -> dict:
        return test_wechat_app


class TestWechat:
    def test_verify(self):
        mywechat = MyWechat()
        # timestamp = "1409735669"
        timestamp = str(int(time.time()))
        # nonce = "1320562132"
        nonce = rand_digit(10)
        token = test_wechat_app["token"]
        signature = hashlib.sha1(
            "".join(sorted([token, timestamp, nonce])).encode("utf8")
        ).hexdigest()
        # echostr = "780419598460648693"
        echostr = rand_digit(18)
        query = {
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": signature,
            "echostr": echostr,
        }
        r = mywechat.verify(query)
        # print(r)
        assert r == echostr

    def test_chat(self):
        """chat（明文）"""
        text = rand_letter(10)
        timestamp = str(int(time.time()))
        nonce = rand_digit(10)
        xml = (
            "<xml>"
            "<ToUserName><![CDATA[gh_73951532543e]]></ToUserName>"
            "<FromUserName><![CDATA[oMIza6tX35aDNfoXr4JGP02QvM08]]></FromUserName>"
            "<CreateTime>{timestamp}</CreateTime>"
            "<MsgType><![CDATA[text]]></MsgType>"
            f"<Content><![CDATA[{text}]]></Content>"
            "<MsgId>23533248665819413</MsgId>"
            "</xml>"
        )
        query = {
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": "b5fa0bcde34ab0b6dccd6e23034c26c0cf5ecbaa",
            "openid": "oMIza6tX35aDNfoXr4JGP02QvM08",
        }

        mywechat = MyWechat()
        r = mywechat.chat(query, xml)
        # print(r)
        assert query["openid"] in r

    def test_chat_aes(self):
        """chat（密文），微信提供的demo"""
        xml = (
            "<xml>"
            "<ToUserName><![CDATA[gh_10f6c3c3ac5a]]></ToUserName>"
            "<FromUserName><![CDATA[oyORnuP8q7ou2gfYjqLzSIWZf0rs]]></FromUserName>"
            "<CreateTime>1409735668</CreateTime>"
            "<MsgType><![CDATA[text]]></MsgType>"
            "<Content><![CDATA[abcdteT]]></Content>"
            "<MsgId>6054768590064713728</MsgId>"
            "<Encrypt>"
            "<![CDATA[hyzAe4OzmOMbd6TvGdIOO6uBmdJoD0Fk53REIHvxYtJlE2B655HuD0m8KUePW"
            "B3+LrPXo87wzQ1QLvbeUgmBM4x6F8PGHQHFVAFmOD2LdJF9FrXpbUAh0B5GIItb52sn896"
            "wVsMSHGuPE328HnRGBcrS7C41IzDWyWNlZkyyXwon8T332jisa+h6tEDYsVticbSnyU8dK"
            "OIbgU6ux5VTjg3yt+WGzjlpKn6NPhRjpA912xMezR4kw6KWwMrCVKSVCZciVGCgavjIQ6X"
            "8tCOp3yZbGpy0VxpAe+77TszTfRd5RJSVO/HTnifJpXgCSUdUue1v6h0EIBYYI1BD1DlD+"
            "C0CR8e6OewpusjZ4uBl9FyJvnhvQl+q5rv1ixrcpCumEPo5MJSgM9ehVsNPfUM669WuMyV"
            "WQLCzpu9GhglF2PE=]]>"
            "</Encrypt>"
            "</xml>"
        )

        query = {
            "timestamp": "1409735669",
            "nonce": "1320562132",
            "encrypt_type": "aes",
            "msg_signature": "5d197aaffba7e9b25a30732f161a50dee96bd5fa",
        }

        mywechat = MyWechat()
        r = mywechat.chat(query, xml)
        # print(r)
        assert f'<Nonce><![CDATA[{query["nonce"]}]]></Nonce>' in r
