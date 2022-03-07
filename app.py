from flask import Flask, request
from flask_json import as_json
from flask import jsonify
import sys
import Alert
import argparse
import requests
import json
import datetime
app = Flask(__name__)

@app.route('/alertinfo', methods=['POST'])
def alert_data():
    data = request.get_data()
    json_re = json.loads(data)
    json.dumps(json_re)
    Alert.send_alert(json_re, args.key)
    return json_re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="The service port")
    parser.add_argument("-k", "--key", type=str, help="The webhook url key")
    args = parser.parse_args()

    if not args.port or not args.key:
        parser.print_help()
        sys.exit(0)
        
    app.run(host="0.0.0.0", port=args.port)
