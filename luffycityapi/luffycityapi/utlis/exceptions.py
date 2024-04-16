from rest_framework.views import exception_handler
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework import status
from redis import RedisError
import logging


logger = logging.getLogger('django')

def custom_exception_handler(exec,context):
    """
    自定义异常
    :param exec: 异常类
    :param context： 抛出异常的执行上下文
    :return: Response响应对象
    """
    # 调用drf原生异常处理方法
    response = exception_handler(exec,context)
    if response is  None:
        view = context['view']
        # 判断是否发生数据库的异常
        if isinstance(exec,DatabaseError):
            # 数据库异常
            logger.error(f'mysql数据库异常！[{view}] {exec}')
            response = Response({"message":"服务器内部错误"},status=status.HTTP_507_INSUFFICIENT_STORAGE)

        if isinstance(exec,ZeroDivisionError):
            response = Response({"message": "0不能作为除数"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if isinstance(exec,RedisError):
            logger.error(f'redis数据库异常！[{view}] {exec}')
            response = Response({"message": "服务器内部错误"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return Response