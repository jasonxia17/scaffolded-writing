from flask import Flask, request
import json

from cfg import cfg_as_json
from hotel_coupon_grader import Grader

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def handle_submit() -> str:
    tokenized_sentence = request.get_json()

    if not isinstance(tokenized_sentence, list):
        return "error"

    print(tokenized_sentence)
    return Grader(tokenized_sentence).generate_feedback()


@app.route("/")
def display_homepage() -> str:
    with open("index.html") as f:
        return f"<script>cfg = {json.dumps(cfg_as_json)};</script>" + f.read()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
