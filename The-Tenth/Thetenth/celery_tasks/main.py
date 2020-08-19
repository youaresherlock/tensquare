# celery入口文件
from celery import Celery

# 用于在异步中添加django自带的模块 要在创建celery实例之前

import os
import django
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'
django.setup()

# 利用导入的celery创建对象 创建celery实例
# 语法: Celery('别名') = 实例名
celery_app = Celery('meiduo')

# 加载配置文件
# 将里面的参数作为我们创建的config配置文件:
# 对象名.config_from_object('配置文件路径')
celery_app.config_from_object('celery_tasks.config')

# 注册异步任务
# 语法: 对象.autodiscover_tasks(['路径(只引导到任务包名即可)'])
celery_app.autodiscover_tasks(['celery_tasks.sms'])
