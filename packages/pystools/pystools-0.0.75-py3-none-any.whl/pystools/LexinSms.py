# -*- coding: utf-8 -*-
import requests
import hashlib
from deprecated import deprecated

API_URL = "https://sdkv2.lx598.com/msgpool/sdk/"


# 乐信短信接口

class LexinSms:
    def __init__(self, app_id, app_secret, acc_name, acc_pwd, **kwargs):
        self.__dict__.update(locals())
        self.AppID = app_id
        self.AppSecret = app_secret
        self.accName = acc_name

        m = hashlib.md5()
        m.update(f"{acc_pwd}".encode("utf-8"))
        self.accPwd = m.hexdigest().upper()

    @staticmethod
    def md5_hash(string):
        """Return MD5 hash of the given string."""
        return hashlib.md5(string.encode()).hexdigest().upper()

    def send_sms(self, aimcodes, content):
        """Send SMS."""
        params = {
            'AppID':  self.accName,
            'AppSecret': self.accPwd,
            'aimcodes': aimcodes,
            'content': content,
            'dataType': 'json'
        }
        response = requests.post(API_URL + "send", data=params)
        return response.text

    def qry_balance(self):
        """Query balance."""
        params = {
            'AppID':  self.accName,
            'AppSecret': self.accPwd
        }
        response = requests.post(API_URL + "qryBalance", data=params)
        return response.text

    def qry_report(self):
        """Query report."""
        params = {
            'AppID':  self.accName,
            'AppSecret': self.accPwd
        }
        response = requests.post(API_URL + "qryReport", data=params)
        return response.text

    def receive_sms(self):
        """Receive SMS."""
        params = {
            'AppID':  self.accName,
            'AppSecret': self.accPwd
        }
        response = requests.post(API_URL + "receiveSms", data=params)
        return response.text

    @deprecated(reason="此方法不建议再使用，请使用send_sms方法")
    def send(self, aimcodes, content, msgId, extNo):
        """

        """
        accName = self.accName
        accPwd = self.accPwd
        url = f"http://sdk.lx198.com/sdk/send?dataType=json&accName={accName}&" \
              f"accPwd={accPwd}&aimcodes={aimcodes}&content={content}&msgId={msgId}&extNo={extNo}"
        """
        accName    用户名(乐信登录账号)
        aimcodes	手机号码(多个手机号码之间用英文半角“,”隔开,单次最多支持5000个号码)
        msgId	提交短信包的唯一id(15位以内数字)，推送短信回执时，会推送此值，用此值和手机号码来匹配短信的状态，如需要接受回执则必须提交此参数,单次提交只需要提交一个即可
        extNo	扩展号(6位以内数字)，推送短信上行时，会推送extNo，用extNo和手机号码来匹配短信的上行，单次提交只需要提交一个即可
        accPwd  密码(乐信登录密码32位MD5加密后转大写，如123456加密完以后为：E10ADC3949BA59ABBE56E057F20F883E)
        """

        # 使用urllib3库发送请求
        import urllib3
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        return r.data.decode('utf-8')


if __name__ == '__main__':
    AppID = "xxx"
    AppSecret = "xxx"
    accName = "xxx"
    accPwd = "xxx"
    aimcodes = "xxx"
    content = "验证码：1234，有效时间10分钟。如非本人操作，请忽略。【灵感涌现】"
    msgId = "12312312312"
    extNo = "123"
    sms = LexinSms(AppID, AppSecret, accName, accPwd)
    print(sms.send(aimcodes, content, msgId, extNo))
