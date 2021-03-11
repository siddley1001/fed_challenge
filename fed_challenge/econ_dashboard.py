import os

import pandas as pd
import streamlit as st
from fredapi import Fred

os.chdir('/Users/vanamsid/quick_py/fed_challenge')

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
    ##Manufacturing Market
    'IPMAN': ['Industrial Production Manufacturing Index'], 'IPG331S': ['Durable Goods - Primary Metals'],
    'IPG334S': ['Durable Goods - Computer and Electronic Products'], 'IPG3361T3S': ['Durable Goods - Motor Vehicles and Parts'],
    'IPG337S': ['Durable Goods - Furniture and related products'], 'IPG315A6S': ['Non-Durable Goods - Apparel and Leather Goods'],
    'GFDEBTN': ['Public Debt $M'], 'GFDEGDQ188S': ['Public Debt/Gross GDP Ratio'], 'MTSDS133FMS': ['Federal Surplus or Deficit'], 'FYFSGDA188S': ['Federal Surplus or Deficit as Ratio of GDP'],
    'NFCI': ['NFCI']
    # Labor Market
}


def to_df(series_name, start_date, end_date):
    series = fred.get_series(series_name, start_date, end_date)
    df = pd.DataFrame(series, columns=econ_dictionary[series_name])
    df.index = df.index.date
    return df

major_selection = st.sidebar.selectbox(
    'Explore Indicators for:',
    ('Overall Economic Activity', 'Labor Market', 'Price Level and Interest Rates')
)

start_date = st.sidebar.date_input('START Date')
end_date = st.sidebar.date_input('END Date')

