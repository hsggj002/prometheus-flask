# -*- coding: UTF-8 -*-
from doctest import debug_script
from pydoc import describe
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

def alert(alertname,levels,times,instances,summary,description):
    params = json.dumps({
        "msgtype": "text",
        "text":
            {
                "content": "**********告警通知**********\告警名称: {0}\n告警级别: {1}\n故障时间: {2}\n告警实例: {3}\n告警主题：{4}\n告警详情：{5}".format(alertname,levels,times[0],instances,summary,description)
            }
        })

    return params

def recive(altername,levels,times,instances,summary,description):
    params = json.dumps({
        "msgtype": "text",
        "text":
            {
                "content": "**********恢复通知**********\n告警名称: {0}\n告警级别: {1}\n告警时间: {2}\n\n恢复时间: {3}\n告警实例: {4}\n告警主题：{5}\n告警详情：{6}".format(alertname,levels,times[0],times[1],instances,summary,description)
            }
        })

    return params

def webhook_url(params):
    headers = {"Content-type": "application/json"}
    url = "自己的机器人的webhook url"
    r = requests.post(url,params,headers)

def send_alert(json_re):
    print(json_re)
    for i in json_re['alerts']:
        if i['status'] == 'firing':
            webhook_url(alert(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt']),i['labels']['instance'],i['annotations']['summary'],i['annotations']['description']))
        elif i['status'] == 'resolved':
            webhook_url(recive(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt'],i['endsAt']),i['labels']['instance'],i['annotations']['summary'],i['annotations']['description']))
