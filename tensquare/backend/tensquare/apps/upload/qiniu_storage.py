from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from qiniu import Auth
from qiniu import put_data


@deconstructible
class QiniuStorage(Storage):
    def __init__(self, base_url=None, secret_key=None, access_key=None, bucket_name=None):

        if base_url is None:
            base_url = settings.IMAGE_BASE_URL
        self.base_url = base_url

        if secret_key is None:
            secret_key = settings.QINIU_SECRET_KEY
        self.secret_key = secret_key

        if access_key is None:
            access_key = settings.QINIU_ACCESS_KEY
        self.access_key = access_key

        if bucket_name is None:
            bucket_name = settings.QINIU_BUCKET_NAME
        self.bucket_name = bucket_name

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        """
        在FastDFS中保存文件
        :param name: 传入的文件名
        :param content: 文件对象
        :return: 保存到数据库中的FastDFS的文件名
        """
        try:
            q = Auth(self.access_key, self.secret_key)
            token = q.upload_token(self.bucket_name)
            ret, info = put_data(token, None, content.read())
            print(ret, info)
        except Exception as e:
            raise e;

        if info.status_code != 200:
            raise Exception("上传图片失败")
        return ret["key"]

    def exists(self, name):
        return False

    def url(self, name):

        return self.base_url + name
