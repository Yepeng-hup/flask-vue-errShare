from flask import Blueprint, jsonify

test = Blueprint("test", __name__)


@test.route("/")
def test_check():
    return jsonify({"code": 200})