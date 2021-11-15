from flask import Flask, request, jsonify
from hotel_coupon_fsm import fsm_json

app = Flask(__name__)


@app.route("/")
def display_homepage():
    with open("index.html") as f:
        return f"<script>fsm_json = {fsm_json};</script>" + f.read()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
