import os
import re
import pdfplumber

URL = 'https://www.dropbox.com/scl/fi/j7kwllamjhm446ao3mhvw/2022_Top_Archievers_8bf75feb7e.pdf?rlkey=lhiajue98l4ri013xpuyqebgd&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = '' # FIXME: Change to the perminant file path the .csvs will be stored in
PDF_LENGTH = 7 # Probably this works enumerate(pdf.pages)

def extract_data():
    
    with pdfplumber.open(PDF_PATH) as pdf:
        for j in range(PDF_LENGTH):
            page_text = pdf.pages[j].extract_text().split('\n')

            if j == 0:
                # Keep track of the lines
                i = 0

                for text in page_text:
                    row = []
                    # print(text)
                    if i == 0:
                        row = ['Rank', '# A\'s', 'Candidate Names', 'Gender', 'Centre No.', 'School Name']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data')
                        i += 1
                    else:
                        if text == '' or text == str(j + 1):
                            continue
                        row = transform_string(text)
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data')
                        i += 1
                continue

            # Keep track of the lines
            i = 0

            for text in page_text:
                    row = []
                    if i == 0:
                        i += 1
                        continue
                    else:
                        if text == '' or text == str(j + 1):
                            continue
                        row = transform_string(text)
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data')
                        i += 1
                


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
    pattern = r'(\d+)\s+(\d+)\s+(.*?)\s+([FM])\s+(LS\d+)\s+(.+)'
    match = re.match(pattern, input_string)
    
    pattern_school = r'(.+?)(SCHOOL|HIGH)'
    match_school = re.match(pattern_school, input_string)
    
    pattern_name = r'(.+)'
    match_name = re.match(pattern_name, input_string)
    
    if match:
        return list(match.groups())
    elif match_school:
        return [' ', ' ', ' ', ' ', ' ', input_string]
    elif match_name:
        return [' ', ' ', input_string, ' ', ' ', ' ']
    else:
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