if major_selection == 'Overall Economic Activity':
    st.header('Overall Economic Activity')

    st.subheader('Gross Domestic Product (GDP)')
    gdp = to_df('GDPC1', start_date, end_date)

    st.line_chart(gdp)
    st.write('Updates *Quarterly*')

    st.subheader('GDP/Capita')
    gdp_percap = to_df('A939RC0Q052SBEA', start_date, end_date)
    st.line_chart(gdp_percap)
    st.write('Updates *Quarterly*')

    st.write('Use the drop box to Look at the GDP through its 4 main components')

    gdp_components = st.selectbox("4 Main Components",
                                  ('Consumption', 'Investment', 'Government Expenditure', 'Net Exports'))
    if gdp_components == 'Consumption':
        st.subheader('Personal Consumption Expenditures')
        c = to_df('PCECC96', start_date, end_date)
        c_goods = to_df('DGDSRX1Q020SBEA', start_date, end_date)
        c_services = to_df('PCESVC96', start_date, end_date)
        c_total = pd.concat([c, c_goods, c_services], axis=1)

        st.line_chart(c_total)
        st.write('Updates *Quarterly*')

    if gdp_components == 'Investment':
        st.subheader('Gross Private Domestic Investment')
        st.write("Where the majority of Investments are *Nonresidential*")

        i = to_df('GPDIC1', start_date, end_date)
        i_res = to_df('PRFIC1', start_date, end_date)
        i_nonres = to_df('PNFIC1', start_date, end_date)
        i_inventory = to_df('CBIC1', start_date, end_date)
        i_total = pd.concat([i, i_res, i_nonres], axis=1)

        st.line_chart(i_total)
        st.write('Updates *Quarterly*')

        inv_change = st.checkbox('Change in Real Private Inventory')
        if inv_change:
            st.line_chart(i_inventory)
            st.write('Updates *Quarterly*')

    if gdp_components == 'Government Expenditure':
        st.subheader('Government Consumption Expenditures and Investment')
        gov_exandinv = to_df('GCEC1', start_date, end_date)
        gov_fed = to_df('FGCEC1', start_date, end_date)
        gov_statelocal = to_df('SLCEC1', start_date, end_date)
        gov_total = pd.concat([gov_exandinv, gov_fed, gov_statelocal], axis=1)

        st.line_chart(gov_total)
        st.write('Updates *Quarterly*')

    if gdp_components == 'Net Exports':
        st.subheader('Net Exports of Goods and Services')
        nex = to_df('NETEXC', start_date, end_date)
        exports = to_df('EXPGSC1', start_date, end_date)
        imports = to_df('IMPGSC1', start_date, end_date)
        netexports = pd.concat([nex, exports, imports], axis=1)

        st.line_chart(netexports)
        st.write('Updates *Quarterly*')

    st.header('Housing Market')
    st.subheader('New Home Sales')
    new_homes = to_df('NHSUSSPT', start_date, end_date)
    st.line_chart(new_homes)
    st.write('Updates *Monthly*')

    st.subheader('Existing Home Sales')
    exist_homes = to_df('EXHOSLUSM495S', start_date, end_date)
    st.line_chart(exist_homes)
    st.write('Updates *Monthly*')

    st.subheader('Median Months on Market for New Homes')
    months_on_market = to_df('MNMFS', start_date, end_date)
    st.line_chart(months_on_market)
    st.write('Updates *Monthly*')


    st.subheader('Federal Housing Financing Agency Price Index')
    fhfi = to_df('USSTHPI', start_date, end_date)
    st.line_chart(fhfi)
    st.write('Updates *Quarterly*')


    st.header('Manufacturing Sector')
    naics_ipmanu = to_df('IPMAN', start_date, end_date)
    st.line_chart(naics_ipmanu)
    st.write('Updates *Monthly*')


    metals = st.checkbox('Industrial Production: Manufacturing - Durable Goods - Primary Metal (NAICS=331)')
    compelec_prods = st.checkbox('Industrial Production: Manufacturing - Durable Goods - Computer and Electronic Products (NAICS=334)')
    vehicles = st.checkbox('Industrial Production: Manufacturing - Durable Goods - Motor Vehicles and Parts (NAICS=3361-3)')
    furniture = st.checkbox('Industrial Production: Manufacturing - Durable Goods - Furniture and Related Goods (NAICS=337)')
    apparel = st.checkbox('Industrial Production: Manufacturing - Non Durable Goods - Apparel and Leather Goods (NAICS=315,6)')

    metals_df = to_df('IPG331S', start_date, end_date)
    compelec_prods_df = to_df('IPG334S', start_date, end_date)
    vehicles_df = to_df('IPG3361T3S', start_date, end_date)
    furniture_df = to_df('IPG337S', start_date, end_date)
    apparel_df = to_df('IPG315A6S', start_date, end_date)


    manu_checks = [metals, compelec_prods, vehicles, furniture, apparel]
    manudf_list = [metals_df, compelec_prods_df, vehicles_df, furniture_df, apparel_df]
    manu_sectors_todisp = []

    #checks checkboxes
    for int in range(len(manu_checks)):
        if manu_checks[int]:
            manu_sectors_todisp.append(manudf_list[int])
    if len(manu_sectors_todisp) ==  0:
        st.write('No Boxes are checked')

    if len(manu_sectors_todisp) >  0:
        final_manudf = pd.concat(manu_sectors_todisp, axis=1)
        st.line_chart(final_manudf)
        st.write('Updates *Monthly*')

    st.header('US National Balance Sheet')
    st.subheader('Federal Debt: Total Public Debt')
    debt = to_df('GFDEBTN', start_date, end_date)
    st.line_chart(debt)
    st.write('Updates *Quarterly*')

    st.subheader('Debt/GDP Ratio')
    debt_to_gdp = to_df('GFDEGDQ188S', start_date, end_date)
    st.line_chart(debt_to_gdp)
    st.write('Updates *Quarterly*')


    st.subheader('Federal Surplus or Deficit')
    surp_or_def = to_df('MTSDS133FMS', start_date, end_date)
    st.line_chart(surp_or_def)
    st.write('Updates *Monthly*')


    st.subheader('Surplus or Deficit/GDP Ratio')
    surp_or_def_ratio = to_df('FYFSGDA188S', start_date, end_date)
    st.line_chart(surp_or_def_ratio)
    st.write('Updates *Monthly*')


    st.header('Credit Market')
    st.subheader('National Financial Conditions Index ')
    nfci = to_df('NFCI', start_date, end_date)
    st.line_chart(nfci)
    st.write('Updates *Weekly*')
if major_selection == 'Labor Market':
    st.header('Labor Market')

if major_selection == 'Price Level and Interest Rates':
    st.header('Price Level and Interest Rates')

# st.header('This is the App')
