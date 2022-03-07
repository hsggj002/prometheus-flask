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

def alert(types,levels,times,ins,instance):
    params = json.dumps({
        "msgtype": "text",
        "text":
            {
                "content": "**********告警通知**********\n告警类型: {0}\n告警级别: {1}\n故障时间: {2}\n{3}: {4}".format(types,levels,times[0],ins,instance)
            }
        })

    return params

def recive(types,levels,times,ins,instance):
    params = json.dumps({
        "msgtype": "text",
        "text":
            {
                "content": "**********恢复通知**********\n告警类型: {0}\n告警级别: {1}\n故障时间: {2}\n\n恢复时间: {3}\n{4}: {5}".format(types,levels,times[0],times[1],ins,instance)
            }
        })

    return params

def webhook_url(params,url_key):
    headers = {"Content-type": "application/json"}
    """
    *****重要*****
    """
    url = "{}".format(url_key)
    r = requests.post(url,params,headers)

def send_alert(json_re,url_key):
    for i in json_re['alerts']:
        if i['status'] == 'firing':
            if "instance" in i['labels']:
                webhook_url(alert(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt']),'故障实例',i['labels']['instance']),url_key)
            elif "namespace" in i['labels']:
                webhook_url(alert(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt']),'名称空间',i['labels']['namespace']),url_key)
            elif "Watchdog" in i['labels']['alertname']:
                webhook_url(alert(i['labels']['alertname'],'0','0','0','0'),url_key)
        elif i['status'] == 'resolved':
            if "instance" in i['labels']:
                webhook_url(recive(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt'],i['endsAt']),'故障实例',i['labels']['instance']),url_key)
            elif "namespace" in i['labels']:
                webhook_url(recive(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt'],i['endsAt']),'名称空间',i['labels']['namespace']),url_key)
            elif "Watchdog" in i['labels']['alertname']:
                webhook_url(alert(i['labels']['alertname'],'0','0','0','0'),url_key)
