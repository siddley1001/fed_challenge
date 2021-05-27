import os
import pandas as pd
from datetime import date
from fredapi import Fred

'''
Download all the series in a for loop
merge them all into a panda's dataframe
save them to dataframe to a sheet in an excel workbook


params: start, end, sheet, workbook
'''


KEY = 'dde5ad634e39b6e288c9a2ebec181e58'
fred = Fred(api_key=KEY)


#start = date.today()
#end = input("Input your END date")

start = '07-01-2010'
end = '05-26-2021'
excel_path = input('Input the EXCEL PATH including the .xlsx workbook')
sheet_name = input('Input the SHEET NAME to upload to in the .xlsx file')
# final_df = pd.DataFrame()
#
# # for k,v in econ_dictionary.items():
# #     series = fred.get_series(k, start, end)
# #     df = pd.DataFrame(series, columns = v)
# #
# #     final_df = pd.concat([final_df, df], axis=1)
# #
# # final_df.to_excel(excel_path, sheet_name=sheet_name, index=False)
df = pd.read_excel(excel_path, sheet_name=sheet_name)
df[]

'''test'''