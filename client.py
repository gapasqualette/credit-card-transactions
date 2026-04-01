import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns

from functions import *

# show_columns()
df = load_data()
df_filter = df.copy()
st.header('👤Client Analysis')

st.subheader('KPIs', divider=True)
filters = get_filter_options(df_filter)

with st.sidebar:
    st.header('Filters', divider=True)
    cat = st.multiselect(label='Category', options=filters['category'])
    if cat :
        df_filter = df_filter[df_filter['category'].isin(cat)]

    gender = st.selectbox("Gender", options=["Select All"] + filters['gender'], index=0)
    if gender != 'Select All':
        df_filter = df_filter[df_filter['gender'] == gender]

    state = st.selectbox('State', options=['Select All'] + filters['state'], index=0)
    if state != 'Select All':
        df_filter = df_filter[df_filter['state'] == state]

    min_date = df_filter['date'].min()
    max_date = df_filter['date'].max()

    date_range = st.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    if len(date_range) == 2:
        df_filter = df_filter[(df_filter['date'] >= date_range[0]) & (df_filter['date'] <= date_range[1])]

with st.container(width="stretch", height="content", horizontal=True, horizontal_alignment='center'):
    st.metric('Total Spending', value=f'{round(df_filter['amount'].sum(), 2):,.2f}')
    st.metric(label='Number of Clients', value=df_filter['full_name'].nunique())
    st.metric(label='Total Transactions', value=df_filter['trans_num'].shape[0])
    st.metric(label='Average Ticket', value=round(df_filter['amount'].sum() / df_filter['full_name'].nunique(), 2))

    df_client_segment = df_filter.groupby(['full_name', 'gender'], observed=False)['amount'].sum().reset_index(name='total_amount')
    df_client_segment['profile'] = pd.cut(
        df_client_segment['total_amount'],
        bins=[0, 125000, 200000, 280000, np.inf],
        labels=['Low', 'Medium', 'High', 'VIP']
    )

    vip_pct = round(100 * (df_client_segment[df_client_segment['profile'] == 'VIP'].shape[0] / df_client_segment.shape[0]), 2)
    st.metric('Percentage of VIPs', f'{vip_pct}%')

with st.container(width="stretch", height="content", horizontal=True, horizontal_alignment='center'):
    df_gender_count = df.groupby('gender', observed=False)['cc_num'].nunique()
    num_women = df_gender_count.iloc[0]
    num_men = df_gender_count.iloc[-1]

    st.metric('Gender Count', value=f'F: {num_women:,} | M: {num_men:,} ')

    df_spender = df_filter.groupby('full_name')['amount'].sum().reset_index(name='total_amount').sort_values('total_amount', ascending=False)
    biggest_spender = df_spender.iloc[0, 0]
    smallest_spender = df_spender.iloc[-1, 0]
    st.metric(label='Biggest Spender', value=biggest_spender)
    st.metric(label='Smallest Spender', value=smallest_spender)

    df_cat = df_filter.groupby('category')['amount'].sum().reset_index(name='total_amt_cat').sort_values('total_amt_cat', ascending=False)
    biggest_cat = df_cat.iloc[0, 0]
    smallest_cat = df_cat.iloc[-1, 0]
    st.metric(label='Biggest Category', value=biggest_cat)
    st.metric(label='Smallest Category', value=smallest_cat)

st.subheader('Plot - Overall Behavior by Category (No Filter)', divider=True)
cols_nofilter = st.columns(2)

with cols_nofilter[0]:
    df_cat = df.groupby('category', observed=False)['amount'].sum().reset_index(name='total_amt_cat').sort_values('total_amt_cat', ascending=False).reset_index()
    df_cat['percentage'] = np.round(df_cat['total_amt_cat'] / df_cat['total_amt_cat'].sum() * 100, 0)

    fig, ax = plt.subplots(figsize=(7, 3))
    sns.barplot(data=df_cat, x='category', y='total_amt_cat', ax=ax, edgecolor='black', linewidth=1.5, palette='pastel')
    ax.set_title("Total amount per Category\n", fontdict={'fontweight': 'bold'})
    ax.set_xlabel('Category')
    ax.set_ylabel('Amount (USD)', color='blue')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax2 = ax.twinx()
    sns.lineplot(data=df_cat, x='category', y='percentage', color='red', ax=ax2)
    ax2.set_ylabel('Percentage', color='red')
    with st.container(height="stretch", border=True, width='stretch'):
        st.pyplot(fig)

    with st.expander('Insight - Total Amount per Category', icon=':material/search_insights:'):
        st.write(
            """
            Some categories account for a large portion of the financial volume, like the Grocery Pos industry having nearly 16'%' of total amount. 
            This can represent an opportunity for strategic focus, but also a risk if there is a decline in these categories.
            """
        )

