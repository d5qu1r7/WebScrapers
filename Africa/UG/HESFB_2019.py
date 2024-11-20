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

URL = 'https://www.dropbox.com/scl/fi/eeyc6kzt06paesqur9z7x/Final-List-of-Successful-Applicants-2018.pdf?rlkey=y8ps5nt66pgkrkj95u98ngdc5&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2019_successful_applicants.log')
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
                    if i <= 2:
                        continue
                    row = []
                    if i == 3:
                        row = ['S/No', 'Application No.', 'Name of Applicant', 'Gender', 'District of Origin', 'Admitted University', 'Admitted Course', 'Course Duration', 'Course Type', 'Region']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_applicants')
                    else:
                        if text == '':
                            continue
                        row = transform_string(text)

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_applicants')
                continue

            for i, text in enumerate(page_text):
                    row = []
                    if text == '':
                        continue
                    row = transform_string(text)

                    # Replace the commas to not mess up the .csv file
                    for k, column in enumerate(row):
                        row[k] = column.replace(',', '-')

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_applicants')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(\d+)\s+(HESFB/2018/\d+)\s+(.*?)([FM])\s+([A-Za-z]+)\s+((?:.*?)(?:Institute Kigumba|Training Insti|School|Clinical Officers|Fortportal|INSTITUTE|Midwifery|Officers,Gulu|Comprehensive Nursing|BusinessSch|University|Technology|College|College Mulago|College,Lira|College, Bushenyi|College,Elgon|Mbale|Management))(.*?)\s*(\d+.+years)\s+([A-Za-z]+)\s+([A-Za-z]+)'
    match = re.match(pattern, input_string)
    
    # This line is messed up
    if input_string == '554 HESFB/2018/04803 COLLIN MAGULU M Kamuli Kyambogo University Ordinary Diploma in Science Technology (Biology, Physics, Ch3e myeiastrrsy) Diploma Eastern':
        return ['554', 'HESFB/2018/04803', 'COLLIN MAGULU', 'M', 'Kamuli', 'Kyambogo University', 'Ordinary Diploma in Science Technology (Biology, Physics, Chemistry)', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '319 HESFB/2018/01068 GEORGE EMESU M Soroti Uganda Institute of Information and CommunicationDsi pTleocmhan oinlo Tgeylecommunications Engineering 2 years Diploma Eastern':
        return ['319', 'HESFB/2018/01068', 'GEORGE EMESU', 'M', 'Soroti', 'Uganda Institute of Information and Communicatios Technology', ' Diploma in Telecommunications Engineering', '2 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '489 HESFB/2018/01574 HENRY SSEMPIJJA M Wakiso Ndejje University BSc. Information Technology (Student passed Mathematics/P3h yyesaicrss at A ‘LeDveeglr)ee Central':
        return ['489', 'HESFB/2018/01574', 'HENRY SSEMPIJJA', 'M', 'Wakiso', 'Ndejje University', ' BSc. Information Technology (Student passed Mathematics/Physics at A Level)', '3 years', 'Degree', 'Central']
    # This line is also messed up
    elif input_string == '1125 HESFB/2018/02692 MARTIN ODYEK M Lira Uganda Institute of Information and CommunicationDsi pTleocmhan oinlo Eglyectrical Engineering 2 years Diploma Northern':
        return ['1125', 'HESFB/2018/02692', 'MARTIN ODYEK', 'M', 'Lira', 'Uganda Institute of Information and Communications Technology', ' Diploma in Electrical Engineering', '2 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '1319 HESFB/2018/02777 NICHOLAS SSEMWOGERERE M Luwero Uganda Institute of Information and CommunicationDsi pTleocmhan oinlo Eglyectrical Engineering 2 years Diploma Central':
        return ['1319', 'HESFB/2018/02777', 'NICHOLAS SSEMWOGERERE', 'M', 'Luwero', 'Uganda Institute of Information and Communications Technology', ' Diploma in Electrical Engineering', '2 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '1609 HESFB/2018/01663 RITAH MUGISHA F Kisoro Uganda Institute of Information and CommunicationDsi pTleocmhan oinlo Tgeylecommunications Engineering 2 years Diploma Western':
        return ['1609', 'HESFB/2018/01663', 'RITAH MUGISHA', 'F', 'Kisoro', 'Uganda Institute of Information and Communications Technology', ' Diploma in Electrical Engineering', '2 years', 'Diploma', 'Western']
    elif match:
        return list(match.groups())
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
