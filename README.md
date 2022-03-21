# prometheus-flask

## 描述：
alertmanager告警信息发送到企业微信群，先发送到prometheus-flask程序，再由prometheus-flask对信息格式解析后再发送到企业微信群中。

## 创建 systemd 文件(ubuntu)
[root@zabbix system]# cat /lib/systemd/system/prome-flask.service  
[Unit]  
Description=This is prometheus node exporter  
After=docker.service  
[Service]  
Type=simple  
ExecStart=/usr/bin/python3.6 /data/prometheus-flask/app.py -p 5000 -k https://qyapi.weixin.qq.com/cgi-bin/XXXX {替换机器人key}  
ExecReload=/bin/kill -HUP $MAINPID  
KillMode=process  
Restart=on-failure  
[Install]  
WantedBy=multi-user.target  

### centos systemd文件位置：/usr/lib/systemd/system

## 启动：
systemctl start prome-flask.service
systemctl enable prome-flask.service

