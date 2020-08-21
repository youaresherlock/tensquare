from django.shortcuts import render, redirect

# Create your views here.
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from upload.qiniu_storage import QiniuStorage


class ImageUploadViewForCKEditor(APIView):
    def post(self, request):
        storage = QiniuStorage()
        ret = storage._save("", request.data.get("upload"))
        from_address = request.META['HTTP_REFERER']
        from_address = from_address[:from_address.rfind('/'):]
        ret_url = from_address + '/upload_success.html?image_url=' + settings.IMAGE_BASE_URL + ret + '&CKEditorFuncNum=' + request.query_params.get(
            'CKEditorFuncNum')
        return redirect(ret_url)


class ImageUploadViewForAvatar(APIView):
    def post(self, request):
        storage = QiniuStorage()
        ret = storage._save("", request.data.get("img"))
        ret_url = settings.IMAGE_BASE_URL + ret;
        return Response({"imgurl": ret_url})