with cols_nofilter[1]:
    df_month_sex = (
        df[df['year'] == 2019].
        groupby(['month', 'gender'], observed=False).
        size().
        reset_index(name='count_sex_month').
        sort_values('count_sex_month', ascending=False).
        reset_index()
    )
    fig, ax = plt.subplots(figsize=(7, 3))
    sns.barplot(data=df_month_sex, x='month', y='count_sex_month', hue='gender', ax=ax, edgecolor='black', linewidth=1.5, palette='deep')
    ax.set_title("Count per Month & Sex (Year 2019)\n", fontdict={'fontweight': 'bold'})
    ax.set_xlabel('Month')
    ax.set_ylabel('Transactions Count', color='blue')
    plt.xticks(rotation=45, ha='center')
    with st.container(border=True, height="stretch", width='stretch'):
        st.pyplot(fig, width='content')

    with st.expander('Insight - Transactions Count per Sex', icon=':material/search_insights:'):
        st.write(
            """
            Considering the scenario of equal numbers between men and women, there is a clear variation in transaction volume throughout the months, with consistent differences between genders. 
            This suggests that consumer behavior may be linked to seasonality and demographic profile.
            """
        )

st.subheader('Filtered Analysis', divider=True)

cols_filter = st.columns(2)
with cols_filter[0]:
    df_month_year = (
        df_filter.groupby(['month_year'], observed=False)['amount'].
        sum().
        reset_index(name='total_amt_month').
        reset_index()
    )

    fig, ax = plt.subplots(figsize=(7, 3))
    sns.barplot(data=df_month_year, x='month_year', y='total_amt_month', ax=ax, edgecolor='black', linewidth=1.5)
    ax.set_title("Total amount per Month\n", fontdict={'fontweight': 'bold'})
    ax.set_xlabel('Month / Year')
    ax.set_ylabel('Amount (USD)', color='blue')
    plt.xticks(rotation=45, ha='center')
    with st.container(height="stretch", width='stretch', border=True):
        st.pyplot(fig)
    with st.expander("Insight - Total amount per Month", icon=":material/search_insights:"):
        st.write("""
        Given the dates in the dataframe, the disparity in total spending in December due to Christmas is noticeable.\n
        It is interesting to see in this dataframe that August has more spending than May, 
        meaning it's possible to conclude that there was more spending on Father's Day than on Mother's Day.\n
        Another interesting piece of data is the low spending in January and February, 
        which would normally be months reserved for family trips, given the school holidays.
        """)

with cols_filter[1]:
    df_hour_amt = (
        df_filter.groupby(['hour', 'gender'], observed=False).
        agg(
            total_amt = ('trans_num', 'nunique')
        ).
        sort_values(['hour', 'gender'], ascending=[True, True]).
        reset_index()
        )

    # gráfico pizza
    fig, ax = plt.subplots(figsize=(7, 3.8))
    sns.lineplot(data=df_hour_amt, x='hour', y='total_amt', hue='gender', linewidth=1.1)
    ax.set_title("Top 10 Total Amount per Client\n", fontdict={'fontweight': 'bold'})
    ax.set_xlabel('Hour of the day (0h - 23h)')
    ax.set_ylabel('Amount (USD)', color='blue')
    ax.tick_params(rotation=45, axis='x')
    with st.container(height="content", width='stretch', border=True):
        st.pyplot(fig, width='stretch')
    with st.expander("Insight - Number of Transactions per Hour", icon=":material/search_insights:"):
        males_hour_0 = df_hour_amt.iloc[1,-1]
        females_hour_0 = df_hour_amt.iloc[0, -1]

        pct_hour_0 = round(100 * (females_hour_0/males_hour_0 - 1), 2)
        females_hour_20 = df_hour_amt.iloc[40, -1]
        males_hour_20 = df_hour_amt.iloc[41, -1]

        pct_hour_20 = round(100 * (females_hour_20/males_hour_20 - 1), 2)

        st.write(
            f"""
            As we can see, at every hour of the day, women buy more times than men.\n
            But, between hour 0 and 11, the proportion women/men is way smaller than hours 12 and 23.\n
            For example, at hour 0: Women buy **{pct_hour_0:.2f}%** more than men.\n
            But at hour 20: **{pct_hour_20:.2f}%** more. 
            """
        )

