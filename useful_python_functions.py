# Useful python functions
import os
import sys
import re 
import glob
import datetime as dt
import pandas as pd 
import numpy as np
import xlrd
import xlsxwriter
import xlwt
import itertools
import warnings
warnings.simplefilter("ignore")


def list_all_excel_files(filedir):
    #Print out all the  .xlsx files in the directory
    os.chdir(filedir)
    for file_names in glob.glob("*.xlsx"):
        print(file_names)

def import_csv_or_xlsx_files(file_directory, file_name, sheet_name='None'):
    # Import files into dataframes either .csv or .xlsx 
    # Read in excel
    if file_name.lower().endswith(('.xlsx')):
        in_df = pd.read_excel(str(file_directory)+str(file_name), skiprows=[0,1])
    else: 
    #Read in csv
        in_df = pd.read_csv(str(file_directory)+str(file_name), encoding='utf-8', low_memory=False)
    return(in_df)
    

def remove_blank_cols_in_dataframe(in_df):
    # Remove blank columns
    # Find the columns where each value is null
    empty_cols = [col for col in in_df.columns if in_df[col].isnull().all()]
    # Drop these columns from the dataframe
    in_df.drop(empty_cols,
            axis=1,
            inplace=True)
    return(in_df)

def rename_df_col(in_df, col_name, new_name):
    # Rename the column
        in_df.rename(columns=lambda x: x.replace(col_name, new_name), inplace=True)

def create_categories(in_df, categories, values, cat_name, col_name):
    # Create NPS segments
    #Categorize into NPS Segments (Promoter, Passive, Detractor)
    categories = [
    (in_df[col_name]), # Some rule >, =, <, ==''
    (in_df[col_name]) | (in_df[col_name]), # An OR list of rules
    (in_df[col_name]) & (in_df[col_name]) # An AND list of rules
    ]
    # Create a list of the values we want to assign for each segment
    values = ['value1', 'value2', 'value3'] # Whatever the values of the categories you want
    # create a new column and use np.select to assign values to it using our lists as arguments
    in_df[cat_name] = np.select(categories, values)
    return(in_df)

def write_out_dataframe_to_excel(in_df, file_name, sheetname=None):
      # Write out dataframes to excel files
    if sheetname:
       # write to specific sheet  
        in_df.to_excel(str(file_name)+'.xlsx', sheet_name=sheetname,index=False)
    else: in_df.to_excel(str(file_name)+'.xlsx', index=False)
    return()

def get_summary(in_df, value, rows, cols):
    # Summarize a dataframe by a specific column
    # Pivot at Brand Level
    pvt = pd.pivot_table(data=in_df, values=value, 
                            index=[rows], columns=[cols], 
                            aggfunc='nunique', fill_value=0, margins=True, dropna=True, margins_name='Total')
    #Put the pivotable back to a dataframe
    out_df = pd.DataFrame(pvt.to_records())
    return(out_df)

def create_moyr(in_df):
    #Create  a month and year field from a timestamp field
    # Find the column  which is a timestamp
    timestamp_cols = [col for col in in_df.columns if in_df[col].istype(dt.timestamp).all()]
    # Change it to a MoYr
    for item in timestamp_cols:
        in_df[str(in_df[item])+'MoYr'] = in_df[item].dt.to_period('M')

def write_dataframe_with_xlswriter(in_df, sheetname, filedir, filename ):
    # another way to write out edataframe to excel
    writer = pd.ExcelWriter(str(filedir)+str(filename)+".xlsx", engine='xlsxwriter')
    in_df.to_excel(writer,sheet_name=sheetname)
    writer.save()
    return()

def iterate_through_dataframe(in_df):
    for index, row in in_df.iterows():
        print (index, row[col])
    return()

def get_todays_date():
    from datetime import datetime, date, time, timezone
    latestdate = (date.today())
    return(latestdate)

def do_db2_conn():
    import ibm_db
    import os
    os.export(IBM_DB2_HOME='/Users/kelleyanders/Documents/CMDP_Drivers/db2jcc4.jar')
    ibm_db_conn = ibm_db.connect('bigsql-1686735759686280-jdbc-tls-prod-cdo-cedp-bigsql.apps.wdc-cdo-prod.core.cirrus.ibm.com:443/bigsql', 'kelleyb@us.ibm.com', 'J3su5CHr!st1sKing')
    import ibm_db_dbi
    conn = ibm_db_dbi.Connection(ibm_db_conn)
    conn.tables('SYSCAT', '%')
    return()

def do_sqlalchemy_dbconn():
    import sqlalchemy
    from sqlalchemy import *
    import ibm_db_sa
    db2 = sqlalchemy.create_engine('ibm_db_sa://kelleyb@us.ibm.com:J3su5CHr!st1sKing@bigsql-1686735759686280-jdbc-tls-prod-cdo-cedp-bigsql.apps.wdc-cdo-prod.core.cirrus.ibm.com:443/bigsql')
    metadata = MetaData()
    return()

def list_files(rootdir):
    # Walk the directory and find the file
    for file in os.listdir(rootdir):
        print((file))
    return()

def walk_file_structure(rootdir):
    # List out all the files in the directories
    import os
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            print(os.path.join(subdir, file))
    return()