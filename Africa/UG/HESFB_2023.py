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

URL = 'https://www.dropbox.com/scl/fi/kinfy6u2madguifbm24h0/Student-Loan-Beneficiaries-AY-2023-24-OFFICIAL.pdf?rlkey=sjpofh6snxrhuvicigaw15x43&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2023_recommended_applicants.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@timer
def extract_data():
    with pdfplumber.open(PDF_PATH) as pdf:
        pdf_length = len(pdf.pages)

        for j in range(pdf_length):
            page_text = pdf.pages[j].extract_text().split('\n')

            if j == 0 or j == 13:
                for i, text in enumerate(page_text):
                    if i <= 1:
                        continue
                    row = []
                    if i == 2:
                        row = ['Application No.', 'Name of Applicant', 'Gender', 'District of Origin', 'Admitted University', 'Admitted Course']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_recommended_applicants')
                    else:
                        if text == '' or text[:4] == 'Page':
                            continue
                        row = transform_string(text)

                        if row is None:
                            continue

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_recommended_applicants')
                continue

            for i, text in enumerate(page_text):
                    if i <= 2:
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

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_recommended_applicants')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(HESFB/2023/\d+)\s+(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(.*?)((?:BSc|Bsc|BSC|B\.|Diploma|Dip|B |Bachelor|BACHELOR|Bachelof|BA |NATIONAL HIGHER|Foundation Programme)(?:.+))'

    # These are messed up strings
    input_string = input_string.replace('TechnoBloSgcy', 'Technology BSc')
    input_string = input_string.replace('TechnoBloSgcy.', 'Technology BSc.')
    input_string = input_string.replace('TechnoBlo.Sgcy.', 'Technology B.Sc.')
    input_string = input_string.replace('TechnoBloagcyhelor', 'Technology Bachelor')
    input_string = input_string.replace('TechnoBlo. gMyedical', 'Technology B. Medical')
    input_string = input_string.replace('TechnoBlo. gNyursing', 'Technology B. Nursing')
    input_string = input_string.replace('TechnoBlo. gPyharmacy', 'Technology B. Pharmacy')
    input_string = input_string.replace('TechnoBlo. gPyetroleum', 'Technology B. Petroleum')
    input_string = input_string.replace('TechnoBlo. gInyformation', 'Technology B. Information')
    input_string = input_string.replace('TechnoBlo. gEyngineering', 'Technology B. Engineering')
    input_string = input_string.replace('TechnoBlo. gPyhysiotherapy', 'Technology B. Physiotherapy')
    input_string = input_string.replace('TechnoBlo. gPyharmaceutical', 'Technology B. Pharmaceutical')
    input_string = input_string.replace('CommDuipnliocamtiao inns CToemchpnuotleorg Sycience', 'Communications Technology Diploma in Computer Science')
    input_string = input_string.replace('CommDuipnliocamtiao inns TTeelcehcnomolomguynications', 'Communications Technology Diploma in Telecommunications')
    input_string = input_string.replace('ManaDgiepm ine nMt eSdeircvailc Rese,c Morudlas gaond', 'Management Services, Mulago Dip in Medical Records and')
    input_string = input_string.replace('ManaDgiepm ine nMt eSdeircvailc Leas,b Morualtaogroy', 'Management Services, Mulago Diploma in Medical Laboratory')
    input_string = input_string.replace('ManaDgiepmloemnat Sine rPvhicaersm, Macuylago', 'Management Services, Mulago Diploma in Pharmacy')
    input_string = input_string.replace('ManaDgiepmloemnat Sine rOvcicceusp, aMtiuolnaaglo', 'Management Services, Mulago Diploma in Occupational')
    input_string = input_string.replace('ManaDgiepmloemnat Sine rPvuicbelisc, MHeualaltgho', 'Management Services, Mulago Diploma in Public Health')
    input_string = input_string.replace('ManaDgiepmloemnat Sine rEvaicre Nso, Mrsuel aagnod', 'Management Services, Mulago Diploma in Ear Norse and')
    input_string = input_string.replace('ManaDgiepmloemnat Sine rMviecdeisc,a Ml Lualabgooratory', 'Management Services, Mulago Diploma in Medical Laboratory')
    input_string = input_string.replace('ManaDgiepmloemnat Sine rMviecdeisc,a Ml Rualadgioography', 'Management Services, Mulago Diploma in Medical Radiography')
    input_string = input_string.replace('ManaDgiepmloemnat Sine rOvrictheos,p Meduilca gMoedicine', 'Management Services, Mulago Diploma in Orthopedic Medicine')
    input_string = input_string.replace('CommDuipn iicna tEiolencst rTiceaclh annodlo Eglyectronics', 'Communications Technology Dip in Electrical and Electronics')

    match = re.match(pattern, input_string)
    
    if match:
        return list(match.groups())
    else:
        print(input_string)
        return None

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
