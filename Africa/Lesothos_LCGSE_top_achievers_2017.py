import os
import re
import pdfplumber

URL = 'https://www.dropbox.com/scl/fi/jvqffoycnudnm9jzuz5m8/2017_Top_Archievers.pdf?rlkey=7ux1bnk2qu8qetvfq54iwiing&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = '' # FIXME: Change to the perminant file path the .csvs will be stored in
PDF_LENGTH = 10

def extract_data():
    
    with pdfplumber.open(PDF_PATH) as pdf:
        for j in range(PDF_LENGTH):
            page_text = pdf.pages[j].extract_text().split('\n')

            if j == 0:
                # Keep track of the lines
                i = 0

                for text in page_text:
                    row = []
                    if i == 0:
                        row.append(text)
                        print(row)
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data')
                        i += 1
                    elif i == 1:
                        row = text.split(" ")
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data')
                        i += 1
                    else:
                        if text == '':
                            continue
                        row = transform_string(text)
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data')
                        i += 1
                continue
            for text in page_text:
                row = []
                
                if text == '':
                    continue
                row = transform_string(text)
                write_row_to_csv(row, SAVE_FILE_PATH, 'data')
                


# Append a single row to .csv
def write_row_to_csv(row, file_path, file_name):
    # Create the directories for the file path
    # exist_ok=True means that no errors are raised if the file path is already there
    os.makedirs(file_path, exist_ok=True)

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
    pattern = r'(\d+)\s+(\d+)\s+(LS\d+)\s+(.*?)\s+([FM])\s+(.+)'
    match = re.match(pattern, input_string)
    
    if match:
        return list(match.groups())
    else:
        return None

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
