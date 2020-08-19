# -*- coding:utf-8 -*-

import ssl

import sys

# sys.path ====> []

# sys.path.insert(0, '../../../')

# 根据自己项目的目录 调整导包格式
from celery_tasks.sms.yuntongxun.CCPRestSDK import REST

ssl._create_default_https_context = ssl._create_unverified_context  # 全局取消证书验证


# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8a216da87249b81301728728cef41dff'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = 'e15187994a344c57b77a02be31ecc488'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8a216da872e4fa670172f9c8001b0537'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'app.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'


class CCP(object):
    """发送短信的辅助类"""

    def __new__(cls, *args, **kwargs):
        # 判断是否存在类属性_instance，_instance是类CCP的唯一对象，即单例
        if not hasattr(CCP, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)
        return cls._instance

    def send_template_sms(self, to, datas, temp_id):
        """发送模板短信"""
        # @param to 手机号码
        # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
        # @param temp_id 模板Id
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # 如果云通讯发送短信成功，返回的字典数据result中statuCode字段的值为"000000"
        if result.get("statusCode") == "000000":
            # 返回0 表示发送短信成功
            return 0
        else:
            # 返回-1 表示发送失败
            return -1


# if __name__ == '__main__':
#     # 注意： 测试的短信模板编号为1
#     # CCP().send_template_sms('手机号码', ['短信验证码', 过期时间], '模板ID')
#     CCP().send_template_sms('17319256402', ['888888', 5], 1)