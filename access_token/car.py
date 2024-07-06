import requests
import base64
import cv2 as cv

# opencv 图片
def vehicle_detect(img):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image)
    params = {"image":base64_image}
    access_token = '24.8d556aead358d524c6a24f268faac581.2592000.1722846404.282335-89980475'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    num1 = 0
    if response:
        data = response.json()
        num1 = data['vehicle_num']['car']
        for item in data['vehicle_info']:
            location = item['location']
            x1 = location['left']
            y1 = location['top']
            x2 = x1 + location['width']
            y2 = y1 + location['height']
            cv.rectangle(img,(x1,y1),(x2,y2),(0,0,255),1)
        # 定义要绘制的文字
            text = item['type']
            position = (x1, y1-2)
            font = cv.FONT_HERSHEY_SIMPLEX
            font_scale =1
            color = (238, 134, 28)
            thickness = 1
            img = cv.putText(img, text, position, font, font_scale, color, thickness, cv.LINE_AA)
    return img, num1


def people_detect(img):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_num"
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image.tobytes()).decode('utf-8')
    params = {"image": base64_image}
    access_token = '24.8d556aead358d524c6a24f268faac581.2592000.1722846404.282335-89980475'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    # 返回识别到的人体数
    num2 = 0
    if response:
        data = response.json()
        num2 = data.get('person_num', 0)
    return num2