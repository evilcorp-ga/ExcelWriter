import pandas as pd
from bs4 import BeautifulSoup
import os
from io import StringIO
converter = {}

def htmler(value):
    soup = BeautifulSoup(value,features="lxml")
    return soup.get_text(separator='\n')

for i in range(0,100):
    converter[i] = htmler

def convert(path, filename, csv, sep=",", skiprows=4):
    stream = StringIO(csv)
    df = pd.read_csv(stream, sep=sep, skiprows=skiprows, converters=converter)
    output_path = os.path.join(path, filename)
    #Set destination directory to save excel.
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    #Indicate workbook and worksheet for formatting
    workbook = writer.book
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    worksheet = writer.sheets['Sheet1']
    #Iterate through each column and set the width == the max length in that column. A padding length of 2 is also added.
    for i, col in enumerate(df.columns):
        # find length of column i
        column_len = df[col].astype(str).str.len().max()
        # Setting the length if the column header is larger
        # than the max column value length
        column_len = max(column_len, len(col)) + 2
        #Make sure its not too big
        if column_len > 125:
            column_len = 125
        # set the column length
        worksheet.set_column(i, i, column_len)
    worksheet.set_default_row(25)
    writer.save()
    return output_path

def convert_csv_file(in_filename, out_filename):
    df = pd.read_csv(in_filename, sep=sep)
    df.to_excel(out_filename)

def convert_json_file(in_filename, out_filename):
    df = pd.read_json(in_filename, out_filename, orient='index')
    df.to_excel(out_filename)
