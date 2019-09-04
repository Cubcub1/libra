import os

from qiniu import Auth, put_file, etag, put_data
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
ACCESS_KEY="2DgCpPTojSccIoYVp0sEEyw0PgYPBN_fGnkZ3VfW"
SECRET_KEY="zMJwZ-2I9_UKOtNuBIzqh_IuK8spC3fghat8-QuB"
BUCKET_NAME = 'libra_pic'
EXPIRE = 3600
BUCKET_NAME_URI = "http://px1h00469.bkt.clouddn.com/"


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
