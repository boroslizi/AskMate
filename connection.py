import csv


def get_all_data(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        all_data = []
        for line in reader:
            all_data.append(line)
        return all_data


# def get_all_headers(file):
#     with open(file, 'r') as f:
#         reader = csv.DictReader(f)
#         headers = reader.fieldnames
#         return headers
