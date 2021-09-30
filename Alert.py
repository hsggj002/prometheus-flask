# -*- coding: UTF-8 -*-
import requests
from flask import jsonify
import json
import datetime

def parse_time(*args):
    times = []
    for dates in args:
        eta_temp = dates
        fd = datetime.datetime.strptime(eta_temp, "%Y-%m-%dT%H:%M:%S.%fZ")
        eta = (fd + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S.%f")
        times.append(eta)
    return times

def alert(types,levels,times,instances):
    params = json.dumps({
        "msgtype": "text",
        "text":
            {
                "content": "**********告警通知**********\n告警类型: {0}\n告警级别: {1}\n故障时间: {2}\n故障实例: {3}".format(types,levels,times[0],instances)
            }
        })

    return params

def recive(types,levels,times,instances):
    params = json.dumps({
        "msgtype": "text",
        "text":
            {
                "content": "**********恢复通知**********\n告警类型: {0}\n告警级别: {1}\n故障时间: {2}\n\n恢复时间: {3}\n故障实例: {4}".format(types,levels,times[0],times[1],instances)
            }
        })

    return params

def webhook_url(params):
    headers = {"Content-type": "application/json"}
    “”“
    *****重要*****
    ”“”
    url = "使用你上面保存的webhook地址"
    r = requests.post(url,params,headers)

def send_alert(json_re):
    for i in json_re['alerts']:
        if i['status'] == 'firing':
            webhook_url(alert(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt']),i['labels']['instance']))
        elif i['status'] == 'resolved':
            webhook_url(recive(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt'],i['endsAt']),i['labels']['instance']))
