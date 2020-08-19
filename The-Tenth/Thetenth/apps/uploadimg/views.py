from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from fdfs_client.client import Fdfs_client
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from Thetenth.utils.fastdfs.fastdfs_storage import FastDFSStorage
from rest_framework.response import Response


# 创建上传图片的类视图函数
class UploadPublicView(APIView):
    """公共图片上传"""

    def post(self, request):
        res = self.uploadfastdfs(request.data.get('img'))
        return Response({'imgurl': res})

    @staticmethod
    def uploadfastdfs(data):
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        res = client.upload_appender_by_buffer(data.read())
        if res.get('Status') != 'Upload successed.':
            raise APIException('上传到FDFS失败')
        file_name = res.get('Remote file_id')
        return settings.FDFS_URL + file_name


# 创建前端富文本编辑器上传图片的视图
class UploadCommonView(APIView):
    """
    上传前段富文本编辑器
    """
    def post(self, request):
        """
        用于上传文本图片
        :param request:
        :return:
        """
        image_data = request.FILES.get('upload')

        client = Fdfs_client(settings.FDFS_CLIENT_CONF)

        ret = client.upload_by_buffer(image_data.read())
        print(ret)
        if ret.get('Status') != 'Upload successed.':
            return Response({'message': '图片上传失败'}, status=status.HTTP_400_BAD_REQUEST)
        imageurl = ret.get('Remote file_id')

        CKEditorFuncNum = request.query_params.get('CKEditorFuncNum')
        from_address = request.META['HTTP_REFERER']
        from_address = from_address[:from_address.rfind('/'):]

        ret_url = from_address + '/upload_success.html?image_url=' + settings.FDFS_URL + imageurl + '&CKEditorFuncNum=' + CKEditorFuncNum

        return HttpResponseRedirect(ret_url)
