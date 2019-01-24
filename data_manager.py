from datetime import datetime
import connection


@connection.connection_handler
def get_all_answers(cursor):
    cursor.execute("""SELECT * FROM answer;""")
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""SELECT * FROM question;""")
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_all_question_headers(cursor):
    cursor.execute("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_NAME = 'question';""")
    table_headers = cursor.fetchall()
    return table_headers


@connection.connection_handler
def get_all_answer_headers(cursor):
    cursor.execute("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_NAME = 'answer';""")
    table_headers = cursor.fetchall()
    return table_headers


"""
@connection.connection_handler
def write_to_questions(cursor, data):
    placeholders = ', '.join(['%s'] * len(data))
    qry = "INSERT INTO question VALUES (%s)" % (placeholders)
    cursor.execute(qry, data.values())
"""


@connection.connection_handler
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


@connection.connection_handler
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


@connection.connection_handler
def sort_questions_by_time(cursor):
    cursor.execute("""SELECT title, id FROM question
                      ORDER BY submission_time DESC;""")
    sorted_questions = cursor.fetchall()
    return sorted_questions


@connection.connection_handler
def get_next_question_id(cursor):
    try:
        cursor.execute("""SELECT MAX(id) from question;""")
        new_id = cursor.fetchall()[0]['max'] + 1
    except KeyError:
        new_id = 0
    return new_id


@connection.connection_handler
def get_next_answer_id(cursor):
    try:
        cursor.execute("""SELECT MAX(id) from answer;""")
        new_id = cursor.fetchall()[0]['max'] + 1
    except KeyError:
        new_id = 0
    return new_id


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""SELECT * FROM question
                      WHERE id=%(id)s;""",
                   {'id': question_id})
    question_data = cursor.fetchall()[0]
    return question_data


@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("""SELECT * FROM answer
                      WHERE question_id=%(id)s;""",
                   {'id': question_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def edit_question(cursor, question_id, edited_data):
    cursor.execute("""UPDATE question
                      SET submission_time = %(submission_time_value)s, title = %(title_value)s, 
                      message = %(message_value)s, image = %(image_value)s
                      WHERE id=%(id)s;""",
                   {'submission_time_value': datetime.now(),
                    'title_value': edited_data['title'],
                    'message_value': edited_data['message'],
                    'image_value': edited_data['image'],
                    'id': question_id})


@connection.connection_handler
def delete_question_by_id(cursor, question_id):
    cursor.execute("""DELETE FROM answer
                      WHERE question_id=%(id)s;""",
                   {'id': question_id})
    cursor.execute("""DELETE FROM question
                      WHERE id=%(id)s;""",
                   {'id': question_id})


@connection.connection_handler
def delete_answer_by_id(cursor, answer_id):
    cursor.execute("""DELETE FROM answer
                      WHERE id=%(id)s;""",
                   {'id': answer_id})


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

@connection.connection_handler
def get_all_answers_by_id_ordered_by_vote_number(cursor, question_id):
    cursor.execute("""SELECT * FROM answer
                      WHERE question_id=%(id)s
                      ORDER BY vote_number DESC;""",
                   {'id': question_id})
    answers = cursor.fetchall()
    return answers

@connection.connection_handler
def vote_up_for_questions(cursor, question_id):
    cursor.execute("""UPDATE question
                          SET vote_number = vote_number + 1
                          WHERE id=%(id)s;""",
                   {'id': int(question_id)})
@connection.connection_handler
def vote_down_for_questions(cursor, question_id):
    cursor.execute("""UPDATE question
                          SET vote_number = vote_number - 1
                          WHERE id=%(id)s;""",
                   {'id': int(question_id)})
@connection.connection_handler
def vote_up_for_answers(cursor, answer_id):
    cursor.execute("""UPDATE answer
                          SET vote_number = vote_number + 1
                          WHERE id = %(id)s;""",
                   {'id': answer_id})
@connection.connection_handler
def vote_down_for_answers(cursor, answer_id):
    cursor.execute("""UPDATE answer
                          SET vote_number = vote_number - 1
                          WHERE id = %(id)s;""",
                   {'id': answer_id})