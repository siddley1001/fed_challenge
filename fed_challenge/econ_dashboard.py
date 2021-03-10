import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import os
from fredapi import Fred

KEY = 'dde5ad634e39b6e288c9a2ebec181e58'
fred = Fred(api_key= KEY)

econ_dictionary =   {
                    #GDP
                    'GDPC1': ['Real GDP $B']
                    #Labor Market
                    }

def to_df(series_name, start_date, end_date):
    series = fred.get_series(series_name, start_date, end_date)
    df = pd.DataFrame(series, column_names = econ_dictionary[series])


major_selection = st.sidebar.selectbox(
    'Explore Indicators for:',
    ('Overall Economic Activity', 'Labor Market', 'Price Level and Interest Rates')
)
start_date = st.sidebar.date_input('START Date', )

if major_selection == 'Overall Economic Activity':
    st.header('Overall Economic Activity')
    gdp = to_df('GDPC1')

if major_selection == 'Labor Market':
    st.header('Labor Market')

if major_selection = 'Price Level and Interest Rates':
    st.header('Price Level and Interest Rates')


st.header('This is the App')

