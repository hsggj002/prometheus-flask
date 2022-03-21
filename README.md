# prometheus-flask

## 描述：
alertmanager告警信息发送到企业微信群，先发送到prometheus-flask程序，再由prometheus-flask对信息格式解析后再发送到企业微信群中。

## 创建 systemd 文件
[root@zabbix system]# cat prome-flask.service
[Unit]
Description=This is prometheus node exporter
After=docker.service
[Service]
Type=simple
ExecStart=/usr/bin/python3.6 /data/prometheus-flask/main.py -p 5000 -k https://qyapi.weixin.qq.com/cgi-bin/XXXX {替换机器人key}
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
[Install]
WantedBy=multi-user.target

## 启动：
systemctl start prome-flask.service
systemctl enable prome-flask.service

