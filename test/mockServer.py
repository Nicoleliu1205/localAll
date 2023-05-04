from flask import abort, jsonify, Flask, request, Response

from gevent import pywsgi
app = Flask(__name__)
# 增加配置，支持中文显示
app.config['JSON_AS_ASCII'] = False

taskss = {
    "code": 0,
    "msg": "OK",
    "data": {
        "waybillNumber": "1526351",
        "serviceMode": "10",
        "waybillStatus": "10",
        "deliveryAbbreviationAddress": "深圳",
        "pickupAbbreviationAddress": "深圳"
    },
    "traceId": "dp1r"
}

tasksl = {
    "code": 0,
    "data": {
        "waybillStatus": "10",
        "deliveryAbbreviationAddress": "深圳",
    },
}


@app.route('/task/ss', methods=['GET', 'POST'])  # 访问网址：http://127.0.0.1:6868/task/ss
def get_taskss():
    return jsonify(taskss)


@app.route('/task/sl', methods=['GET', 'POST'])  # 访问网址：http://127.0.0.1:6868/task/sl
def get_tasksl():
    return jsonify(tasksl)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6868, debug=True)
    # server = pywsgi.WSGIServer(('0.0.0.0', 12345), app)
    # server.serve_forever()
