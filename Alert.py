# -*- coding: UTF-8 -*-
from doctest import debug_script
from pydoc import describe
from flask import jsonify
import requests
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

def alert(status,alertnames,levels,times,ins,instance,description):
    params = json.dumps({
        "msgtype": "markdown",
        "markdown":
            {
                "content": "## <font color=\"red\">告警通知: {0}</font>\n**告警名称:** <font color=\"warning\">{1}</font>\n**告警级别:** {2}\n**告警时间:** {3}\n{4}: {5}\n**告警详情:** <font color=\"comment\">{6}</font>".format(status,alertnames,levels,times[0],ins,instance,description)
            }
        })

    return params

def recive(status,alertnames,levels,times,ins,instance,description):
    params = json.dumps({
        "msgtype": "markdown",
        "markdown":
            {
                "content": "## <font color=\"info\">恢复通知: {0}</font>\n**告警名称:** <font color=\"warning\">{1}</font>\n**告警级别:** {2}\n**告警时间:** {3}\n{4}: {5}\n**告警详情:** <font color=\"comment\">{6}</font>".format(status,alertnames,levels,times[0],times[1],ins,instance,description)
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
                webhook_url(alert(i['status'],i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt']),'故障实例',i['labels']['instance'],i['annotations']['description']),url_key)
            elif "namespace" in i['labels']:
                webhook_url(alert(i['status'],i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt']),'名称空间',i['labels']['namespace'],i['annotations']['description']),url_key)
            elif "Watchdog" in i['labels']['alertname']:
                webhook_url(alert(i['status'],i['labels']['alertname'],'0','0','0','0','0'),url_key)
        elif i['status'] == 'resolved':
            if "instance" in i['labels']:
                webhook_url(recive(i['status'],i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt'],i['endsAt']),'故障实例',i['labels']['instance'],i['annotations']['description']),url_key)
            elif "namespace" in i['labels']:
                webhook_url(recive(i['status'],i['labels']['alertname'],i['labels']['severity'],parse_time(i['startsAt'],i['endsAt']),'名称空间',i['labels']['namespace'],i['annotations']['description']),url_key)
            elif "Watchdog" in i['labels']['alertname']:
                webhook_url(alert(i['status'],i['labels']['alertname'],'0','0','0','0','0'),url_key)
