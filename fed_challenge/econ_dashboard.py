import os

import pandas as pd
import streamlit as st
from fredapi import Fred

os.chdir('/Users/vanamsid/quick_py/fed_challenge')

KEY = 'dde5ad634e39b6e288c9a2ebec181e58'
fred = Fred(api_key=KEY)

econ_dictionary = {
    # GDP
    'GDPC1': ['Real GDP $B'],
    'PCECC96':['TOTAL $B'],'DGDSRX1Q020SBEA':['Goods $B'],'PCESVC96':['Services $B'],
    'GPDIC1': ['TOTAL $B'], 'PNFIC1': ['Nonresidential $B'], 'PRFIC1': ['Residential $B'], 'CBIC1': ['Change in Private Inventory'],
    'GCEC1': ['TOTAL $B'], 'FGCEC1': ['Federal $B'], 'SLCEC1': ['State/Local $B'],
    'NETEXC': ['NET Exports $B'], 'EXPGSC1': ['Exports $B'], 'IMPGSC1': ['Imports $B'],
    ##Housing Market
    'NHSUSSPT': ['Total New Houses Sold (1,000s of Units)'],'EXHOSLUSM495S': ['Existing Houses Sold (1,000s of Units)'], 'MNMFS': ['Months on Maarket'], 'USSTHPI': ['House Price Index'],
    ##Manufacturing Market

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

    st.subheader('Gross Domestic Product GDP')
    gdp = to_df('GDPC1', start_date, end_date)
    st.line_chart(gdp)

    gdp_age = st.checkbox('Age')
    gdp_race = st.checkbox('Race')

    if gdp_age:
        pass
    if gdp_race:
        pass
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

    if gdp_components == 'Investment':
        st.subheader('Gross Private Domestic Investment')
        st.write("Where the majority of Investments are *Nonresidential*")

        i = to_df('GPDIC1', start_date, end_date)
        i_res = to_df('PRFIC1', start_date, end_date)
        i_nonres = to_df('PNFIC1', start_date, end_date)
        i_inventory = to_df('CBIC1', start_date, end_date)
        i_total = pd.concat([i, i_res, i_nonres], axis=1)
        st.write('Nonresidential and Residential Investment is considered **Fixed Investment**')

        st.line_chart(i_total)

        inv_change = st.checkbox('Change in Real Private Inventory')
        if inv_change:
            st.line_chart(i_inventory)

    if gdp_components == 'Government Expenditure':
        st.subheader('Government Consumption Expenditures and Investment')
        gov_exandinv = to_df('GCEC1', start_date, end_date)
        gov_fed = to_df('FGCEC1', start_date, end_date)
        gov_statelocal = to_df('SLCEC1', start_date, end_date)
        gov_total = pd.concat([gov_exandinv, gov_fed, gov_statelocal], axis=1)

        st.line_chart(gov_total)

    if gdp_components == 'Net Exports':
        st.subheader('Net Exports of Goods and Services')
        nex = to_df('NETEXC', start_date, end_date)
        exports = to_df('EXPGSC1', start_date, end_date)
        imports = to_df('IMPGSC1', start_date, end_date)
        netexports = pd.concat([nex, exports, imports], axis=1)

        st.line_chart(netexports)

    st.header('Housing Market')
    st.subheader('Home Sales')
    st.write('New and Existing Home Sales')
    new_homes = to_df('NHSUSSPT', start_date, end_date)
    exist_homes = to_df('EXHOSLUSM495S', start_date, end_date)
    home_sales = pd.concat([new_homes, exist_homes], axis=1)

    st.line_chart(home_sales)

    st.subheader('Median Months on Market for New Homes')
    months_on_market = to_df('MNMFS', start_date, end_date)
    st.line_chart(months_on_market)

    st.subheader('Federal Housing Financing Agency Price Index')
    fhfi = to_df('USSTHPI', start_date, end_date)
    st.line_chart(fhfi)

    st.header('Manufacturing Sector')


    st.header('US National Balance Sheet')

    st.header('Credit Market')
if major_selection == 'Labor Market':
    st.header('Labor Market')

if major_selection == 'Price Level and Interest Rates':
    st.header('Price Level and Interest Rates')

# st.header('This is the App')
