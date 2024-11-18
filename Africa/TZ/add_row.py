import os
import csv

# Define the row you want to insert
# new_row = ["CODE", "SUBJECT NAME", "REG", "SAT", "NO-CA", "W/HD", "CLEAN", "PASS", "GPA", "COMPENTENCY LEVEL"]
new_row = ["REGIST", "ABSENT", "SAT", "WITHHELD", "NO-CA", "CLEAN", "DIV I", "DIV II", "DIV III", "DIV IV", "DIV 0"]

def edit_csv_file(file_path):
    '''
    If a row exists in the csv this will add a row after it
    '''
    rows = []
    found_target = False

    # Read the file
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
            if "EXAMINATION CENTRE DIVISION PERFORMANCE" in row:
                found_target = True
                rows.append(new_row)

    # Write the file back only if target row was found
    if found_target:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

def crawl_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                edit_csv_file(file_path)
                print(f'Fixed: {file_path}')

# Replace 'your_folder_path' with the path to your folder
crawl_folder('w:/papers/current/african_records/TZ_ACSEE/')
