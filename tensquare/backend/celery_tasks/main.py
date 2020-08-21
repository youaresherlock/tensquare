from celery import Celery


# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tensquare.settings.dev'


# 创建celery应用
celery_app = Celery('tensquare')

# 导入celery配置
celery_app.config_from_object('celery_tasks.config')

# 导入任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])

# 在命令行需要执行的命令如下:
# celery -A celery_tasks.main worker --loglevel=info
