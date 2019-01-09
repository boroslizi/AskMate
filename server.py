from flask import Flask, render_template, redirect, request, session
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions = data_manager.get_all_data("questions")
    sorted_questions = data_manager.sort_by_id(questions)
    return render_template('index.html', questions=sorted_questions)


@app.route('/ask-question', methods=['GET', 'POST'])
def ask_question():
    if request.method == "GET":
        return render_template('question.html')
    else:
        pass
    return render_template('question.html')


@app.route("/question/<question_id>/new-answer")
def route_add_new_answer(question_id):
    return render_template("new_answer.html")


@app.route("/question/<question_id>/new-answer", methods=["POST"])
def add_new_answer(question_id):
    new_answer = request.form["new_answer"]
    data_manager.add_new_answer(new_answer, question_id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=7000)
