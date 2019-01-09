import os
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
    submission_times.sort()
    sorted_questions = []
    for time in submission_times:
        for question in questions:
            if time in question.values():
                sorted_questions.append(question)
    connection.get_next_id(QUESTIONS)
    return sorted_questions


def write_new_question(data):
    connection.write_to_file(QUESTIONS, data)


def add_new_answer(new_answer, question_id):
    print(question_id, new_answer)
    pass


def get_next_question_id():
    return connection.get_next_id(QUESTIONS)
