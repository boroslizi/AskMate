from datetime import datetime
import connection
import util


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
def get_all_comments(cursor):
    cursor.execute("""SELECT * FROM comment;""")
    comments = cursor.fetchall()
    return comments


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


@connection.connection_handler
def get_new_question_id_by_title(cursor, title):
    cursor.execute("""SELECT id FROM question
                      WHERE title=%(title_value)s;""",
                   {'title_value': title})
    question_id = cursor.fetchall()[0]['id']
    return question_id


@connection.connection_handler
def write_to_questions(cursor, data):
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                    VALUES (%(submission_time_value)s, %(view_number_value)s, 
                    %(vote_number_value)s, %(title_value)s, %(message_value)s, %(image_value)s, %(user_id_value)s);""",
                   {'submission_time_value': data['submission_time'],
                    'view_number_value': data['view_number'],
                    'vote_number_value': data['vote_number'],
                    'title_value': data['title'],
                    'message_value': data['message'],
                    'image_value': data['image'],
                    'user_id-value': data['user_id']})


@connection.connection_handler
def write_to_answers(cursor, data):
    cursor.execute("""INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id) 
                    VALUES (%(submission_time_value)s, %(vote_number_value)s, 
                    %(question_id_value)s, %(message_value)s, %(image_value)s, %(user_id_value)s);""",
                   {'submission_time_value': data['submission_time'],
                    'vote_number_value': data['vote_number'],
                    'question_id_value': data['question_id'],
                    'message_value': data['message'],
                    'image_value': data['image'],
                    'user_id_value': data['user_id']})


@connection.connection_handler
def write_to_comments(cursor, data):
    cursor.execute("""INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id) 
                    VALUES (%(question_id_value)s, %(answer_id_value)s, 
                    %(message_value)s, %(submission_time_value)s, %(edited_count_value)s, %(user_id_value)s);""",
                   {'question_id_value': data['question_id'] if data['type'] == 'question' else None,
                    'answer_id_value': data['answer_id'] if data['type'] == 'answer' else None,
                    'message_value': data['message'],
                    'submission_time_value': datetime.now().replace(microsecond=0),
                    'edited_count_value': None,
                    'user_id_value': data['user_id']})


@connection.connection_handler
def sort_questions_by_time(cursor):
    cursor.execute("""SELECT title, id FROM question
                      ORDER BY submission_time DESC;""")
    sorted_questions = cursor.fetchall()
    return sorted_questions


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""SELECT * FROM question
                      WHERE id=%(id)s;""",
                   {'id': question_id})
    question_data = cursor.fetchall()[0]
    return question_data


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""SELECT * FROM answer
                      WHERE id=%(id)s;""",
                   {'id': answer_id})
    answer_data = cursor.fetchall()[0]
    return answer_data


@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute("""SELECT * FROM comment
                      WHERE id=%(id)s;""",
                   {'id': comment_id})
    comment_data = cursor.fetchall()[0]
    return comment_data


@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("""SELECT * FROM answer
                      WHERE question_id=%(id)s;""",
                   {'id': question_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_comments_by_question_id(cursor, question_id):
    cursor.execute("""SELECT * FROM comment
                      WHERE question_id=%(id)s;""",
                   {'id': question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_answer_comments_by_question_id(cursor, question_id):
    cursor.execute("""SELECT * FROM comment
                      WHERE question_id=%(id)s;""",
                   {'id': question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def edit_question(cursor, question_id, edited_data):
    cursor.execute("""UPDATE question
                      SET submission_time = %(submission_time_value)s, title = %(title_value)s, 
                      message = %(message_value)s, image = %(image_value)s
                      WHERE id=%(id)s;""",
                   {'submission_time_value': datetime.now().replace(microsecond=0),
                    'title_value': edited_data['title'],
                    'message_value': edited_data['message'],
                    'image_value': edited_data['image'],
                    'id': question_id})


@connection.connection_handler
def edit_answer(cursor, answer_id, edited_data):
    cursor.execute("""UPDATE answer
                      SET submission_time = %(submission_time_value)s, message = %(message_value)s,
                      image = %(image_value)s
                      WHERE id=%(id)s;""",
                   {'submission_time_value': datetime.now().replace(microsecond=0),
                    'message_value': edited_data['message'],
                    'image_value': edited_data['image'],
                    'id': answer_id})


@connection.connection_handler
def edit_comment(cursor, comment_id, edited_data):
    cursor.execute("""UPDATE comment
                      SET submission_time = %(submission_time_value)s, message = %(message_value)s,
                      edited_count = %(edited_count_value)s
                      WHERE id=%(id)s;""",
                   {'message_value': edited_data['message'],
                    'submission_time_value': datetime.now().replace(microsecond=0),
                    'edited_count_value': edited_data['edited_count'],
                    'id': comment_id})


@connection.connection_handler
def delete_question_by_id(cursor, question_id):
    cursor.execute("""DELETE FROM comment
                      WHERE question_id=%(id)s;""",
                   {'id': question_id})
    cursor.execute("""SELECT id FROM answer
                      WHERE question_id=%(id)s;""",
                   {'id': question_id})
    answer_ids = cursor.fetchall()
    for answer_id in answer_ids:
        delete_answer_by_id(answer_id['id'])
    cursor.execute("""DELETE FROM question
                      WHERE id=%(id)s;""",
                   {'id': question_id})


@connection.connection_handler
def delete_answer_by_id(cursor, answer_id):
    cursor.execute("""DELETE FROM comment
                      WHERE answer_id=%(id)s;""",
                   {'id': answer_id})
    cursor.execute("""DELETE FROM answer
                      WHERE id=%(id)s;""",
                   {'id': answer_id})


@connection.connection_handler
def delete_comment_by_id(cursor, comment_id):
    cursor.execute("""DELETE FROM comment
                      WHERE id=%(id)s;""",
                   {'id': comment_id})


def add_new_question():
    new_question_data = {
        'submission_time': datetime.now().replace(microsecond=0),
        'view_number': 0,
        'vote_number': 0
        }
    return new_question_data


def add_new_answer(new_answer, user_id, question_id):
    new_data = {
        "submission_time": datetime.now().replace(microsecond=0),
        "vote_number": "0",
        "question_id": question_id,
        "message": new_answer,
        "image": "",
        "user_id": user_id
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


@connection.connection_handler
def search_in_questions(cursor, search_phrase):
    cursor.execute("""SELECT * FROM question
                      WHERE title LIKE %(search_phrase)s OR message LIKE %(search_phrase)s;""",
                   {'search_phrase': '%' + search_phrase + '%'})
    question_data = cursor.fetchall()
    return question_data


@connection.connection_handler
def search_in_answers(cursor, search_phrase):
    cursor.execute("""SELECT * FROM answer
                      WHERE message LIKE %(search_phrase)s;""",
                   {'search_phrase': '%' + search_phrase + '%'})
    answer_data = cursor.fetchall()
    return answer_data


@connection.connection_handler
def get_latest_questions(cursor, count):
    cursor.execute("""SELECT * FROM question
                      ORDER BY submission_time DESC
                      LIMIT %(count)s;""",
                   {'count': count})
    latest_questions = cursor.fetchall()
    return latest_questions


@connection.connection_handler
def get_user_id_by_user_name(cursor, user_name):
    cursor.execute("""SELECT id FROM users WHERE user_name=%(user_name_value)s;""",
                   {'user_name_value': user_name})
    user_id = cursor.fetchall()[0]['id']
    return user_id


@connection.connection_handler
def add_new_user(cursor, new_user):
    salt = util.generate_salt()
    cursor.execute("""
                    INSERT INTO users (user_name, salt, hashed_password, reg_date)
                    VALUES (%(user_name)s, %(salt)s, %(hashed_password)s, %(reg_date)s) ;
                    """,
                   {
                       'user_name': new_user['user_name'],
                       'salt': salt,
                       'hashed_password': util.hash_password(new_user['password'], salt),
                       'reg_date': datetime.now().replace(microsecond=0)
                   })


@connection.connection_handler
def mark_question_as_accepted(cursor, question_id):
    cursor.execute("""UPDATE question
                        SET accepted = TRUE
                            WHERE id=%(id)s;""",
                   {'id': question_id})


@connection.connection_handler
def is_question_accepted(cursor, question_id):
    cursor.execute("""SELECT accepted FROM question
                      WHERE id=%(id);""",
                   {'id': question_id})
    accepted = cursor.fetchall()[0]['accepted']
    return accepted
