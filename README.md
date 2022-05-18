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

创建docker镜像：      
1、创建app目录，将代码文件拷贝到app下。     
2、在app目录下指定依赖包，放在/app/rquirements.txt中。       
3、docker build .       

### cat Dockerfile     
FROM python      
COPY ./app /app    
COPY ./requirements.txt /app/requirements.txt      
WORKDIR /app     
RUN pip install -r /app/requirements.txt      
CMD ["python", "/app/main.py"]    

### cat requirements.txt    
flask_json == 0.3.4    
flask == 2.0.1   
requests == 2.19.1   

