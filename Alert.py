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

def alert(alertname,levels,times,instances,summary,description,status):
    params = json.dumps({
        "msgtype": "markdown",
        "markdown":
            {
                "content": "## <font color=\"info\">#告警通知： {6}</font> \n**告警名称：** <font color=\"warning\">{0}</font>\n**告警级别：** {1}\n**告警时间：** {2}\n**告警实例：** {3}\n**告警主题：** {4}\n**告警详情：**\n<font color=\"comment\"> {5}</font>".format(alertname,levels,times[0],instances,summary,description,status)
            }
        })

    return params

def recive(alertname,levels,times,instances,summary,description,status):
    params = json.dumps({
        "msgtype": "markdown",
        "markdown":
            {
                "content": "## <font color=\"info\">#恢复通知： {7}</font> \n**告警类型：** <font color=\"warning\">{0}</font>\n**告警级别：** {1}\n**告警时间：** {2}\n**恢复时间：** {3}\n**告警实例：** {4}\n**告警主题：** {5}\n**告警详情：**\n  <font color=\"comment\">{6}</font>".format(alertname,levels,times[0],times[1],instances,summary,description,status)
            }
        })

    return params

def webhook_url(params):
    headers = {"Content-type": "application/json"}
    url = "xxx"
    r = requests.post(url,params,headers)

def send_alert(json_re):
    for i in json_re['alerts']:
        if i['status'] == 'firing':
            webhook_url(alert(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt']),i['labels']['instance'],i['annotations']['summary'],i['annotations']['description'],i['status']))
        elif i['status'] == 'resolved':
            webhook_url(recive(i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt'],i['endsAt']),i['labels']['instance'],i['annotations']['summary'],i['annotations']['description'],i['status']))
