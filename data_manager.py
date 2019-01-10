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


def write_new_question(data):
    connection.write_to_file(QUESTIONS, data)


def get_new_answer_id():
    latest_answer_id = get_all_data("answers")[-1]["id"]
    new_id = str(int(latest_answer_id) + 1)
    return new_id


def add_new_answer(new_answer, question_id):
    print(question_id, new_answer)
    new_data = {
        "id": get_new_answer_id(),
        "submission_time": random.randint(1, 10000000),
        "vote_number": "0",
        "question_id": question_id,
        "message": new_answer,
        "image": ""
    }
    connection.write_to_file(ANSWERS, new_data)

    pass


def get_next_question_id():
    return connection.get_next_id(QUESTIONS)

def get_all_data_by_question_id(question_id):
    questions_list = connection.get_all_data(QUESTIONS)
    question_by_id = []
    for question in questions_list:
        if (question_id == question['id']):
            question_by_id = question
    return question_by_id

def get_answers_by_question_id(question_id):
    answers_list = connection.get_all_data(ANSWERS)
    answers_list_by_id = []
    for answers in answers_list:
        if (answers['question_id'] == question_id):
            answers_list_by_id.append(answers['message'])
    return answers_list_by_id

