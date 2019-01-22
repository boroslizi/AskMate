from flask import Flask, render_template, redirect, request, url_for
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    sorted_questions = data_manager.sort_questions_by_time()
    return render_template('index.html', questions=sorted_questions)


@app.route('/question/<question_id>')
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template('display_question.html', question=question, answers=answers)


@app.route('/questions/<question_id>/vote-up', methods=['POST'])
def vote_up(question_id):
    data_manager.vote_for_questions("up", question_id)
    return redirect(url_for('display_question'))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == "GET":
        return render_template('new_question.html')

    new_question_all_data = data_manager.add_new_question()
    new_question_all_data.update(
        {
            'title': request.form.get('question'),
            'message': request.form.get('message'),
            'image': request.form.get('image')
        }
    )
    data_manager.write_to_questions(new_question_all_data)
    return redirect(url_for('display_question', question_id=new_question_all_data['id']))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == "GET":
        question = data_manager.get_all_data_by_question_id(question_id, "questions")
        return render_template('edit_question.html', question=question)

    edited_question_data = data_manager.edit_question(question_id)
    edited_question_data.update(
        {
            'title': request.form.get('question'),
            'message': request.form.get('message'),
            'image': request.form.get('image')
        }
    )
    data_manager.get_edited_question_to_write(edited_question_data)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question_by_id(question_id)
    return redirect(url_for('index'))


@app.route("/question/<question_id>/new-answer")
def route_add_new_answer(question_id):
    return render_template("new_answer.html", question_id=question_id)


@app.route("/question/<question_id>/new-answer", methods=["POST"])
def add_new_answer(question_id):
    new_answer = request.form["new_answer"]
    data_manager.add_new_answer(new_answer, question_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    data_manager.delete_answer_by_id(answer_id)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=7000)
