import os

from qiniu import Auth, put_file, etag, put_data
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
BUCKET_NAME = 'libra_pic'
EXPIRE = 3600
BUCKET_NAME_URI = os.environ.get('BUCKET_NAME_URI')


def upload_qiniu(data):
    q = Auth(ACCESS_KEY, SECRET_KEY)
    bucket_name = BUCKET_NAME
    key = None
    token = q.upload_token(bucket_name, key, EXPIRE)
    ret, info = put_data(token, key, data)

    if ret is not None:
        return BUCKET_NAME_URI + ret.get('key')
    else:
        raise BaseException(info)
