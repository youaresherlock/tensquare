# 定义任务的文件
# 提示: celery里面的所有的任务 本质是标准的python函数
from celery_tasks.main import celery_app
from celery_tasks.sms.yuntongxun.ccp_sms import CCP


# 使用celery自带的装饰器去装饰函数 让celery可以识别该函数
# 语法: @celery_app.task(name='起别名') 名字与任务名同名
@celery_app.task(name='ccp_send_sms_code')
def ccp_send_sms_code(mobile, sms_code):
    """
    该函数就是一个任务, 用于发送短信的异步任务
    """
    result = CCP().send_template_sms(mobile, [sms_code, 5], 1)
    return result
