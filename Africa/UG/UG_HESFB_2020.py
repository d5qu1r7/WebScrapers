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

URL = 'https://www.dropbox.com/scl/fi/wbfua2aa87lvhsnlfw5dt/2019-20-HESFB-Final-List-of-Successful-Loan-Beneficiaries.-The-Tower-Post.pdf?rlkey=w85aamwdarwqbywm4y3rmca63&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2020_loan_awards_2.log')
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
                        row = ['S/No', 'Application No.', 'Name of Applicant', 'Gender', 'District of Origin', 'Admitted University', 'Admitted Course', 'Course Duration', 'Course Type', 'Region of Origin']
                        # write_row_to_csv(row, SAVE_FILE_PATH, 'data_loan_awards_2')
                    else:
                        if text == '' or text[:4] == 'Page':
                            continue
                        row = transform_string(text)

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        # write_row_to_csv(row, SAVE_FILE_PATH, 'data_loan_awards_2')
                continue

            for i, text in enumerate(page_text):
                    if i <= 2:
                        continue
                    row = []
                    if text == '' or text[:4] == 'Page':
                        continue
                    row = transform_string(text)

                    # Replace the commas to not mess up the .csv file
                    for k, column in enumerate(row):
                        row[k] = column.replace(',', '-')

                    # write_row_to_csv(row, SAVE_FILE_PATH, 'data_loan_awards_2')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(\d+)\s+(HESFB/2019/\d+)\s+(.*?)([FM])\s+([A-Za-z]+)\s+(.*?)((?:BSc|Bsc|BSC|B\.|diploma|Diploma|Dip|B |Bachelor|BA )(?:.*?))\s*(\d+.+years)\s+([A-Za-z]+)\s+([A-Za-z]+)'
    match = re.match(pattern, input_string)
    
    # This line is messed up
    if input_string == '51 HESFB/2019/07015 ALEX LUBEGA M Lwengo Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheasr, mMauclyago 3 years Diploma Central':
        return ['51', 'HESFB/2019/07015', 'ALEX LUBEGA', 'M', 'Lwengo', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '75 HESFB/2019/05899 AMBROSE BYAMUKAMA M Rubirizi Uganda Institute of Information and CommuDniipclaotmioan sin T Eelcehcntroilcoagl yEngineering 2 years Diploma Western':
        return ['75', 'HESFB/2019/05899', 'AMBROSE BYAMUKAMA', 'M', 'Soroti', 'Uganda Institute of Information and Communicatios Technology', ' Diploma in Telecommunications Engineering', '2 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '133 HESFB/2019/06582 ARTHUR MASIKA M Namisindwa Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Aicneess, tMheuslaiago 2 years Diploma Eastern':
        return ['133', 'HESFB/2019/06582', 'ARTHUR MASIKA', 'M', 'Namisindwa', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Anesthesia', '2 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '226 HESFB/2019/04112 BRIAN PULE M Amolatar Gulu University BSc. Computer Science (Student passes Mathematics/Physic3s y aeta Ar’s Level) Degree Northern':
        return ['226', 'HESFB/2019/04112', 'BRIAN PULE', 'M', 'Amolatar', 'Gulu University', 'BSc. Computer Science (Student passes Mathematics/Physics at A’s Level)', '3 years', 'Degree', 'Northern']
    # This line is also messed up
    elif input_string == '227 HESFB/2019/04216 BRIAN SENONO M Wakiso Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheasr, mMauclyago 3 years Diploma Central':
        return ['227', 'HESFB/2019/04216', 'BRIAN SENONO', 'M', 'Wakiso', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '299 HESFB/2019/05032 CLINTON ASHABA M Isingiro Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheasr, mMauclyago 3 years Diploma Western':
        return ['299', 'HESFB/2019/05032', 'CLINTON ASHABA', 'M', 'Isingiro', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '365 HESFB/2019/07902 DEBORAH NAKANYIKE REBECCA F Wakiso Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Oicretsh,o Mpuedlaigc oMedicine 3 years Diploma Central':
        return ['365', 'HESFB/2019/07902', 'DEBORAH NAKANYIKE REBECCA', 'F', 'Wakiso', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Orthopedic Medicine', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '375 HESFB/2019/00747 DENIS NYENDE M Iganga Kyambogo University Ordinary Diploma in Science Technology (Biology, Physics, 3C hyeemarisstry) Diploma Eastern':
        return ['375', 'HESFB/2019/00747', 'DENIS NYENDE', 'M', 'Iganga', 'Kyambogo University', 'Ordinary Diploma in Science Technology (Biology, Physics, Chemistry)', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '381 HESFB/2019/06182 DENNIS NYENDE M Iganga Kyambogo University Ordinary Diploma in Science Technology (Biology, Physics, 3C hyeemarisstry) Diploma Eastern':
        return ['381', 'HESFB/2019/06182', 'DENIS NYENDE', 'M', 'Iganga', 'Kyambogo University', 'Ordinary Diploma in Science Technology (Biology, Physics, Chemistry)', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '397 HESFB/2019/05043 DERRICK ODWAR OLARA M Lamwo Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Oicretsh,o Mpuedlaigc oMedicine 3 years Diploma Northern':
        return ['397', 'HESFB/2019/05043', 'DERRICK ODWAR OLARA', 'M', 'Lamwo', 'Kabale', 'Diploma in Orthopedic Medicine', '3 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '447 HESFB/2019/08291 EDITH NSHEMEREIRWE ASHEMEREIRFWE Mbarara Gulu College of Health Science Dip. Medical Laboratory Technology 3 years Diploma Western':
        return ['447', 'HESFB/2019/08291', 'EDITH NSHEMEREIRWE ASHEMEREIRWE', 'F', 'Lamwo', 'Gulu College of Health Science', 'Dip. Medical Laboratory Technology', '3 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '468 HESFB/2019/03299 ELISA AHIMBISIBWE M Kabale Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picuebsl,i Mc Huelaagltoh Dentistry 3 years Diploma Western':
        return ['468', 'HESFB/2019/03299', 'ELISA AHIMBISIBWE', 'M', 'Kabale', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Public Health Dentistry', '3 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '598 HESFB/2019/02432 FRED SSEBATTA M Bukomansimbi Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Miceeds,i cMaul Rlaagdoiography 3 years Diploma Central':
        return ['598', 'HESFB/2019/02432', 'FRED SSEBATTA', 'M', 'Bukomansimbi', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Medical Radiography', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '622 HESFB/2019/07799 GEORGE OKIRIA M Ngora Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picuebsl,i Mc Huelaagltoh Dentistry 3 years Diploma Eastern':
        return ['622', 'HESFB/2019/07799', 'GEORGE OKIRIA', 'M', 'Ngora', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Public Health Dentistry', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '633 HESFB/2019/04512 GIFT JURUGO M Adjumani Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Cicliensi,c Malu &la Cgoommunity Nutrition 3 years Diploma Northern':
        return ['633', 'HESFB/2019/04512', 'GIFT JURUGO', 'M', 'Adjumani', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Clinical & Community Nutrition', '3 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '651 HESFB/2019/03610 GLORIA NAMUTEBI F Wakiso Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Oicretsh,o Mpuedlaigc oMedicine 3 years Diploma Central':
        return ['651', 'HESFB/2019/03610', 'GLORIA NAMUTEBI', 'F', 'Wakiso', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Orthopedic Medicine', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '688 HESFB/2019/01461 Harold Rwothomio M Nebbi Makerere University BSc. Computer Science (Student passes Mathematics/Physic3s y aeta Ar’s Level) Degree Northern':
        return ['688', 'HESFB/2019/01461', 'Harold Rwothomio', 'M', 'Nebbi', 'Makerere University', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree', 'Northern']
    # This line is also messed up
    elif input_string == '740 HESFB/2019/03684 IBRAHIM KASAGGA M Mukono Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picuebsl,i Mc Huelaagltoh Dentistry 3 years Diploma Central':
        return ['740', 'HESFB/2019/03684', 'IBRAHIM KASAGGA', 'M', 'Mukono', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Public Health Dentistry', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '785 HESFB/2019/05302 ISAAC LEMA M Kaabong Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Oicretsh,o Mpuedlaigc oMedicine 3 years Diploma Northern':
        return ['785', 'HESFB/2019/05302', 'ISAAC LEMA', 'M', 'Kaabong', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Orthopedic Medicine', '3 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '990 HESFB/2019/05190 JOVEL MUKISA M Busia Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Miceeds,i cMaul Elangtoomology 3 years Diploma Eastern':
        return ['990', 'HESFB/2019/05190', 'JOVEL MUKISA', 'M', 'Busia', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Medical Entomology', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '1012 HESFB/2019/08117 JULIUS KAMYA M Budaka Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Oicretsh,o Mpuedlaigc oMedicine 3 years Diploma Eastern':
        return ['1012', 'HESFB/2019/08117', 'JULIUS KAMYA', 'M', 'Budaka', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Orthopedic Medicine', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '1029 HESFB/2019/07100 JUSTINE ELSHAMER KASULE M Wakiso Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheyss, iMotuhleargaopy 3 years Diploma Central':
        return ['1029', 'HESFB/2019/07100', 'JUSTINE ELSHAMER KASULE', 'M', 'Wakiso', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Physiotherapy', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '1039 HESFB/2019/07320 KAMILO KIDEGA M Agago Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheasr, mMauclyago 3 years Diploma Northern':
        return ['1039', 'HESFB/2019/07320', 'KAMILO KIDEGA', 'M', 'Agago', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '1063 HESFB/2019/08113 KEVIN JUMA M Busia Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheasr, mMauclyago 3 years Diploma Eastern':
        return ['1063', 'HESFB/2019/08113', 'KEVIN JUMA', 'M', 'Busia', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '1084 HESFB/2019/05885 LAWRENCE KABILA M Kitgum Uganda Martyrs University BSc. Information Technology (Student passed Mathematics/3P yheyasriscs at A ‘Level)Degree Northern':
        return ['1084', 'HESFB/2019/05885', 'LAWRENCE KABILA', 'M', 'Kitgum', 'Uganda Martyrs University', 'BSc. Computer Science (Student passes Mathematics/Physics at A’ Level)', '3 years', 'Degree', 'Northern']
    # This line is also messed up
    elif input_string == '1178 HESFB/2019/06479 MARY KATUSHABE F Nakaseke Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheyss, iMotuhleargaopy 3 years Diploma Central':
        return ['1178', 'HESFB/2019/06479', 'MARY KATUSHABE', 'F', 'Nakaseke', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Physiotherapy', '3 years', 'Degree', 'Northern']
    # This line is also messed up
    elif input_string == '1297 HESFB/2019/02985 NICHOLUS TUGUMISIRIZE M Bunyangabu Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Diceenst, aMl Tuleacghonology 3 years Diploma Western':
        return ['1297', 'HESFB/2019/02985', 'NICHOLUS TUGUMISIRIZE', 'M', 'Bunyangabu', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Dental Technology', '3 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '1350 HESFB/2019/05782 PATRIC SENTONGO M Mityana Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picuebsl,i Mc Huelaagltoh Dentistry 3 years Diploma Central':
        return ['1350', 'HESFB/2019/05782', 'PATRIC SENTONGO', 'M', 'Mityana', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Public Health Dentistry', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '1394 HESFB/2019/06439 PETER LOKORU M Napak Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Cicliensi,c Malu &la Cgoommunity Nutrition 3 years Diploma Northern':
        return ['1394', 'HESFB/2019/06439', 'PETER LOKORU', 'M', 'Napak', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Clinical & Community Nutrition', '3 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '1557 HESFB/2019/03986 SALIIM KALYESUBULA M Kampala Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheasr, mMauclyago 3 years Diploma Central':
        return ['1557', 'HESFB/2019/03986', 'SALIIM KALYESUBULA', 'M', 'Kampala', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '1577 HESFB/2019/07976 SAMUEL OMALA M Kalangala Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picuebsl,i Mc Huelaagltoh Dentistry 3 years Diploma Central':
        return ['1577', 'HESFB/2019/07976', 'SAMUEL OMALA', 'M', 'Kalangala', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Public Health Dentistry', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '1579 HESFB/2019/07915 SAMUEL OMARA M Otuke Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Oicretsh,o Mpuedlaigc oMedicine 3 years Diploma Northern':
        return ['1579', 'HESFB/2019/07915', 'SAMUEL OMARA', 'M', 'Otuke', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Orthopedic Medicine', '3 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '1670 HESFB/2019/02818 SOLOMON OGWAL M Omoro Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheyss, iMotuhleargaopy 3 years Diploma Northern':
        return ['1670', 'HESFB/2019/02818', 'SOLOMON OGWAL', 'M', 'Omoro', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Physiotherapy', '3 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '1683 HESFB/2019/03438 STEPHEN AGONZA M Kyenjojo Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Eicnetso, mMoulloaggyo and Parasitology 3 years Diploma Western':
        return ['1683', 'HESFB/2019/03438', 'STEPHEN AGONZA', 'M', 'Kyenjojo', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Entomology and Parasitology', '3 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '1744 HESFB/2019/02896 TUKESIGA EMMANUEL M Ntungamo Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Oicretsh,o Mpuedlaigc oMedicine 3 years Diploma Western':
        return ['1744', 'HESFB/2019/02896', 'TUKESIGA EMMANUEL', 'M', 'Ntungamo', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Orthopedic Medicine', '3 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '1755 HESFB/2019/03629 UMAR OMURON M Kumi Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Oicretsh,o Mpuedlaigc oMedicine 3 years Diploma Eastern':
        return ['1755', 'HESFB/2019/03629', 'UMAR OMURON', 'M', 'Kumi', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Orthopedic Medicine', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '1771 HESFB/2019/08180 VICTORIA NAKALEMA F Buikwe Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheasr, mMauclyago 3 years Diploma Central':
        return ['1771', 'HESFB/2019/08180', 'VICTORIA NAKALEMA', 'F', 'Buikwe', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '1772 HESFB/2019/07979 VICTORIA NAMAKHONJE F Manafwa Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picheasr, mMauclyago 3 years Diploma Eastern':
        return ['1772', 'HESFB/2019/07979', 'VICTORIA NAMAKHONJE', 'F', 'Manafwa', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '1789 HESFB/2019/02749 VIVIAN NASSUNA F Wakiso Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Picuebsl,i Mc Huelaagltoh Dentistry 3 years Diploma Central':
        return ['1789', 'HESFB/2019/02749', 'VIVIAN NASSUNA', 'F', 'Wakiso', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Public Health Dentistry', '3 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '28 HESFB/2019/06407 AGNES ASIIMWE F Mbarara Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Eicnevsi,r Monumlaegnotal Health Science 2 years Diploma Western':
        return ['28', 'HESFB/2019/06407', 'AGNES ASIIMWE', 'F', 'Mbarara', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Environmental Health Science', '2 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '143 HESFB/2019/08031 ASSUMPTA MARY ATUHAIRE F Masindi Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Miceeds,i cMaul Llaagbooratory Technology 2 years Diploma Western':
        return ['143', 'HESFB/2019/08031', 'ASSUMPTA MARY ATUHAIRE', 'F', 'Masindi', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Medical Laboratory Technology', '2 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '385 HESFB/2019/05170 DEOGRATIUS LUKYAMUZI M Gomba Uganda Institute of Information and CommuDniipclaotmioan sin T Iencfhonrmolaotgiyon Technology 2 years Diploma Central':
        return ['385', 'HESFB/2019/05170', 'DEOGRATIUS LUKYAMUZI', 'M', 'Gomba', 'Uganda Institute of Information and Communications Technology', 'Diploma in Information Technology', '2 years', 'Diploma', 'Central']
    # This line is also messed up
    elif input_string == '664 HESFB/2019/08314 GOODHOPE RWOTOMIYO M Gulu Uganda Institute of Allied Health and ManagDeimp einn tM Seedrvicicael sL,a Mbourlaagtoory Technology 3 years Diploma Northern':
        return ['664', 'HESFB/2019/08314', 'GOODHOPE RWOTOMIYO', 'M', 'Gulu', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Dip in Medical Laboratory Technology', '3 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '879 HESFB/2019/05443 JIMMY WAISWA M Bugiri Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Miceeds,i cMaul Llaagbo Technology 2 years Diploma Eastern':
        return ['879', 'HESFB/2019/05443', 'JIMMY WAISWA', 'M', 'Bugiri', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Medical Laboratory Technology', '2 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '967 HESFB/2019/04551 JOSEPH TEBAKOL M Napak Butabika School of Psychiatric Clinical OfficeDrisploma in Clinical Medicine in Psychiatry 3 years Diploma Northern':
        return ['967', 'HESFB/2019/04551', 'JOSEPH TEBAKOL', 'M', 'Napak', 'Butabika School of Psychiatric Clinical Officers', 'Diploma in Clinical Medicine in Psychiatry', '3 years', 'Diploma', 'Northern']
    # This line is also messed up
    elif input_string == '1078 HESFB/2019/06041 LASTUS NAMANYA M Bushenyi Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Miceeds,i cMaul Llaagbooratory Technology 2 years Diploma Western':
        return ['1078', 'HESFB/2019/06041', 'LASTUS NAMANYA', 'M', 'Bushenyi', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Medical Laboratory Technology', '2 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '1165 HESFB/2019/07933 MARTIN EKELLOT M Katakwi Uganda Institute of Information and CommuDniipclaotmioan sin T Iencfhonrmolaotgiyon Technology 2 years Diploma Eastern':
        return ['1165', 'HESFB/2019/07933', 'MARTIN EKELLOT', 'M', 'Katakwi', 'Uganda Institute of Information and Communications Technology', 'Diploma in Information Technology', '2 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '1193 HESFB/2019/07851 MEDARD AGABA M Bushenyi Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Eicnevsi,r Monumlaegnotal Health Science 2 years Diploma Western':
        return ['1193', 'HESFB/2019/07851', 'MEDARD AGABA', 'M', 'Bushenyi', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Environmental Health Science', '2 years', 'Diploma', 'Western']
    # This line is also messed up
    elif input_string == '1214 HESFB/2019/06665 MIRIAM NAMULI F Mukono Uganda Institute of Allied Health and ManagDeimpleonmt aS einrv Miceeds,i cMaul Llaagbo Technology 2 years Diploma Central':
        return ['1214', 'HESFB/2019/06665', 'MIRIAM NAMULI', 'F', 'Mukono', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Medical Laboratory Technology', '2 years', 'Diploma', 'Central']
    elif match:
        return list(match.groups())
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
