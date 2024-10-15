import os
import re
import pdfplumber

URL = 'https://www.dropbox.com/scl/fi/e8b880li4gcl6qwitnuwp/2016-LGCSE-Results.pdf?rlkey=kbdjanpun98mtz391j53ei1db&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = '' # FIXME: Change to the perminant file path the .csvs will be stored in

def extract_data():
    
    with pdfplumber.open(PDF_PATH) as pdf:

        PDF_LENGTH = len(pdf.pages)

        header = ['Rank','Average Score','Names','Gender','Centre No.','School Name','No. A*']
        write_row_to_csv(header, SAVE_FILE_PATH, 'data')

        for j in range(PDF_LENGTH):
            page_text = pdf.pages[j].extract_text().split('\n')

            if j > 4:
                continue
            elif j == 0:
                # Keep track of the lines
                i = 0

                for text in page_text:
                    row = []

                    if i < 4:
                        i += 1
                        continue
                    else:
                        if text == '' or text == str(j + 1):
                            continue
                        row = transform_string(text)
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data')
                        i += 1
                continue
            for text in page_text:
                row = []
                
                if text == '' or text == str(j + 1):
                    continue
                row = transform_string(text)
                write_row_to_csv(row, SAVE_FILE_PATH, 'data')
                


# Append a single row to .csv
def write_row_to_csv(row, file_path, file_name):
    # Create the directories for the file path
    # exist_ok=True means that no errors are raised if the file path is already there
    os.makedirs(file_path, exist_ok=True)

    # print(f"Path '{file_path}' created successfully!")

    csv_file_path = f'{file_path}{file_name}.csv'
    with open(csv_file_path, 'a', encoding='utf-8') as work_file:
        row_text = ''
        # Each pipeline indicates the start of a new column in the .csv file
        for item in row:
            row_text += item + ','
        row_text = row_text[:-1]
        row_text = row_text + '\n'
        work_file.write(row_text)

# Transforms the string into desired format for csv table
def transform_string(input_string):

    # Remove strange bug from MASILO KOPANANG OFNIAL
    if input_string == '5 16 MASILO KOPANANG OFNIAL M(cid:12) LS878 NTAOTE HIGH SCHOOL 1':
        input_string = '5 16 MASILO KOPANANG OFNIAL M LS878 NTAOTE HIGH SCHOOL 1'

    pattern = r'(\d+)\s+(\d+)\s+(.*?)\s+([FM])\s+(LS\d+)\s+(.*?)\s+(\d+)'
    match = re.match(pattern, input_string)

    pattern_missing_score = r'(\d+)\s+(.*?)\s+([FM])\s+(LS\d+)\s+(.*?)\s+(\d+)'
    match_missing_score = re.match(pattern_missing_score, input_string)
    
    if match:
        return list(match.groups())
    elif match_missing_score:
        student = list(match_missing_score.groups())
        student.insert(1, '')
        return student
    else:
        print(input_string) # This is for debugging
        return None

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
