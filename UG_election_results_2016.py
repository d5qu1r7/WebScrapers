import pdfplumber
import pandas as pd

"""
pip install pdfplumber
pip install pandas
"""

PDF_PATH = 'w:/RA_work_folders/Davis_Holdstock/Africa/Uganda_data/UG_election_results_2021_parliamentary/UG_election_results_2021_parliamentary.pdf'
SAVE_FILE_PATH = '' # FIXME: Change to the perminant file path the .csvs will be stored in


def extract_tables_from_all_pages(pdf_path, output_csv):
    # Initialize an empty list to hold all the DataFrames
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:

        category_name = ''

        # Loop through each page
        for page_num, page in enumerate(pdf.pages):

            # For testing purposes only
            # if page_num > 1:
            #     continue

            table = page.extract_table()
            
            # Convert to a DataFrame if a table is found
            if table:
                if page_num == 0:
                    df = pd.DataFrame(table[2:], columns=table[1])  # First row as column names
                else:
                    df = pd.DataFrame(table[1:], columns=table[0])  # First row as column names

#----------------------------------------------------------------- This Checks for a row with the Category in it -----------------------------------------------------------------#
                # First, reset the index if necessary
                if df.index.name is None and df.columns.name == 'District':
                    df = df.reset_index()

                # Now, find the column that contains 'CATEGORY:'
                category_column = None
                for col in df.columns:
                    if df[col].astype(str).str.contains('CATEGORY:', case=False).any():
                        category_column = col
                        break

                if category_column is not None:
                    # Find the row containing 'CATEGORY:'
                    category_row = df[df[category_column].astype(str).str.contains('CATEGORY:', case=False)]

                    if not category_row.empty:
                        # Extract the category name
                        category_name = category_row[category_column].iloc[0].replace("\nCATEGORY:", "")
                        
                        # Print the category name
                        print("Category name:", category_name)

                        # Remove the category row in-place
                        df.drop(df[df[category_column].astype(str).str.contains('CATEGORY:', case=False)].index, inplace=True)
                        df = df.drop(df.index[0])
                        print("Category row removed.")
                    else:
                        print("No category row found. DataFrame remains unchanged.")
                else:
                    print("No column containing 'CATEGORY:' found.")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                # This deletes the empty column at the end to format all tables the same
                # if page_num <= 4:
                #     df = df.iloc[:, :-1]

                # Add category column to the Dataframe
                df['Category'] = category_name

                all_tables.append(df)  # Append the DataFrame to the list
                print(f"Table extracted from page {page_num + 1}")
            else:
                print(f"No table found on page {page_num + 1}")

    # If any tables were extracted, concatenate them into a single DataFrame
    if all_tables:
        combined_df = pd.concat(all_tables, ignore_index=True)
        
        # Output the combined DataFrame to CSV
        combined_df.to_csv(f'{SAVE_FILE_PATH}{output_csv}', index=False)
        print(f"All tables have been written to {SAVE_FILE_PATH}{output_csv}.")
    else:
        print("No tables found in the entire document.")


if __name__ == "__main__":
    # Specify the path to the PDF and the desired output CSV file
    extract_tables_from_all_pages(PDF_PATH, 'data.csv')
