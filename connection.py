import csv


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


def get_next_id(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for data_block in reader:
            data_id = int(data_block['id'])
        data_id += 1
        print("New id is: {}".format(data_id))
        return data_id


def write_to_file(file, data):
    headers = get_all_headers(file)
    with open(file, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(data)

#
# def get_new_question_details(file):
#     with open(file, 'a') as f:
#         csv_writer = csv.writer(f)
#         question_details = []  # id, submission_time, view_number, vote_number
#         question_details.append()


def get_all_headers(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        return headers


def get_id(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for data_block in reader:
            data_id = int(data_block['id'])
        data_id += 1
        print("New id is: {}".format(data_id))
        return data_id

