import logging
import os
import re
import sys
import pdfplumber

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_modules.scraping import timer, write_row_to_csv

'''
pip install pdfplumber
'''

URL = 'https://www.dropbox.com/scl/fi/s42zcnc63atxulg99tec2/List-of-LOT-2-Students-Loan-Scheme-Beneficiaries-for-the-AY2021-22.pdf?rlkey=be4nmislms6in0wene40po8ix&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2021_undergraduate_beneficiaries_2.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@timer
def extract_data():
    with pdfplumber.open(PDF_PATH) as pdf:
        pdf_length = len(pdf.pages)

        for j in range(pdf_length):
            page_text = pdf.pages[j].extract_text().split('\n')

            if j == 0:
                for i, text in enumerate(page_text):
                    if i <= 1:
                        continue
                    row = []
                    if i == 2:
                        row = ['Name of Applicant', 'Gender', 'District of Origin', 'Admitted University', 'Admitted Course', 'Course Type', 'Region Origin']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_undergraduate_beneficiaries_2')
                    else:
                        if text == '' or text[:4] == 'Page':
                            continue
                        row = transform_string(text)

                        if row is None:
                            continue

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_undergraduate_beneficiaries_2')
                continue

            for i, text in enumerate(page_text):
                    if i <= 1:
                        continue
                    row = []
                    if text == '' or text[:4] == 'Page':
                        continue
                    row = transform_string(text)

                    if row is None:
                        continue

                    # Replace the commas to not mess up the .csv file
                    for k, column in enumerate(row):
                        row[k] = column.replace(',', '-')

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_undergraduate_beneficiaries_2')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(.*?)([FM])\s+([-A-Za-z]+)\s+(.*?)((?:BSc|Bsc|BSC|B\.|Diploma|Dip|B |Bachelor|BACHELOR|BA |NATIONAL HIGHER)(?:.*?))\s*([A-Za-z]+)\s+([A-Za-z]+)'
    match = re.match(pattern, input_string)
    
    # These lines are messed up
    if input_string == 'COSMAS OJWANG M Soroti Gulu University Bachelof of Science Education (Physical, Biological, Economics, SportsD Secgierneece, TechnologiEcaals tEedruncation)':
        return ['COSMAS OJWANG', 'M', 'Soroti', 'Gulu University', 'Bachelof of Science Education (Physical, Biological, Economics, Sports Science, Technological Education)', 'Degree', 'Eastern']
    elif input_string == 'OSCAR OWANI M Oyam Gulu University Bachelof of Science Education (Physical, Biological, Economics, SportsD Secgierneece, TechnologiNcaol rEthdeurcnation)':
        return ['OSCAR OWANI', 'M', 'Oyam', 'Gulu University', 'Bachelof of Science Education (Physical, Biological, Economics, Sports Science, Technological Education)', 'Degree', 'Northern']
    elif input_string == 'JONATHANGEORGE MUSENEWABENDMO Bududa Makerere University B.Sc. Quantity surveying Degree Eastern':
        return ['JONATHANGEORGE MUSENEWABENDO', 'M', 'Bududa', 'Makerere University', 'B.Sc. Quantity surveying', 'Degree', 'Eastern']
    elif input_string == 'Nakuwanda Bridget Hellen NakuwandFa Mityana Makerere University BSc. Computer Science Degree Central':
        return ['Nakuwanda Bridget Hellen Nakuwanda', 'F', 'Mityana', 'Makerere University', 'BSc. Computer Science', 'Degree', 'Central']
    elif input_string == 'ODONGO Samuel kasiri M Kotido Mbarara University of Science and TechnoBloSgc.y Software Engineering Degree Northern':
        return ['ODONGO Samuel kasiri', 'M', 'Kotido', 'Mbarara University of Science and Technology', 'BSc. Software Engineering', 'Degree', 'Northern']
    elif match:
        return list(match.groups())
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
