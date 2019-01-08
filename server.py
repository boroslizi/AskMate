from flask import Flask, render_template, redirect, request, session
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions = data_manager.get_all_data("questions")
    sorted_questions = data_manager.sort_by_id(questions)
    return render_template('index.html', questions=sorted_questions)


if __name__ == "__main__":
    app.run(debug=True, port=7000)
