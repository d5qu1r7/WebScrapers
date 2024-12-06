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

URL = ''
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2024_successful_loan_applicants.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@timer
def extract_data():
    with pdfplumber.open(PDF_PATH) as pdf:
        pdf_length = len(pdf.pages)

        for j in range(pdf_length):

            page_text = pdf.pages[j].extract_text().split('HESFB')

            if j == 0:
                for i, text in enumerate(page_text):
                    row = []
                    if i == 0:
                        row = ['Application No.', 'Name of Applicant', 'Gender', 'District of Origin', 'Admitted University', 'Admitted Course', 'Course Duration', 'Course Type']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_loan_applicants')
                    else:
                        if text == '' or text[:4] == 'Page':
                            continue
                        row = transform_string(text)

                        if row is None:
                            continue

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_loan_applicants')
                continue

            for i, text in enumerate(page_text):
                    if i == 0:
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

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_loan_applicants')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(HESFB/2024/\d+)\s*(.*?)\s+([FM])\s+([-A-Za-z]+)\s+((?:ISBAT|Soroti|School|Adjumani|Muteesa|Islamic|Ndejje|Bishop|Kampala|Busitema|Muni|Kyambogo|University|Makerere|Nkumba|International|Institute|Mountains|Uganda|Gulu|NAKAWA|Mbarara|Kabale|Lira|Victoria|Bugema|Bukalasa)(?:.*?))((?:BSc|Bsc|BSC|B\.|Diploma|Dip|B |Bachelor|BACHELOR|Bachelof|BA |BA.|NATIONAL HIGHER|Foundation Programme)\s*(?:.*?))(\d+.+years)\s+([A-Za-z]+)'
    pattern_13 = r'(HESFB/2024/\d+)\s*(Uganda Technical College,|Uganda Technical|NAKAWA VOC TRAINING|Uganda Institute of Allied|Mbarara University of Science|Mbale College of Health|MakerereUniversityBusiness|Uganda Petroleum Institute|Mulago School of Nursing and|Ophthalmic Clinical Officers|Soroti School of|Institute of Survey and Land|Arua School of Comprehensive)\s*(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(.*?)((?:BSc|Bsc|BSC|B\.|Diploma|Dip|B |Bachelor|BACHELOR|Bachelof|BA |NATIONAL HIGHER|Foundation Programme)(?:.*?))(\d+.+years)\s+([A-Za-z]+)'
    pattern_10 = r'(HESFB/2024/\d+)\s*(Diploma in Computer Science and|Bachelor of Computer Science and|B. Medical Laboratory Technology|Bachelor of Science in Applied Information|Dip in Clinical Medicine and Community|National Diploma in Civil & Building|Bachelor of Science in Agri-Entrepreneurship and Communication|National Diploma in Water and Sanitation|Bachelor of Tourism and Hospitality|BSC in Agri Entrepreneurship and|Bachelor of Education External -|B of Information Technology and)(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(.*?)(Information Technology|\(Direct\)|Technology|Health|Engineering|Management|Eng|Communication MGT|Secondary|Computing)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_22 = r'(HESFB/2024/\d+)\s*(BACHELOR OF SCIENCE EDUCATION -)(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(.*?)(BIOLOGY|PHYSICS|MATHEMATICS|ENTREPRENEURSHIP|AGRICULTURE|ECONOMICS)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_26 = r'(HESFB/2024/\d+)\s*(.*?)\s*(Bachelor of Artificial Intelligence and|Bachelor of Science in Human Nutrition|Bachelor of Demography and|Bachelor of Engineering in|Bachelor of Education \(Physics and|Bachelor of Medicine and Bachelor of|Bachelor of Tourism and Hospitality|Bachelor of Science Technology -|Bachelor of Science in Animation and|B. Agriculture and Community|Diploma in Food Science and Processing)\s*(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(.*?)(Machine Learning|and Dietetics|Reproductive Health|Telecommunications Engineering|Mathematics\)|Surgery|Management|Chemistry|Visual Effects|Development|Technology)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_27 = r'(HESFB/2024/\d+)\s*(.*?)\s*(Jinja School of Nursing and|Uganda Technical|Uganda Technical College,|Mbarara University of Science|Soroti School of|Uganda Institute of Allied|Mulago School of Nursing and|NAKAWA VOC TRAINING)\s*(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(Midwifery|College,Elgon|Kichwamba|Bushenyi|and Technology|Nursing|Health & Mgt Svs|Comprehensive Nursing|COLLEGE)\s+(.*?)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_29 = r'(HESFB/2024/\d+)\s+(.*?)\s+(Kampala International)\s+(Bachelor of Computer Science with|Diploma in Clinical Medicine and)(\S*?)\s*([FM])\s+([A-Za-z]+)\s+(University)\s+(Community Health|Education)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_23 = r'(HESFB/2024/\d+)\s*((?:Bachelor of |BACHELOR OF |B of |B in |B |B. |B. of |B. in |BSc. |Bsc. |BSC. |Bsc. in |BSc in |Bsc. of |B.Sc. |Bsc |BSC |BSc in |Bsc of |Diploma in |Dip. |National Diploma in |Higher Diploma in |Diploma In )(?:Science in Software|Leisure, Tourism and Hotel|Food Science and Processing|Science Technology -|Agricultural and Rural|Science in Biosystems|SCIENCE EDUCATION|Demography and|Engineering in|Engineering - Electronics and|Science in Human Nutrition|Science with Education -|Information Technology and|Science in Quantitative|Science in Water Resource|Vocational Studies in|Science in Chemical and|Science in Animation and|Science in EnvironmentalScience and Natural Resources|Science in Fisheries and|Adult and Community|Agricuture and Community|Animal Production And|Computer Science and|Water and Sanitation|Mechanical|Civil and Building|Toursim and Hotel|Animal Production Technology|Industrial Engineering and|Science in Agribusiness|Education \(Physics and|Hotel and Hospitality|Agribusiness Management and|Artificial Intelligence and|Science in Industrial|Science in Networking and|Eng in Electronics and|Agriculture and Community|Vocational Studies in Agric with|Mechatronics and Biomedical|Agri-Entrepreneurship and|Computer Science & Information|Agricultural Economics and|Artificial Intelligence & Machine|Agribusiness Management &|Engineering in Civil and Building|Clinical Medicine & Community|Environmental Science Technology|Building & Civil|Ginning and Industrial|Eng in Mechanical and Manufacturing|Information and Communication|Crop Production And|Hotel and Institutional|Science in Food Science and|Cooperative Agribusiness|Science in Computer|Agribusiness & Community|Tourism and Hospitality|Refrigeration and Air|Fisheries and Water Resources|Environmental Sc and Natural|Science in Natural Resources|Science in Textile and Clothing|Agricultural Science and|Agricultural Land Use and|Agribusiness Management|Science in Chemical|Education \(Biology and|Refrigeration & Air|Science in Economics and))(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(.*?)(Engineering|Technology|Chemistry|Innovation|\(PHYSICAL\)|Reproductive Health|Telecommunications Engineering|Communication|Management|and Dietetics|Mathematics|Computing|Economics|Engineering|Agriculture with Education|Processing Engineering|Visual Effects|Aquaculture|Education|Development|Information|Innovation and Management|Mathematics\)|Community Development|Machine Learning|Cyber Security|Communication Management|Agribusiness MGT|Learning|and MGT|Health|Catering|Conditioning Engineering|Resource MGT|Technology \(TCD\)|Entrepreneurship|&CommunityDevelopment|Chemistry\)|Conditioning|Statistics|)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_24 = r'(HESFB/2024/\d+)\s*(B of Eng in Automotive and Power)(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(.*?)(Engineering)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_14 = r'(HESFB/2024/\d+)\s*(Uganda Technical College,)\s+(National Diploma in Mechanical)(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(Kyema, Masindi)\s+(Engineering)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_21 = r'(HESFB/2024/\d+)\s*(Kampala International|Uganda Technical College,|Uganda Technical|Mbarara University of Science|MakerereUniversityBusinessS|Uganda Institute of Inform &|Fortportal Colleg of Health|NAKAWA VOC TRAINING)\s+(Bachelor of Science with Environmental|Bachelor of Science in Enviromental|Bachelor of Science in Mechanical|Bachelor of Science in Electrical|Bachelor of Computer Science with|Bachelor of Toursim and Hotel|BSc in Mechanical and Industrial|B. Petroleum Engineering &|Bachelors of Electrical and Electronic|BSc in Petroleum Engineering and|Diploma in Clinical Medicine & Community|Diploma in Clinical Medicine and|Diploma in Medical Laboratory|Diploma in Refrigeration & Air|National Diploma in Mechanical|National Diploma in Civil & Building|Higher Diploma in Building & Civil|Bachelor of Petroleum Engineering and|B. Engineering in Electrical & Electronics|Bachelor of Science in Software|Bachelor of Medicine and Bachelor of|Bachelor of Tourism and Hospitality|Dip in Electrical and Electronics|Dip in Clinical Medicine and Community|Diploma in Computer Science)(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(University|College,Elgon|Kichwamba|Bushenyi|and Technology|ch|Coms Tech|Sciences|COLLEGE)\s+(Management|Enginering|Engineering|Health|Community Health|Education|Technology|Conditioning|Environmental|Environment Mgt|Environmental Mgt|Environment Mgt|Environmental Management|Enginee|Surgery|Information Technology)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_25 = r'(HESFB/2024/\d+)\s*(Bukomansi|Kaberamaid)\s*(Kampala International| )\s*(Bachelor of Science in Applied|Bachelor of Computer Science and|Diploma in Clinical Medicine & Community)\s*(.*?)\s+([FM])\s+(mbi|o)\s+(University|Kampala University)\s+(Mathematics and Statistics|Information Technology|Health)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_30 = r'(HESFB/2024/\d+)\s*(Kaberamaid|Kapelebyon)\s*(B of Agricultural Economics and|B of Vocational Studies in Agric with)\s*(.*?)\s+([FM])\s+(g|o)\s+([A-Za-z]+)\s+(.*?)\s+(Agribusiness MGT|Education)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_31 = r'(HESFB/2024/\d+)\s+(Kiryandong)\s+(Uganda Technical College,)\s*(.*?)\s+([FM])\s+(o)\s+(.*?)\s+(Diploma in Civil Engineering)\s+(\d+.+years)\s+([A-Za-z]+)'
    pattern_28 = r'(HESFB/2024/\d+)\s*(Nakapiripiri)\s*(Bachelor of Science with Education -|Bachelor of Science in Computer)\s*(.*?)\s+([FM])\s+(t)\s+(.*?)\s+(Engineering|Secondary)\s+(\d+.+years)\s+([A-Za-z]+)'
    
    input_string = input_string.replace('\n', '')
    input_string = f'HESFB{input_string}'

    match = re.match(pattern, input_string)
    match_10 = re.match(pattern_10, input_string)
    match_13 = re.match(pattern_13, input_string)
    match_14 = re.match(pattern_14, input_string)
    match_21 = re.match(pattern_21, input_string)
    match_22 = re.match(pattern_22, input_string)
    match_23 = re.match(pattern_23, input_string)
    match_24 = re.match(pattern_24, input_string)
    match_25 = re.match(pattern_25, input_string)
    match_26 = re.match(pattern_26, input_string)
    match_27 = re.match(pattern_27, input_string)
    match_28 = re.match(pattern_28, input_string)
    match_29 = re.match(pattern_29, input_string)
    match_30 = re.match(pattern_30, input_string)
    match_31 = re.match(pattern_31, input_string)
    
    if match:
        return list(match.groups())
    elif match_10:
        return [match_10.group(1), match_10.group(3), match_10.group(4), match_10.group(5), match_10.group(6), f'{match_10.group(2)} {match_10.group(7)}', match_10.group(8), match_10.group(9)]
    elif match_13:
        return [match_13.group(1), match_13.group(3), match_13.group(4), match_13.group(5), f'{match_13.group(2)} {match_13.group(6)}', match_13.group(7), match_13.group(8), match_13.group(9)]
    elif match_14:
        return [match_14.group(1), match_14.group(4), match_14.group(5), match_14.group(6), f'{match_14.group(2)} {match_14.group(7)}', f'{match_14.group(3)} {match_14.group(8)}', match_14.group(9), match_14.group(10)]
    elif match_21:
        return [match_21.group(1), match_21.group(4), match_21.group(5), match_21.group(6), f'{match_21.group(2)} {match_21.group(7)}', f'{match_21.group(3)} {match_21.group(8)}', match_21.group(9), match_21.group(10)]
    elif match_22:
        return [match_22.group(1), match_22.group(3), match_22.group(4), match_22.group(5), match_22.group(6), f'{match_22.group(2)} {match_22.group(7)}', match_22.group(8), match_22.group(9)]
    elif match_23:
        return [match_23.group(1), match_23.group(3), match_23.group(4), match_23.group(5), match_23.group(6), f'{match_23.group(2)} {match_23.group(7)}', match_23.group(8), match_23.group(9)]
    elif match_24:
        return [match_24.group(1), match_24.group(3), match_24.group(4), match_24.group(5), match_24.group(6), f'{match_24.group(2)} {match_24.group(7)}', match_24.group(8), match_24.group(9)]
    elif match_25:
        return [match_25.group(1), match_25.group(5), match_25.group(6), f'{match_25.group(2)}{match_25.group(7)}', f'{match_25.group(3)} {match_25.group(8)}', f'{match_25.group(4)} {match_25.group(9)}', match_25.group(10), match_25.group(11)]
    elif match_26:
        return [match_26.group(1), f'{match_26.group(2)} {match_26.group(4)}', match_26.group(5), match_26.group(6), match_26.group(7), f'{match_26.group(3)} {match_26.group(8)}', match_26.group(9), match_26.group(10)]
    elif match_27:
        return [match_27.group(1), f'{match_27.group(2)} {match_27.group(4)}', match_27.group(5), match_27.group(6), f'{match_27.group(3)} {match_27.group(7)}', match_27.group(8), match_27.group(9), match_27.group(10)]
    elif match_28:
        return [match_28.group(1), match_28.group(4), match_28.group(5), f'{match_28.group(2)}{match_28.group(6)}', match_28.group(7), f'{match_28.group(3)} {match_28.group(8)}', match_28.group(9), match_28.group(10)]
    elif match_29:
        return [match_29.group(1), f'{match_29.group(2)} {match_29.group(5)}', match_29.group(6), match_29.group(7), f'{match_29.group(3)} {match_29.group(8)}', f'{match_29.group(4)} {match_29.group(9)}', match_29.group(10), match_29.group(11)]
    elif match_30:
        return [match_30.group(1), match_30.group(4), match_30.group(5), f'{match_30.group(2)}{match_30.group(6)}', f'{match_30.group(7)} {match_30.group(8)}', f'{match_30.group(3)} {match_30.group(9)}', match_30.group(10), match_30.group(11)]
    elif match_31:
        return [match_31.group(1), match_31.group(4), match_31.group(5), f'{match_31.group(2)}{match_31.group(6)}', f'{match_31.group(3)} {match_31.group(7)}', match_31.group(8), match_31.group(9), match_31.group(10)]
    else:
        print(input_string)
        return None

if __name__ == "__main__":
    extract_data()
