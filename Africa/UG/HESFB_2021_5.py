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

URL = 'https://www.dropbox.com/scl/fi/suxo6zvqoirwvy4f473qw/Succesful-Loan-Scheme-Beneficiaries-Undergraduate-DEGREE-Lot-1_2021_22.pdf?rlkey=okc01tivuswoi95xwwv7nufvs&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2021_undergraduate_beneficiaries.log')
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
                        row = ['Application No.', 'Name of Applicant', 'Gender', 'District of Origin', 'Admitted University', 'Admitted Course', 'Course Duration', 'Course Type']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_undergraduate_beneficiaries')
                    else:
                        if text == '' or text[:4] == 'Page':
                            continue
                        row = transform_string(text)

                        if row is None:
                            continue

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_undergraduate_beneficiaries')
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

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_undergraduate_beneficiaries')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(HESFB/2021/\d+)\s+(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(.*?)((?:BSc|Bsc|BSC|B\.|Diploma|Dip|B |Bachelor|BACHELOR|BA |NATIONAL HIGHER)(?:.*?))\s*(\d+.+years)\s+([A-Za-z]+)'
    match = re.match(pattern, input_string)
    
    # These lines are messed up
    if input_string == 'HESFB/2021/06135 Addah Nahwera F Kiruhura Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/06135', 'Addah Nahwera', 'F', 'Kiruhura', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/11770 ANGEL NATUMANYA F Kamwenge Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/11770', 'ANGEL NATUMANYA', 'F', 'Kamwenge', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/09027 Annah Kyarikunda F Ntungamo Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/09027', 'Annah Kyarikunda', 'F', 'Ntungamo', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/11553 Zerinda Turyaguma F Ntungamo Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/11553', 'Zerinda Turyaguma', 'F', 'Ntungamo', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/06827 SHIVAN NUWASIIMA F MBARARA CITY Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/06827', 'SHIVAN NUWASIIMA', 'F', 'MBARARA CITY', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/11767 RABON ANDIHIHI M Ibanda Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/11767', 'RABON ANDIHIHI', 'M', 'Ibanda', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/04061 Rabecca Nakahima F Isingiro Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/04061', 'Rabecca Nakahima', 'F', 'Isingiro', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/10550 pellan kansiime F Ntungamo Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/10550', 'pellan kansiime', 'F', 'Ntungamo', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/03876 PATIENCE NAKAWUKYI F Isingiro Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/03876', 'PATIENCE NAKAWUKYI', 'F', 'Isingiro', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/04119 Mercy Britah Kemigisha F Mitooma Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/04119', 'Mercy Britah Kemigisha', 'F', 'Mitooma', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/09017 Evelyine Kediinie F Ntungamo Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/09017', 'Evelyine Kediinie', 'F', 'Ntungamo', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/09074 Daphine Kemigisha F Bushenyi Bishop Stuart University B. Agribusiness Management & Community Deve3l oypeamresnt Degree':
        return ['HESFB/2021/09074', 'Daphine Kemigisha', 'F', 'Bushenyi', 'Bishop Stuart University', 'B. Agribusiness Management & Community Development', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/08308 ANTHONY LULE SSENYONYI M MASAKA CITY Uganda Martyrs University BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/08308', 'ANTHONY LULE SSENYONYI', 'M', 'MASAKA CITY', 'Uganda Martyrs University', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/05627 ESTHER NAKATO F Hoima Uganda Martyrs University BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/05627', 'ESTHER NAKATO', 'F', 'Hoima', 'Uganda Martyrs University', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/12123 Judith Nambuusi F Kalungu Uganda Martyrs University BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/12123', 'Judith Nambuusi', 'F', 'Kalungu', 'Uganda Martyrs University', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/06976 ZUBEDA NAMBOZO F Mbale Islamic University in Uganda BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/06976', 'ZUBEDA NAMBOZO', 'F', 'Mbale', 'Islamic University in Uganda', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/11252 RONAH ASHABA F Bushenyi Mbarara University of Science and Technology BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/11252', 'RONAH ASHABA', 'F', 'Bushenyi', 'Mbarara University of Science and Technology', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/09850 EVALYINE NAHWERA F Isingiro Mbarara University of Science and Technology BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/09850', 'EVALYINE NAHWERA', 'F', 'Isingiro', 'Mbarara University of Science and Technology', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/08525 Hillary Tumwine M Rukungiri Mbarara University of Science and Technology BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/08525', 'Hillary Tumwine', 'M', 'Rukungiri', 'Mbarara University of Science and Technology', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/07646 MICHEAL KATENDE M Buikwe Mbarara University of Science and Technology BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/07646', 'MICHEAL KATENDE', 'M', 'Buikwe', 'Mbarara University of Science and Technology', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/07849 Murashani Fredrick M Sheema Mbarara University of Science and Technology BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/07849', 'Murashani Fredrick', 'M', 'Sheema', 'Mbarara University of Science and Technology', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/09321 William Omara M Abim Kampala International University BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/09321', 'William Omara', 'M', 'Abim', 'Kampala International University', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/00346 HAPPY NUWASIIMA F Sheema Kabale University BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/00346', 'HAPPY NUWASIIMA', 'F', 'Sheema', 'Kabale University', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/07039 MUKWAYA Kevin KEVIN BRYANNAH F Wakiso Kampala University BSc. Computer Science (Student passes Mathema3t yicesa/rPshysics at A’ LevDele)gree':
        return ['HESFB/2021/07039', 'MUKWAYA Kevin KEVIN BRYANNAH', 'F', 'Wakiso', 'Kampala University', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/04297 Betty Arieba F Pallisa Kampala International University B. Special needs with Education, Speech & Langu3a gyee atrhserapy Degree':
        return ['HESFB/2021/04297', 'Betty Arieba', 'F', 'Pallisa', 'Kampala International University', 'B. Special needs with Education, Speech & Language therapy', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/11105 SALIMA NAKATO F Bugiri Kampala International University B. Special needs with Education, Speech & Langu3a gyee atrhserapy Degree':
        return ['HESFB/2021/11105', 'SALIMA NAKATO', 'F', 'Bugiri', 'Kampala International University', 'B. Special needs with Education, Speech & Language therapy', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/11139 SILINA BABIRYE F Bugiri Kampala International University B. Special needs with Education, Speech & Langu3a gyee atrhserapy Degree':
        return ['HESFB/2021/11139', 'SILINA BABIRYE', 'F', 'Bugiri', 'Kampala International University', 'B. Special needs with Education, Speech & Language therapy', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/11574 BRENDA NAMUGENYI F Kampala Bugema University BSc in Computer Networks and SystemsAdminis3t ryaetaiorns Degree':
        return ['HESFB/2021/11574', 'BRENDA NAMUGENYI', 'F', 'Kampala', 'Bugema University', 'BSc in Computer Networks and SystemsAdministration', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/04031 CHRISTINE KOBUSINGE F HOIMA CITY Ndejje University BSc. Surveying, Quantity Surveying & Land Form4a ytieoanrs Degree':
        return ['HESFB/2021/04031', 'CHRISTINE KOBUSINGE', 'F', 'HOIMA CITY', 'Ndejje University', 'BSc. Surveying, Quantity Surveying & Land Formation', '4 years', 'Degree']
    elif input_string == 'HESFB/2021/00867 SHARON NABUKALU F Luweero Ndejje University Bsc.Surveying,Quantity Surveying & Land Use/ F4o yrmeaartsion Degree':
        return ['HESFB/2021/00867', 'SHARON NABUKALU', 'F', 'Luweero', 'Ndejje University', 'BSc. Surveying, Quantity Surveying & Land Formation', '4 years', 'Degree']
    elif input_string == 'HESFB/2021/10402 INNOCENT OKWIR M LIRA CITY Ndejje University BSc. Surveying, Quantity Surveying & Land Form4a ytieoanrs Degree':
        return ['HESFB/2021/10402', 'INNOCENT OKWIR', 'M', 'LIRA CITY', 'Ndejje University', 'BSc. Surveying, Quantity Surveying & Land Formation', '4 years', 'Degree']
    elif input_string == 'HESFB/2021/11955 JOSELINE KISEMBO KABANTU F Bundibugyo Ndejje University BSc. Information Technology (Student passed M3at yheeamrsatics/Physics atD Ae g‘Lreeveel)':
        return ['HESFB/2021/11955', 'JOSELINE KISEMBO KABANTU', 'F', 'Bundibugyo', 'Ndejje University', 'BSc. Information Technology (Student passed Mathematics/Physics at A ‘Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/08155 MURUNGI DAVIES M Ntoroko Mountains of the Moon University BSc. Information Technology (Student passed M3at yheeamrsatics/Physics atD Ae g‘Lreeveel)':
        return ['HESFB/2021/08155', 'MURUNGI DAVIES', 'M', 'Ntoroko', 'Mountains of the Moon University', 'BSc. Information Technology (Student passed Mathematics/Physics at A ‘Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/08245 RINET TUKAHIRWA F Kibaale Mountains of the Moon University BSc. Information Technology (Student passed M3at yheeamrsatics/Physics atD Ae g‘Lreeveel)':
        return ['HESFB/2021/08245', 'RINET TUKAHIRWA', 'F', 'Kibaale', 'Mountains of the Moon University', 'BSc. Information Technology (Student passed Mathematics/Physics at A ‘Level)', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/08662 GIFT KIHEMBO F Kabale Ndejje University Bachelor of Cooperative Agribusiness Managem3e nytears Degree':
        return ['HESFB/2021/08662', 'GIFT KIHEMBO', 'F', 'Kabale', 'Ndejje University', 'Bachelor of Cooperative Agribusiness Management', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/10903 HAWA BARUNGI F Kanungu Ndejje University Bachelor of Cooperative Agribusiness Managem3e nytears Degree':
        return ['HESFB/2021/10903', 'HAWA BARUNGI', 'F', 'Kanungu', 'Ndejje University', 'Bachelor of Cooperative Agribusiness Management', '3 years', 'Degree']
    elif input_string == 'HESFB/2021/03931 Francis Okwairwoth M Pakwach Mbarara University of Science and Technology BSc in Petroleum Engineering and Environment 4M ygetars Degree':
        return ['HESFB/2021/03931', 'Francis Okwairwoth', 'M', 'Pakwach', 'Mbarara University of Science and Technology', 'BSc in Petroleum Engineering and Environment Mgt', '4 years', 'Degree']
    elif input_string == 'HESFB/2021/00152 SHEILLAH AHEEBWE F Bushenyi Ndejje University Bsc. Engineering in Civil and Building Engineerin4g y ears Degree':
        return ['HESFB/2021/00152', 'SHEILLAH AHEEBWE', 'F', 'Bushenyi', 'Ndejje University', 'Bsc. Engineering in Civil and Building Engineering', '4 years', 'Degree']
    elif match:
        return list(match.groups())
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
