from flask import Flask

from core.conf import fk_host, fk_port, fk_debug
from view.test import test

app = Flask(__name__)
app.secret_key = 'ertyuiplbcvrtRTYssa345oplyt'
app.config['JSON_AS_ASCII'] = False
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Shanghai'
app.register_blueprint(test)

if __name__ == "__main__":
    app.run(debug=fk_debug, host=fk_host, port=fk_port)