st.divider()

cols_filter = st.columns(2)
with cols_filter[0]:
    df_decade = df_filter.groupby(['decade_birth', 'gender'], observed=False)['trans_num'].count().reset_index(name='count_decade').sort_values(['decade_birth', 'gender'], ascending=[True, False])

    fig, ax = plt.subplots(figsize=(7, 3))
    sns.lineplot(data=df_decade, x='decade_birth', y='count_decade', linewidth=1.5, hue='gender', palette='deep')
    ax.set_title("Number of Transactions per Decade\n", fontdict={'fontweight': 'bold'})
    ax.set_xlabel('Decade')
    ax.set_ylabel('Number of Transactions')
    with st.container(height="stretch", width='stretch', border=True):
        st.pyplot(fig, width='stretch')

    with st.expander("Insight - Transaction Distribution per Decade", icon=":material/search_insights:"):
        st.write(
            """
            According to the data, alongside the filters, the youngest and the elderly are not willing to buying as much as the adults.\n
            People born in the 70s and 80s are the ones who buys the most, probably because they are in their financial peak with their jobs.\n
            In a general aspect, men born in the 1940s and 2000s, buy more than women.\n
            But when it comes to the Travel category, adult and young men are very willing to spend their money more than women. 
            """
        )

with cols_filter[1]:
    df_client_segment2 = df_client_segment.copy()
    df_client_segment2 = df_client_segment2.groupby(['profile', 'gender'], observed=False).size().reset_index(name='count')

    fig, ax = plt.subplots(figsize=(7, 3))
    sns.barplot(data=df_client_segment2, x='profile', y='count', edgecolor='black', linewidth=1.5, hue='gender')
    ax.set_title("Client Profile Count\n", fontdict={'fontweight': 'bold'})
    ax.set_xlabel('Profile')
    ax.set_ylabel('Count')
    with st.container(height="stretch", width='stretch', border=True):
        st.pyplot(fig, width='stretch')

    with st.expander("Insight - Client Segment", icon=":material/search_insights:"):
        st.code("Low: < 125000 | Medium: 125000 < x > 200000 | High: 200000 < x > 280000 | VIP: > 280000", language="python", wrap_lines=True)
        st.write(
            """
            In this sample, there are more low profile men than women, contradicting the rest of profiles. 
            """
        )

st.divider()

df_filter_pivot = (
    df_filter.groupby(['category', 'hour'], observed=False)['trans_id'].
    count().
    reset_index(name='amount_hour_cat').
    pivot(index='hour', columns='category', values='amount_hour_cat')
)

df_filter_pivot = df_filter_pivot.fillna(0).sort_index()
# df_filter_pivot = df_filter_pivot.div(100)

fig, ax = plt.subplots(figsize=(10,6), dpi=100)
sns.heatmap(df_filter_pivot, annot=True, fmt='.0f', linewidths=.75, ax=ax, cmap='YlGnBu')
ax.set_title("Transactions Count per Category and Hour\n", fontweight='bold', fontsize=12)
ax.set_xlabel('Category', fontsize=8)
ax.set_ylabel('Hour', fontsize=8)

col_plot = st.columns([1,3,1])
with col_plot[1]:
    st.pyplot(fig, width='stretch')

    with st.expander('Insight - Heatmap: Transaction Count per Category and Hour', icon=":material/search_insights:"):
        st.write(
            f"""
            The heatmap illustrates the distribution of transaction volume across different hours of the day and spending categories, 
            revealing clear behavioral patterns in customer activity.\n
    
            Overall, transaction activity tends to concentrate during typical daytime and evening hours, particularly between late morning and early night. 
            This pattern suggests that most users engage in financial activity during standard daily routines, such as working hours and leisure periods.\n
    
            A noticeable increase in activity is often observed during the evening (around 18:00–22:00), which likely reflects consumption related to dining, entertainment, and other discretionary spending. 
            In contrast, early morning hours (00:00–06:00) generally show lower transaction volumes, as expected under normal behavior.\n
    
            However, any significant spikes in transaction volume during late-night or early-morning hours may indicate atypical behavior. 
            If such patterns are concentrated in specific categories, they could suggest unusual usage or potential fraudulent activity, 
            especially when inconsistent with typical customer habits.
            """
        )