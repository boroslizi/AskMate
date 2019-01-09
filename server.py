from flask import Flask, render_template, redirect, request
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions = data_manager.get_all_data("questions")
    sorted_questions = data_manager.sort_by_id(questions)
    return render_template('index.html', questions=sorted_questions)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == "GET":
        return render_template('new_question.html')
    else:
        new_question_data = {
            'id': data_manager.get_next_question_id(),
            'submission_time': 1234567890,  # TODO: datetime?
            'view_number': 0,
            'vote_number': 0,
            'title': request.form.get('question'),
            'message': request.form.get('message'),
            'image': request.form.get('image'),
            }

        data_manager.write_new_question(new_question_data)

    return render_template('new_question.html')


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
