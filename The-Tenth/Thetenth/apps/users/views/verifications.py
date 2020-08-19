from django.views import View
from django_redis import get_redis_connection
import random, logging, re
from celery_tasks.sms.tasks import ccp_send_sms_code
from apps.users.models import User
from django.http import JsonResponse

# 获取当前django的logger
logger = logging.getLogger('django')


class VerificationsView(View):
    """
    获取短信验证码
    """
    def get(self, request, mobile):
        conn = get_redis_connection("verify_code")
        # 判断标记是否存在 如果标记存在 说明已经发送
        send_flag = conn.get('send_flag_%s' % mobile)

        # 对手机号进行判断
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'success': False,
                                 'message': '手机格式不正确'})

        if send_flag:
            return JsonResponse({'success': False, 'errmsg': '频繁发送短信验证码'})

        # 判断手机号是否重复
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'success': False, 'errmsg': '查询数据库错误'})

        if count:
            return JsonResponse({'success': False, 'errmsg': '手机号已经被注册'})
        # 生成短信验证码
        sms_code = "%06d" % random.randint(100000, 999999)
        logger.info(sms_code)
        # 保存短信验证码 并设置有效期
        # 创建管道
        pl = conn.pipeline()

        # 保存标记
        pl.setex('send_flag_%s' % mobile, 60, 1)

        # 保存短信验证码到数据库
        pl.setex('sms_%s' % mobile, 300, sms_code)

        # 执行管道
        pl.execute()

        # 异步发送短信
        ccp_send_sms_code.delay(mobile, sms_code)

        # 返回相应
        return JsonResponse({'success': True, 'sms_code': sms_code, 'message': '发送短信成功'})