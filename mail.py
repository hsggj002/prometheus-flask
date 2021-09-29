from flask import Flask, request
import sendAlert
import requests
import json
import datetime
app = Flask(__name__)

@app.route('/alertinfo', methods=['POST'])
def alert_data():
    data = request.get_data()
    json_re = json.loads(data)
    json.dumps(json_re)
    sendAlert.send_alert(json_re)
    return json_re

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
