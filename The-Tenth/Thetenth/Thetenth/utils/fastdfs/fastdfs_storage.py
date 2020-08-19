# 自定义文件存储类 提供文件下载的全路径
from django.conf import settings
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from rest_framework.exceptions import APIException


class FastDFSStorage(Storage):
    """实现文件存储"""

    def _open(self, name, mode='rb'):
        """
        打开文件时自动调用,因为当前不是打开文件 文档要求必须实现
        只能写上pass 防止报错
        :param mode: 要打开文件的模式
        :return: None
        """
        pass

    def _save(self, name, content):
        """
        保存文件自动调用 因为当前不是打开文件 文档要求必须实现
        只能写上 pass 防止报错
        name: 上传文件名称
        content : 文件对象 可以通过content.read() 获取上传文件的内容
        :param content: 保存的文件
        :return: None
        """

        # 将上传的文件保存到Fdfs文件系统
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)

        # 上传文件
        result = client.upload_by_buffer(content.read())

        if result.get('Status') != 'Upload successed.':
            raise APIException('Fdfs上传文件失败')

        file_id = result.get('Remote file_id')
        return file_id

    # 判断在我们上传之前,判断文件名称是否冲突
    def exists(self, name):
        """
        根据上面的图片 可知
        fdfs中文件名fdfs生成 所以不可能冲突
        返回false代表永不冲突
        :param name:
        :return:
        """
        return False

    def url(self, name):
        """
        返回文件下载全路径的方法
        :param name: 外界返回的image字段传入到文件名中查找
        :return: 将拼接路径返回 http://192.168.254.128:8888
        """
        return settings.FDFS_URL + name
        # 获取SKUImage image.url+> 文件存储类的url方法返回值

