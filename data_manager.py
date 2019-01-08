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
    return sorted_questions
