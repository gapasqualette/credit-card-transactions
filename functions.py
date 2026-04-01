import pandas as pd
import streamlit as st

URL = 'https://huggingface.co/datasets/alenc123/credit-card-fraud/resolve/main/credit_card_transactions.parquet'

@st.cache_data()
def load_data():
    df = pd.read_parquet(URL)
    
    return get_df(df)

@st.cache_data()
def get_df(df):
    try:
        days_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        months_order = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        df['full_name'] = df['first'] + ' ' + df['last']
        df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
        df['dob'] = pd.to_datetime(df['dob'])
        df['date'] = df['trans_date_trans_time'].dt.date
        df['year'] = df['trans_date_trans_time'].dt.year
        df['month_year'] = df['trans_date_trans_time'].dt.to_period('M')
        df['time'] = df['trans_date_trans_time'].dt.time
        df['hour'] = df['trans_date_trans_time'].dt.hour
        df['day_week'] = df['trans_date_trans_time'].dt.day_name()
        df['day_week'] = pd.Categorical(df['day_week'], categories=days_order, ordered=True)

        df['month'] = df['trans_date_trans_time'].dt.month_name()
        df['month'] = pd.Categorical(df['month'], categories=months_order, ordered=True)

        df = df.drop_duplicates(subset='trans_num')
        df = df[df['amt'] > 0]
        df['merchant'] = df['merchant'].str.replace('fraud_', '').str.strip().str.title()
        df['category'] = df['category'].str.replace('_', ' ').str.strip().str.title()
        df['year_birth'] = df['dob'].dt.year
        df['decade_birth'] = (df['year_birth'] // 10) * 10
        df = df.rename(columns={'amt': 'amount', 'Unnamed: 0': 'trans_id', 'dob': 'date_birth'})
        df = df.drop(columns=['first', 'last', 'lat', 'long', 'merch_lat', 'merch_long', 'unix_time', 'trans_date_trans_time'])
        df['gender'] = df['gender'].astype('category')
        df['state'] = df['state'].astype('category')
        return df

    except Exception as e:
        raise Exception(f'No credit card transactions data found: {e}')

@st.cache_data
def get_filter_options(df):
    return {
        "category": sorted(df['category'].dropna().unique()),
        "gender": sorted(df['gender'].dropna().unique()),
        "state": sorted(df['state'].dropna().unique()),
    }
