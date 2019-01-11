import os
import time
import connection

QUESTIONS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWERS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'


def get_all_data(file):
    if file == "questions":
        return connection.get_all_data(QUESTIONS)
    elif file == "answers":
        return connection.get_all_data(ANSWERS)


def sort_by_id(questions):
    submission_times = [question['submission_time'] for question in questions]
    submission_times.sort(reverse=True)
    sorted_questions = []
    for time in submission_times:
        for question in questions:
            if time in question.values():
                sorted_questions.append(question)
    return sorted_questions


def write_new_question(data):
    connection.write_to_file(QUESTIONS, data)


def get_new_answer_id():
    latest_answer_id = get_all_data("answers")[-1]["id"]
    new_id = str(int(latest_answer_id) + 1)
    return new_id


def add_new_answer(new_answer, question_id):
    new_data = {
        "id": question_id,
        "submission_time": int(time.time()),
        "vote_number": "0",
        "question_id": question_id,
        "message": new_answer,
        "image": ""
    }
    connection.write_to_file(ANSWERS, new_data)


def get_next_question_id():
    return connection.get_next_id(QUESTIONS)


def get_all_data_by_question_id(question_id, source):
    details = []
    if source == "questions":
        file = connection.get_all_data(QUESTIONS)
        for question in file:
            if question_id == question['id']:
                details = question
                details['vote_number'] = int(details['vote_number'])
    else:
        file = connection.get_all_data(ANSWERS)
        for answer in file:
            if question_id == answer['question_id']:
                details.append(answer)
    return details


def vote_for_questions(vote, question_id):
    question_to_vote = get_all_data_by_question_id(question_id, "questions")
    if vote == "up":
        question_to_vote['vote_number'] += 1
    else:
        question_to_vote['vote_number'] -= 1
    connection.write_to_file(QUESTIONS, connection.get_all_data(QUESTIONS))

