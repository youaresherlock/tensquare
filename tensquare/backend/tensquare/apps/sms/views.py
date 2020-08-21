import random

from django.shortcuts import render

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from celery_tasks.sms.tasks import send_sms_code
from sms import constants


class SMSCodeView(APIView):
    """
    短信验证码
    """
    def get(self, request, mobile):
        redis_conn = get_redis_connection('verify_codes')
        send_flag = redis_conn.get("send_flag_%s" % mobile)

        if send_flag:
            return Response({'success': False, 'message': '请求次数过于频繁'}, status=400)

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # redis管道
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 让管道通知redis执行命令
        pl.execute()
        print("短信验证码:%s" % sms_code)
        # 使用celery发送短信验证码
        expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        send_sms_code.delay(mobile, sms_code, expires, constants.SMS_CODE_TEMP_ID)
        # 正式版本中,应该把sms_code这个字段去除
        return Response({'success':True,'message': 'OK','sms_code':sms_code})




