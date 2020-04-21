# coding: utf-8
import os
import time
import json
import random
import execjs
import requests


def _load_js():
    """use python load js"""
    with open('./yp_slider.js', encoding='utf-8') as f:
        js_data = f.read()

    js_text = execjs.compile(js_data)
    return js_text


jst = _load_js()
url = "https://captcha.yunpian.com/v1/jsonp/captcha/get"
header = {
    "Referer": "https://www.yunpian.com/product/captcha",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}
# 浏览器固定参数，用于加密获取i,k参数
data = {
            "browserInfo": [
                {
                    "key": "userAgent",
                    "value": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
                },
                {"key": "language", "value": "zh-CN"},
                {"key": "hardware_concurrency", "value": 8},
                {"key": "resolution", "value": [1440, 900]},
                {"key": "navigator_platform", "value": "MacIntel"}
            ],
            "mobile": "",
            "nativeInfo": {},
            "username": "",
            "options": {
                "sdk": "https://www.yunpian.com/static/official/js/libs/riddler-sdk-0.2.2.js"
            }
    }


def get_captcha():
    """获得滑块验证码的背景和滑块图片地址"""
    cb = jst.call('get_cb')
    encrypt_data = jst.call('encrypt', data)

    params = {
        'cb': cb,
        'i': encrypt_data['i'],
        'k': encrypt_data['k'],
        'captchaId': '974cd565f11545b6a5006d10dc324281'  # 固定值
    }
    resp = requests.get(url, params=params, headers=header)
    result = json.loads(resp.text.replace('ypjsonp(', '').replace(')', ''))
    if result['msg'] == 'ok':
        return {
            'bg': result['data']['bg'],
            'front': result['data']['front']
        }
    return None


def pic_download(url, name):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    save_path = os.getcwd() + '/' + 'images/'

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    img_path = save_path + '{}.jpg'.format(name)
    img_data = requests.get(url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def get_yunpian_pic():
    cur = 1
    for i in range(500):
        res = get_captcha()
        if res:
            pic_download(res['bg'], '{}captcha'.format(cur))
            pic_download(res['front'], '{}slider'.format(cur))
            cur += 1
        #     print('{}成功！'.format(cur))
        # else:
        #     print('{}失败.'.format(cur))
        time.sleep(random.random())


if __name__ == '__main__':
    get_yunpian_pic()