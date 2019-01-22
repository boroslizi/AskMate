import os
from datetime import datetime
import connection
import database_connect

QUESTIONS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWERS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'


@database_connect.connection_handler
def get_all_answers(cursor):
    cursor.execute("""SELECT * FROM answer;""")
    answers = cursor.fetchall()
    return answers


@database_connect.connection_handler
def get_all_questions(cursor):
    cursor.execute("""SELECT * FROM question;""")
    questions = cursor.fetchall()
    return questions


@database_connect.connection_handler
def get_all_question_headers(cursor):
    cursor.execute("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_NAME = 'question';""")
    table_headers = cursor.fetchall()
    print(type(table_headers))
    return table_headers


@database_connect.connection_handler
def get_all_answer_headers(cursor):
    cursor.execute("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_NAME = 'answer';""")
    table_headers = cursor.fetchall()
    return table_headers


@database_connect.connection_handler
def write_to_questions(cursor, data):
    placeholders = ', '.join(['%s'] * len(data))
    qry = "INSERT INTO question VALUES (%s)" % (placeholders)
    cursor.execute(qry, data.values())

@database_connect.connection_handler
def write_to_questions(cursor, data):
    headers = get_all_question_headers()
    cursor.execute("""INSERT INTO question VALUES (%(id_value)s, %(submission_time_value)s, %(view_number_value)s, %(vote_number_value)s, %(title_value)s,
                    %(message_value)s, %(image_value)s);
                    """,
                   {'id_value': data['id'],
                    'submission_time_value': data['submission_time'],
                    'view_number_value': data['view_number'],
                    'vote_number_value': data['vote_number'],
                    'title_value': data['title'],
                    'message_value': data['message'],
                    'image_value': data['image']}
                   )


@database_connect.connection_handler
def sort_questions_by_time(cursor):
    cursor.execute("""SELECT title FROM question
                      ORDER BY submission_time DESC;""")
    sorted_questions = cursor.fetchall()
    return sorted_questions


def write_new_question(data):
    write_to_questions(data)


def get_next_answer_id():
    if len(get_all_answers()) == 0:
        return 0
    latest_answer_id = get_all_answers()[-1]["id"]
    new_id = str(int(latest_answer_id) + 1)
    return new_id


def get_next_question_id():
    if len(get_all_questions()) == 0:
        return 0
    latest_question_id = get_all_questions()[-1]["id"]
    new_id = str(int(latest_question_id) + 1)
    return new_id


def add_new_question():
    new_question_data = {
        'id': get_next_question_id(),
        'submission_time': datetime.now(),
        'view_number': 0,
        'vote_number': 0
        }
    return new_question_data


def edit_question(question_id):
    question_data = get_all_data_by_question_id(question_id, "questions")
    edited_question_data = {
        'id': question_id,
        'submission_time': datetime-now(),
        'view_number': int(question_data['view_number']),
        'vote_number': int(question_data['vote_number'])
        }
    return edited_question_data


def get_edited_question_to_write(edited_question):
    question_id = edited_question['id']
    connection.edit_file(QUESTIONS, edited_question, question_id)


def add_new_answer(new_answer, question_id):
    new_data = {
        "id": get_next_answer_id(),
        "submission_time": datetime.now(),
        "vote_number": "0",
        "question_id": question_id,
        "message": new_answer,
        "image": ""
    }
    connection.write_to_file(ANSWERS, new_data)


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


def delete_question_by_id(question_id):
    connection.delete_from_file(QUESTIONS, question_id)


def delete_answer_by_id(answer_id):
    connection.delete_from_file(ANSWERS, answer_id)
