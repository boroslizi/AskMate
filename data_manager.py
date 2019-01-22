from datetime import datetime
import database_connect


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
    cursor.execute("""INSERT INTO question VALUES (%(id_value)s, %(submission_time_value)s, %(view_number_value)s, 
                    %(vote_number_value)s, %(title_value)s, %(message_value)s, %(image_value)s);""",
                   {'id_value': data['id'],
                    'submission_time_value': data['submission_time'],
                    'view_number_value': data['view_number'],
                    'vote_number_value': data['vote_number'],
                    'title_value': data['title'],
                    'message_value': data['message'],
                    'image_value': data['image']}
                   )


@database_connect.connection_handler
def write_to_answers(cursor, data):
    cursor.execute("""INSERT INTO answer VALUES (%(id_value)s, %(submission_time_value)s, %(vote_number_value)s, 
                    %(question_id_value)s, %(message_value)s, %(image_value)s);""",
                   {'id_value': data['id'],
                    'submission_time_value': data['submission_time'],
                    'vote_number_value': data['vote_number'],
                    'question_id_value': data['question_id'],
                    'message_value': data['message'],
                    'image_value': data['image']}
                   )


@database_connect.connection_handler
def sort_questions_by_time(cursor):
    cursor.execute("""SELECT title, id FROM question
                      ORDER BY submission_time DESC;""")
    sorted_questions = cursor.fetchall()
    return sorted_questions


@database_connect.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""SELECT * FROM question
                      WHERE id=%(id)s;""",
                   {'id': int(question_id)})
    question_data = cursor.fetchall()
    return question_data[0]


@database_connect.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("""SELECT * FROM answer
                      WHERE question_id=%(id)s;""",
                   {'id': int(question_id)})
    answers = cursor.fetchall()
    return answers


@database_connect.connection_handler
def edit_question(cursor, question_id, edited_data):
    cursor.execute("""UPDATE question
                      SET submission_time = %(submission_time_value)s, title = %(title_value)s, 
                      message = %(message_value)s, image = %(image_value)s
                      WHERE id=%(id)s;""",
                   {'submission_time_value': datetime.now(),
                    'title_value': edited_data['title'],
                    'message_value': edited_data['message'],
                    'image_value': edited_data['image'],
                    'id': int(question_id)
                    })


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


def add_new_answer(new_answer, question_id):
    new_data = {
        "id": get_next_answer_id(),
        "submission_time": datetime.now(),
        "vote_number": "0",
        "question_id": question_id,
        "message": new_answer,
        "image": ""
    }
    write_to_answers(new_data)


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
