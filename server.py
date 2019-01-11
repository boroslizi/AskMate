from flask import Flask, render_template, redirect, request, url_for
import time
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions = data_manager.get_all_questions()
    sorted_questions = data_manager.sort_by_id(questions)
    return render_template('index.html', questions=sorted_questions)


@app.route('/question/<question_id>')
def display_question(question_id):

    question = data_manager.get_all_data_by_question_id(question_id, "questions")
    answers = data_manager.get_all_data_by_question_id(question_id, "answers")
    return render_template('display_question.html', question=question, answers=answers)


@app.route('/questions/<question_id>/vote-up', methods=['POST'])
def vote_up(question_id):

    data_manager.vote_for_questions("up", question_id)

    return redirect(url_for('display_question'))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == "GET":
        return render_template('new_question.html')
    else:
        new_question_data = {
            'id': data_manager.get_next_question_id(),
            'submission_time': int(time.time()),
            'view_number': 0,
            'vote_number': 0,
            'title': request.form.get('question'),
            'message': request.form.get('message'),
            'image': request.form.get('image'),
            }

        data_manager.write_new_question(new_question_data)
    return redirect(url_for('display_question', question_id=new_question_data['id']))


@app.route("/question/<question_id>/new-answer")
def route_add_new_answer(question_id):
    return render_template("new_answer.html", question_id=question_id)


@app.route("/question/<question_id>/new-answer", methods=["POST"])
def add_new_answer(question_id):
    new_answer = request.form["new_answer"]
    data_manager.add_new_answer(new_answer, question_id)
    return redirect(url_for("display_question", question_id=question_id))


if __name__ == "__main__":
    app.run(debug=True, port=7000)
