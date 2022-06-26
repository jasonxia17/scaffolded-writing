from flask import Flask, request, render_template
import importlib

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def handle_submit() -> str:
    problem = importlib.import_module("problems.partition_digits_basic_version")

    tokenized_sentence = request.get_json()
    data = {
        "submitted_answers": {"subproblem_definition": tokenized_sentence},
        "partial_scores": {},
        "feedback": {},
    }

    problem.grade(data)

    return data["feedback"]["subproblem_definition"]


@app.route("/")
def display_homepage() -> str:
    problem = importlib.import_module("problems.partition_digits_basic_version")

    data = {"params": {}}
    problem.generate(data)

    return render_template(
        'index.html',
        statement=problem.statement,
        cfg=data["params"]["subproblem_definition_cfg"]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
