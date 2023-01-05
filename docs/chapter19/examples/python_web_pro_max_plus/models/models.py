import urllib.request
import cv2
import base64
import numpy as np
from .modelAPI import modelAPI




modelapi = modelAPI()


def base64_to_cv2(b64str):
    data = base64.b64decode(b64str.encode('utf8'))
    data = np.fromstring(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data


def cv2_to_base64(image):
    # return base64.b64encode(image)
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tostring()).decode('utf8')


def aimodels(apiname,image_code='',image_url='',rate=0.2):
    img = ''
    if image_code:
        img = base64_to_cv2(image_code)
    elif image_url:
        img = urllib.request.urlopen(image_url)
        img = np.asarray(bytearray(img.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    image,res = getattr(modelapi,apiname)(img, rate = rate, save_dir = None)
    return image,res
