from flask import Flask, jsonify

app = Flask(__name__)
app.secret_key = 'ddfkowfwfmfddddcccvvvrtRTYssa345oplyt'
app.config['JSON_AS_ASCII'] = False
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Shanghai'


@app.route('/')
def test():
    return jsonify({"code": 200})



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8088)

