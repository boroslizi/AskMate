from flask import Flask, render_template, redirect, request, url_for
import data_manager

app = Flask(__name__)

latest_opened_question_id = 0


@app.route('/')
def index():
    latest_questions = data_manager.get_latest_questions(5)
    return render_template('index.html', questions=latest_questions)


@app.route('/list')
def route_to_all_questions():
    sorted_questions = data_manager.sort_questions_by_time()
    return render_template('all_questions.html', questions=sorted_questions)


@app.route('/search', methods=['POST'])
def search():
    search_phrase = request.form.get('search_phrase')
    questions = data_manager.search_in_questions(search_phrase)
    answers = data_manager.search_in_answers(search_phrase)
    return render_template('search.html', search_phrase=search_phrase, questions=questions, answers=answers)


@app.route('/question/<question_id>')
def display_question(question_id):
    global latest_opened_question_id
    latest_opened_question_id = question_id
    question = data_manager.get_question_by_id(question_id)
    comments = data_manager.get_comments_by_question_id(question_id)
    answers = data_manager.get_all_answers_by_id_ordered_by_vote_number(question_id)
    return render_template('display_question.html', question=question, answers=answers, comments=comments)


@app.route('/questions/<question_id>/vote-up', methods=['POST'])
def question_vote_up(question_id):
    data_manager.vote_up_for_questions(question_id)
    return redirect(url_for('display_question', question_id=question_id))

@app.route('/questions/<question_id>/vote-down', methods=['POST'])
def question_vote_down(question_id):
    data_manager.vote_down_for_questions(question_id)
    return redirect(url_for('display_question', question_id=question_id))

@app.route('/answers/<question_id>/<answer_id>/vote-up', methods=['POST'])
def answer_vote_up(question_id, answer_id):
    data_manager.vote_up_for_answers(answer_id)
    return redirect(url_for('display_question', question_id=question_id))

@app.route('/questions/<question_id>/<answer_id>/vote-down', methods=['POST'])
def answer_vote_down(question_id, answer_id):
    data_manager.vote_down_for_answers(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


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
        question = data_manager.get_question_by_id(question_id)
        return render_template('edit_question.html', question=question)

    edited_question_data = {
            'title': request.form.get('question'),
            'message': request.form.get('message'),
            'image': request.form.get('image')
            }
    data_manager.edit_question(question_id, edited_question_data)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == "GET":
        question = data_manager.get_question_by_id(question_id)
        return render_template('new_comment_q.html', question=question)

    new_comment_to_question = {
        'message': request.form.get('comment'),
        'type': 'question',
        'question_id': question_id
        }
    data_manager.write_to_comments(new_comment_to_question)
    global latest_opened_question_id
    return redirect(url_for('display_question', question_id=latest_opened_question_id))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question_by_id(question_id)
    return redirect(url_for('route_to_all_questions'))


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
    global latest_opened_question_id
    return redirect(url_for('display_question', question_id=latest_opened_question_id))


if __name__ == "__main__":
    app.run(debug=True, port=7000)
