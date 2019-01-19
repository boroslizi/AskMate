from tempfile import NamedTemporaryFile
import shutil
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


def edit_file(file, edited_data, data_id):
    headers = get_all_headers(file)
    temp_file = NamedTemporaryFile(mode="wt", delete=False)
    with open(file, 'r+') as csvFile, temp_file:
        reader = csv.DictReader(csvFile)
        writer = csv.DictWriter(temp_file, fieldnames=headers)
        writer.writeheader()
        for data_block in reader:
            if data_block['id'] == data_id:
                data_block = edited_data
            writer.writerow(data_block)
    shutil.move(temp_file.name, file)


def delete_from_file(file, data_id):
    headers = get_all_headers(file)
    temp_file = NamedTemporaryFile(mode="wt", delete=False)
    with open(file, 'r+') as stories, temp_file:
        reader = csv.DictReader(stories)
        writer = csv.DictWriter(temp_file, fieldnames=headers)
        writer.writeheader()
        for data_block in reader:
            if data_block['id'] != data_id:
                writer.writerow(data_block)
    shutil.move(temp_file.name, file)
