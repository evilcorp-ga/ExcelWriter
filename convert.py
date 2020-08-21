import pandas as pd
import os
from io import StringIO

def convert(path, filename, csv, sep=",", skiprows=4):
    stream = StringIO(csv)
    df = pd.read_csv(stream, sep=sep, skiprows=skiprows)
    output_path = os.path.join(path, filename)
    df.to_excel(output_path, index=False)
    return output_path

def convert_csv_file(in_filename, out_filename):
    df = pd.read_csv(in_filename, sep=sep)
    df.to_excel(out_filename)

def convert_json_file(in_filename, out_filename):
    df = pd.read_json(in_filename, out_filename, orient='index')
    df.to_excel(out_filename)
