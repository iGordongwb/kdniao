# -*- coding:utf-8 -*-
'''
 * ┏┓      ┏┓
 *┏┛┻━━━━━━┛┻┓
 *┃          ┃
 *┃     ━    ┃
 *┃   ┳┛ ┗┳  ┃
 *┃          ┃
 *┃     ┻    ┃
 *┃          ┃
 *┗━┓      ┏━┛
 *  ┃      ┃         CODE IS FAR AWAY FROM BUG
 *  ┃      ┃         WITH THE ANIMAL PROTECTING
 *  ┃      ┗━━━┓
 *  ┃          ┣┓
 *  ┃         ┏┛
 *  ┗┓┓┏━━━┳┓┏┛
 *   ┃┫┫   ┃┫┫
 *   ┗┻┛   ┗┻┛
 *
'''

from urllib import request, parse
import json
import hashlib
import base64


EBusinessID = "1326300"
APIKey = "a91e07e9-a641-4479-b5ef-f3a0e0b68207"


def datasign(jsonstr):
    """将请求数据先进行MD5编码，再base64编码"""
    data = jsonstr + APIKey
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    code_1 = m.hexdigest()
    code_2 = base64.b64encode(code_1.encode("utf-8"))
    return code_2


def sendpost(url, data):
    data = parse.urlencode(data).encode('utf-8')
    headers = {
        "Accept": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept-Encoding": "utf-8"
    }
    req = request.Request(url, headers=headers, data=data)
    get_data = request.urlopen(req).read().decode("utf-8")
    return get_data


def get_company(url, logistic_code):
    request_data1 = {"LogisticCode": logistic_code}
    request_data2 = json.dumps(request_data1, sort_keys=True)
    data_sign = datasign(request_data2)
    post_data = {
        'RequestData': request_data2,
        'EBusinessID': EBusinessID,
        'RequestType': '2002',
        'DataSign': data_sign,
        'DataType': '2'
    }
    json_data = sendpost(url, post_data)
    get_data = json.loads(json_data)
    print(get_data)
    return get_data


def get_traces(url, logistic_code, shipper_code):
    request_data1 = {
        "OrderCode": "",
        "ShipperCode": shipper_code,
        "LogisticCode": logistic_code,
        "IsHandleInfo": "0"}
    request_data2 = json.dumps(request_data1, sort_keys=True)
    data_sign = datasign(request_data2)
    post_data = {
        'RequestData': request_data2,
        'EBusinessID': EBusinessID,
        'RequestType': '1002',
        'DataSign': data_sign,
        'DataType': '2'
    }
    json_data = sendpost(url, post_data)
    get_data = json.loads(json_data)
    return get_data


def recognise(logistic_code):
    """输出数据"""
    url = "http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx"
    shipper = get_company(url, logistic_code)
    if not any(shipper['Shippers']):
        print("未查找到快递信息，请检查快递单号是否有误！")
    else:
        print("已查到该", str(shipper['Shippers'][0]['ShipperName']) + "(" +
              str(shipper['Shippers'][0]['ShipperCode']) + ")", logistic_code)
        data = get_traces(
            url,
            logistic_code,
            shipper['Shippers'][0]['ShipperCode'])
        if not data['Success'] or not any(data['Traces']):
            print(data['Reason'])
        else:
            state = data['State']
            state_str = "无轨迹"
            if state == "1":
                state_str = "已揽收"
            elif state == "2":
                state_str = "在途中"
            elif state == "3":
                state_str = "签收"
            elif state == "4":
                state_str = "问题件"
            print("当前状态：" + state_str)
            print("-----------------------------------")
            i = 1
            for item in data['Traces']:
                print(
                    i,
                    item['AcceptTime'],
                    item['AcceptStation'])
                i += 1
                print("\n")
    pass


while True:
    code = input("请输入快递单号(输入esc退出)：")
    code = code.strip()
    if code == "esc":
        break
    recognise(code)
