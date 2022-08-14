from flask import Flask, request, render_template, redirect
import importlib

app = Flask(__name__)

@app.route("/")
def display_homepage():
    return render_template("dp_intro.html")

FREE_RESPONSE_PROBLEMS = {"max_halloween_profit", "coloring_mistakes"}

@app.route("/<problem_name>/problem")
def display_problem(problem_name: str) -> str:
    if problem_name in FREE_RESPONSE_PROBLEMS:
        return render_template(problem_name + ".html")

    problem = importlib.import_module("problems." + problem_name)

    data = {"params": {}}
    problem.generate(data)

    return render_template(
        'autograded_problem.html',
        statement=problem.statement,
        cfg=data["params"]["subproblem_definition_cfg"]
    )

@app.route("/<problem_name>/submit", methods=["POST"])
def handle_submit(problem_name: str) -> str:
    problem = importlib.import_module("problems." + problem_name)

    tokenized_sentence = request.get_json()
    data = {
        "submitted_answers": {"subproblem_definition": tokenized_sentence},
        "partial_scores": {},
        "feedback": {},
    }

    problem.grade(data)

    return data["feedback"].get("subproblem_definition", "Good job!")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
