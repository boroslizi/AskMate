import csv


QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_data(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        all_data = []
        for line in reader:
            all_data.append(line)
        return all_data


def get_all_headers(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        return headers


def write_to_file(file, data):
    headers = get_all_headers(file)
    with open(file, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(data)

