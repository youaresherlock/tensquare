import json
from django.conf import settings
import urllib.parse
from urllib.request import urlopen
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from user.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id':user.id,
        'mobile': user.mobile,
        'username': user.username,
        'avatar':user.avatar
    }


def get_user_by_account(account):
    """根据帐号获取用户对象"""
    users = User.objects.filter(Q(username=account)|Q(mobile=account))
    if not users:
        return None
    return users[0]


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """username可能是用户名， 也可能是手机号"""
        # 获取用户对象
        user = get_user_by_account(username)

        if user is not None and user.check_password(password):
            return user


class OAuthWeixin(object):
    """
    微信认证辅助工具类
    """
    def __init__(self, app_id=None, secret=None):
        self.app_id = app_id if app_id else settings.WEIXIN_APP_ID
        self.secret = secret if secret else settings.WEIXIN_SECRET

    def get_access_token(self, code):

        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'

        params = {
            'grant_type': 'authorization_code',
            'appid': self.app_id,
            'secret': self.secret,
            'code': code
        }

        url += urllib.parse.urlencode(params)

        # 发送请求
        resp = urlopen(url)
        # 读取响应体数据
        resp_data = resp.read()
        resp_data = resp_data.decode()
        resp_data = json.loads(resp_data)
        access_token = resp_data.get('access_token')
        open_id = resp_data.get('openid')
        return access_token,open_id

    def get_weixin_user_info(self, access_token, open_id):
        url = 'https://api.weixin.qq.com/sns/userinfo?access_token=' + access_token + '&openid=' + open_id
        # 发送请求
        resp = urlopen(url)
        # 读取响应体数据
        resp_data = resp.read()  # bytes
        resp_data = resp_data.decode()  # str

        resp_data = json.loads(resp_data)
        # 解析
        open_id = resp_data.get('openid')
        nickname = resp_data.get('nickname')
        avatar = resp_data.get('headimgurl')
        return open_id, nickname, avatar
