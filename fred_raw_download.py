import os
import pandas as pd
from fredapi import Fred

'''
Download all the series in a for loop
merge them all into a panda's dataframe
save them to dataframe to a sheet in an excel workbook


params: start, end, sheet, workbook
'''


KEY = 'dde5ad634e39b6e288c9a2ebec181e58'
fred = Fred(api_key=KEY)

econ_dictionary = {
    # GDP
    'GDPC1': ['Real GDP $B'], 'A939RC0Q052SBEA': ['GDP/Capita'],
    'PCECC96':['TOTAL $B'],'DGDSRX1Q020SBEA':['Goods $B'],'PCESVC96':['Services $B'],
    'GPDIC1': ['TOTAL $B'], 'PNFIC1': ['Nonresidential $B'], 'PRFIC1': ['Residential $B'], 'CBIC1': ['Change in Private Inventory'],
    'GCEC1': ['TOTAL $B'], 'FGCEC1': ['Federal $B'], 'SLCEC1': ['State/Local $B'],
    'NETEXC': ['NET Exports $B'], 'EXPGSC1': ['Exports $B'], 'IMPGSC1': ['Imports $B'],
    ##Housing Market
    'NHSUSSPT': ['Total New Houses Sold (1,000s of Units)'],'EXHOSLUSM495S': ['Existing Houses Sold (1,000s of Units)'], 'MNMFS': ['Months on Maarket'], 'USSTHPI': ['House Price Index'],
    # Manufacturing Market
    'IPMAN': ['Industrial Production Manufacturing Index'], 'IPG331S': ['Durable Goods - Primary Metals'],
    'IPG334S': ['Durable Goods - Computer and Electronic Products'], 'IPG3361T3S': ['Durable Goods - Motor Vehicles and Parts'],
    'IPG337S': ['Durable Goods - Furniture and related products'], 'IPG315A6S': ['Non-Durable Goods - Apparel and Leather Goods'],
    'GFDEBTN': ['Public Debt $M'], 'GFDEGDQ188S': ['Public Debt/Gross GDP Ratio'], 'MTSDS133FMS': ['Federal Surplus or Deficit'], 'FYFSGDA188S': ['Federal Surplus or Deficit as Ratio of GDP'],
    'NFCI': ['NFCI'],

    # Labor Market
    'UNRATE': ['U3 Rate %'], 'U6RATE': ['U6 Rate %'], 'NROU': ['Natural Unemployment Rate %'],
    'CIVPART': ['Cumm. LFPR %'], 'LNS11300002': ['Women LFPR%'], 'LNS11300001': ['Men LFPR%'],
    'LNS11300012': ["16-19yrs LFPR %"], 'LNS11300036': ['20-24yrs LFPR %'] ,'LNS11300060': ['25-54yrs LFPR %'], 'LNS11324230': ['55+yrs LFPR %'],
    'LNS11300003': ['White LFPR %'], 'LNS11300006': ['Black LFPR %'], 'LNS11300009': ['Hispanic LFPR %'], 'LNU01332183': ['Asian LFPR %'],
    'ICSA': ['Initial Jobless Claims'], 'IC4WSA': ['4 wk MA of Initial Claims'], 'CCSA': ['Continued Claims (Insured Unempl.)'], 'CC4WSA': ['4wk MA of Continued Claims'],
    'FRBKCLMCIM': ['Labor Market Momentum'], 'FRBKCLMCILA': ['Labor Market Level of Activity'],

    # Fed's Tools
    'DFF': ['Daily EFF rate'], 'FEDTARRM': ['EFF Midpoint Projection'],
    'T20YIEM':  ['20 yr CPI'], 'EFFR': ['Median EFFR'],
    'INTDSRUSM193N': ["Fed's Discount Rate"], 'IORR': ['% on Required Reserves'], 'IOER': ['% on Excess Reserves'],
    'RPONAGYD': ['Repos Purchased $B'], 'RRPONTSYD': ['Repos Sold $B'],
    'DGS30': ['30 Year %'], 'DGS10': ['10 Year %'], 'DGS2': ['2 Year %'],
    'RESPPLLDTXAWXCH52NWW': ['Weekly Net Change in General Account $M'],

    #Inflation
    'USACPIALLMINMEI': ['Inflation level'], 'PPIACO': ['PPI Level'], 'PCEC96': ['Real PCE Level'],
    'DSPIC96': ['Real Disposable Income $B']
}



#start = input("Input your START date")
#end = input("Input your END date")

start = '07-01-1954'
end = '04-25-2021'
excel_path = input('Input the EXCEL PATH including the .xlsx workbook')
sheet_name = input('Input the SHEET NAME to upload to in the .xlsx file')
final_df = pd.DataFrame()

for k,v in econ_dictionary.items():
    series = fred.get_series(k, start, end)
    df = pd.DataFrame(series, columns = v)

    final_df = pd.concat([final_df, df], axis=1)

final_df.to_excel(excel_path, sheet_name=sheet_name, index=False)
