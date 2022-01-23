#!/usr/bin/env python
# coding: utf-8



import originpro as op
import pandas as pd
import os
import re


# location of sample data files that ship with Origin.
counts = 0
def read_data(freq='Frequency', magnitude='Magnitude', reference_book = 'Book1.ogwu'):
    temp     = []
    power    = []
    frequency = [] 
    # Iterate data file folder for file names to import.
    for file in os.listdir(data_folder):
        counts=+1
        print(f'working on {file}')
        imp_file = os.path.join(data_folder, file)
        power.append(int(re.search(r'-?\d+', file.split('_')[-1].split('.')[0]).group()))
        # Load analysis template book that ships with Origin.
        at = op.load_book(prime_folder + reference_book)
        print(at)
        # This template put Data sheet as 1st worksheet in book.
        wks = at[0]
        # Import the file into the worksheet and removing the Data Connector.
        wks.from_file(imp_file, True)
        # Wait for analysis operation to complete.
        op.wait()
        df = at[1].to_df()
        temp.append(df[magnitude])
        if len(frequency) == 0:
            frequency.append(df[freq])
    return temp, power, frequency[0]




def convert_to_excel(mag, power, frequency, excelfilename='converted_file.xlsx'):
    df = pd.DataFrame()
    df['Frequency'] = frequency
    for count, item in enumerate(power):
        df[item] = mag[count]
    df.to_excel(excelfilename)  

def convert_to_csv(mag, power, frequency, csvfilename='converted_file.csv'):
    df = pd.DataFrame()
    df['Frequency'] = frequency
    for count, item in enumerate(power):
        df[item] = mag[count]
    df.to_csv(csvfilename)
    


#specify the path
prime_folder ='C:\\Users\\Uday Aalto Account\\OneDrive - Aalto University\\Documents\\mumax\\Abhishek\\'
data_folder   = prime_folder+'data_folder'
# values can be changed accordingly
# magnitude: fft convert data
# power    : column name
# frequency: first column
magnitude, power, frequency = read_data(freq='Frequency', magnitude='Power as MSA', 
                                        reference_book = 'Book1.ogwu')
convert_to_excel(magnitude, power, frequency, excelfilename='converted_file.xlsx')
convert_to_csv(magnitude, power, frequency, csvfilename='converted_file.csv')

if counts==len(magnitude):
    print('File successfully created')
else:
    print('Please check the parameters')

