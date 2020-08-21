import logging
from django.db import DatabaseError
from redis import RedisError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger('django')


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        view = context['view']
        logger.error('[%s] %s' % (view, exc))
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            response = Response({'message': '数据库出现了异常'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        else:
            response = Response({'message': '服务器出现了未知异常'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response