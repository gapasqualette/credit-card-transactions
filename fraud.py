import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import seaborn as sns
import numpy as np

from functions import *

df = load_data()
df_filter = df.copy()
st.header('🚦 Fraud Analysis')

st.subheader('KPIs - No Filter Analysis', divider=True)
filters = get_filter_options(df_filter)

with st.container(horizontal=True):
    total_frauds = df_filter[df_filter['is_fraud'] == 1].shape[0]
    st.metric('Total Frauds', value=total_frauds)

    pct_fraud = round(total_frauds*100/df_filter.shape[0], 2)
    st.metric('Percentage of Frauds', value=f'{pct_fraud}%')

    amount_fraud = df_filter[df_filter['is_fraud'] == 1]['amount'].sum()
    st.metric('Total Amount Stolen in Frauds (USD)', value=f'{amount_fraud:,.2f}')

    avg_ticket_fraud = round(amount_fraud / total_frauds,2)
    total_amt_no_frauds = df_filter[df_filter['is_fraud'] == 0]['amount'].sum()
    avg_ticket_no_fraud = round( total_amt_no_frauds / (df_filter.shape[0] - total_frauds),2)
    st.metric('Average Ticket Fraud x Non-Fraud (USD)', value=f'{avg_ticket_fraud} || {avg_ticket_no_fraud}')

st.subheader('Plots - Frauds', divider=True)

cols_fraud = st.columns(2)

with cols_fraud[0]:
    colors = ['mediumturquoise', 'gold']
    df_cnt_fraud = df_filter.groupby(['is_fraud'], observed=False).size().reset_index(name='count')
    fig = px.pie(
        df_cnt_fraud, 
        labels=['No Fraud', 'Fraud'], 
        values='count', 
        hole=0.3, 
        title='Fraud x Non Fraud Count',
        names=['Non Fraud', 'Fraud'],
    )
    fig.update_traces(textfont_size=20, hoverinfo='label+value', textinfo='value', marker=dict(colors=colors, line=dict(color='black', width=1)))

    with st.container(height='stretch', width='stretch', border=True):
        st.plotly_chart(fig)

    with st.expander('Insight - Fraudulent x Non Fraudulent Transactions Count', icon=':material/search_insights:'):
        st.write(
            """
            The proportion of fraud is significantly lower than in normal transactions, which is expected.\n
            However, even a small percentage can represent a high financial impact, reinforcing the importance of continuous monitoring.
            """
        )
with cols_fraud[1]:
    df_cat_fraud = (
        df_filter[df_filter['is_fraud'] == 1].
        groupby('category', observed=False).
        size().
        reset_index(name='count').
        sort_values('count', ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(df_cat_fraud, x='category', y='count', ax=ax, linewidth = 1.5, edgecolor='black', palette='pastel')
    ax.set_title('Number of Frauds per Category\n', fontweight='bold')
    ax.set_xlabel('Category')
    ax.set_ylabel('Number of Frauds')
    ax.tick_params(axis='x', labelrotation=30)
    
    with st.container(height='content', width='stretch', border=True):
        st.pyplot(fig)
    with st.expander('Insight - Fraud Count per Category', icon=':material/search_insights:'):
        st.write(
            """
            Some categories concentrate more fraud than others, indicating potential specific vulnerabilities.\n
            This can help guide stricter anti-fraud rules in these segments.
            """
        )

st.divider()
cols_fraud = st.columns(2)

with cols_fraud[0]:
    df_fraud_per_month = df_filter[df_filter['is_fraud'] == 1].groupby(['year', 'month'], observed=False).size().reset_index(name='count')
    df_fraud_per_month['date'] = pd.to_datetime(
        df_fraud_per_month['year'].astype(str) + '-' + df_fraud_per_month['month'].astype(str),
        format='%Y-%B'
    )
    df_fraud_per_month = df_fraud_per_month[df_fraud_per_month['count'] > 0]

    fig, ax = plt.subplots(figsize=(10,6))
    sns.lineplot(df_fraud_per_month, x='date', y='count', ax=ax, linewidth = 3, marker='o')
    ax.set_title('Number of Frauds per Month\n', fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Frauds')
    ax.tick_params(axis='x', labelrotation=60)
    with st.container(border=True, height='stretch', width='stretch'):
        st.pyplot(fig)

    with st.expander('Insight - Number of Fraudulent Transactions per Month', icon=':material/search_insights:'):
        st.write(
            """
            Monthly variations in fraud can indicate periods of higher risk exposure, 
            possibly linked to seasonality, higher transaction volume, or specific events.\n
            The clear example of this is Christmas holiday, when customers tend to spend buy and spend a lot in the Internet, 
            therefore the risk of being wronged is higher than usual.
            """
        )

with cols_fraud[1]:
    df_fraud_gender = (
        df_filter.
        groupby(['category', 'gender', 'is_fraud'], observed=False).
        size().
        reset_index(name='count').
        sort_values(['category', 'gender'], ascending=[False, True])
    )

    df_fraud_gender['percentage'] = np.round(
        100 * df_fraud_gender['count'] / df_fraud_gender.groupby(['category', 'gender'], observed=False)['count'].transform('sum'), 2)

    df_fraud_gender = df_fraud_gender[df_fraud_gender['is_fraud'] == 1]

    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(df_fraud_gender, x='category', y='percentage', hue='gender', ax=ax, linewidth = 1.5, edgecolor='black', palette='pastel')
    ax.set_title('Fraud Rate per Gender and Category\n', fontweight='bold')
    ax.set_xlabel('Percentage of Frauds')
    ax.set_ylabel('Number of Frauds')
    ax.tick_params(axis='x', labelrotation=60)
    with st.container(height='content', width='stretch', border=True):
        st.pyplot(fig)

    with st.expander('Insight - Fraudulent Transactions Rate per Gender and Category', icon=':material/search_insights:'):
        st.write(
            """
            The fraud rate varies not only by category, but also between genders, 
            suggesting distinct behavioral patterns that can be exploited to improve detection models.
            """
        )

st.divider()
cols_fraud = st.columns([1,3,1])
with cols_fraud[1]:
    df_hist_amt = df_filter[df_filter['is_fraud'] == 1].copy()
    df_hist_amt['amount_range'] = (df_hist_amt['amount'] // 100) * 100

    bins = [0, 100, 250, 500, 1000, 2500, np.inf]
    df_hist_amt['amount_range'] = pd.cut(
        df_hist_amt['amount'],
        bins=bins
    )

    df_hist_amt = df_hist_amt.groupby('amount_range', observed=False).size().reset_index(name='count')

    fig, ax = plt.subplots(figsize=(10,6))
    p = ax.bar(df_hist_amt['amount_range'].astype(str), df_hist_amt['count'])
    ax.set_title('Fraud Count per Amount Range\n', fontweight='bold', fontsize=14)
    ax.set_xlabel('Amount Range')
    ax.set_ylabel('Number of Frauds')
    ax.bar_label(p, fontsize=10)
    with st.container(height='content', width='stretch'):
        st.pyplot(fig)

    with st.expander('Insight - Fraudulent Transactions Count per Amount Range', icon=':material/search_insights:'):
        st.write(
            """
            The concentration of fraud in certain value ranges may indicate an operational pattern among fraudsters, who tend to operate on strategic values ​​to avoid detection.\n
            In this case, most fraud occurs in transactions of values ​​considered high, but not extremely high.
            """
        )