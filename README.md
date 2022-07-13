# prometheus-flask

## 描述：
alertmanager告警信息发送到企业微信群，先发送到prometheus-flask程序，再由prometheus-flask对信息格式解析后再发送到企业微信群中。

## 创建 systemd 文件(ubuntu)   注：非docker运行
[root@zabbix system]# cat /lib/systemd/system/prome-flask.service  
[Unit]  
Description=This is prometheus node exporter  
After=docker.service  
[Service]  
Type=simple  
ExecStart=/usr/bin/python3.6 /data/prometheus-flask/app/main.py -p 5000 -k https://qyapi.weixin.qq.com/cgi-bin/XXXX {替换机器人key}  
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
2、在app目录下指定依赖包，放在rquirements.txt中。             
3、requirements.txt与dockerfile同目录。               
4、docker build .       

### cat Dockerfile     
FROM harbor.xxx.com/python/python:v1.0            
RUN mkdir -p /app          
COPY app /app           
COPY requirements.txt /app/requirements.txt          
WORKDIR /app     
RUN pip install -r /app/requirements.txt        
CMD ["python", "main.py"]       

### OR
### cat Dockerfile     
FROM python:3.10.2    
COPY ./app /app     
COPY ./requirements.txt /app/requirements.txt     
WORKDIR /app      
RUN pip install -r /app/requirements.txt    
CMD ["python", "/app/main.py"]      

### cat requirements.txt    
flask_json == 0.3.4    
flask == 2.0.1   
requests == 2.19.1   
gevent == 20.5.1       # 如果是第二种dockerfile可以不加版本。
