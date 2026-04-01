import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

from functions import *

# show_columns()
df = load_data()
df_filter = df.copy()
st.header('🛒 Merchants Analysis')

st.subheader('KPIs', divider=True)
filters = get_filter_options(df_filter)

seasons_map = {
    'Winter': ['January', 'February', 'March'],
    'Spring': ['April', 'May', 'June'],
    'Summer': ['July', 'August', 'September'],
    'Autumn': ['October', 'November', 'December']
}

conditions = [df_filter['month'].isin(months) for months in seasons_map.values()]
choices = list(seasons_map.keys())

day_week = {
    'Week Days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'Weekend Days': ['Saturday', 'Sunday'],
}

conditions_days = [df_filter['day_week'].isin(days) for days in day_week.values()]
choices_day = list(day_week.keys())

df_filter['season'] = np.select(conditions, choices, default='Other')
df_filter['type_days'] = np.select(conditions_days, choices_day, default='Other')

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
    active_merchants = df_filter['merchant'].nunique()
    st.metric('Number of Merchants', value=active_merchants)

    df_most_sell_gender = df_filter.groupby(['merchant', 'gender'])['trans_id'].size().reset_index(name='count')
    most_sell_women = df_most_sell_gender[df_most_sell_gender['gender'] == 'F'].sort_values('count', ascending=False).iloc[0]
    most_sell_men = df_most_sell_gender[df_most_sell_gender['gender'] == 'M'].sort_values('count', ascending=False).iloc[0]

    if most_sell_women['count'] > 0:
        st.metric('Most Sell Women', value=most_sell_women['merchant'])
    else:
        st.metric('Most Sell Women', value='No sells')

    if most_sell_men['count'] > 0:
        st.metric('Most Sell Men', value=most_sell_men['merchant'])
    else:
        st.metric('Most Sell Men', value='No sells')

    total_amt = df_filter['amount'].sum()
    avg_ticket = round(total_amt / active_merchants, 2)
    st.metric('Average Ticket per Merchant (USD)', value=avg_ticket)

    total_trans = df_filter.shape[0]
    avg_trans = round(total_trans // active_merchants, 2)
    st.metric('Total Transactions per Merchant', value=avg_trans)

st.subheader('Plots', divider=True)

col_merch = st.columns(2)

with col_merch[0]:
    df_total_no_filter = (
        df.groupby('category', observed=False)['amount'].
        sum().
        reset_index(name='total_amount').
        sort_values('total_amount', ascending=False).
        head(10)
    )
    fig, ax = plt.subplots(figsize=(10,6), dpi=100)
    sns.barplot(x='total_amount', y='category', data=df_total_no_filter, ax=ax, linewidth=1.5, edgecolor='black',palette='deep')
    ax.set_title('Total Amount per Category (USD) - No Filter\n', fontweight='bold')
    ax.set_xlabel('Total Amount (USD)', fontweight='bold')
    ax.set_ylabel('Category', fontweight='bold')
    ax.set_xlim(left=df_total_no_filter['total_amount'].min() - 10000)

    with st.container(width="stretch", height="stretch", border=True):
        st.pyplot(fig)

    with st.expander('Insight - Top 10 Categories - Total Amount (USD)', icon=':material/search_insights:'):
        st.write(
            """
            Some categories dominate total revenue, indicating greater commercial relevance.\n
            This may reflect both higher demand and a higher average ticket price.
            """
        )

with col_merch[1]:
    df_total_filter = (
        df_filter.groupby('merchant', observed=False)['amount'].
        sum().
        reset_index(name='total_amount').
        sort_values('total_amount', ascending=False).
        head(10)
    )
    fig, ax = plt.subplots(figsize=(10,7), dpi=100)
    sns.barplot(x='total_amount', y='merchant', data=df_total_filter, ax=ax, linewidth=1.5, edgecolor='black', palette='deep')
    ax.set_title('Total Amount per Merchant (USD) - Filtered\n', fontweight='bold')
    ax.set_xlabel('Total Amount (USD)', fontweight='bold')
    ax.set_ylabel('Merchant', fontweight='bold')
    ax.set_xlim(left=df_total_filter['total_amount'].min() - 10000)
    with st.container(width="stretch", height="content", border=True):
        st.pyplot(fig, width='stretch')

    with st.expander('Insight - Top 10 Merchants per Amount (USD)', icon=':material/search_insights:'):
        st.write(
            """
            A few merchants concentrate a large portion of the financial volume, suggesting a scenario of revenue concentration.\n 
            This may indicate strategic partnerships or commercial dependence.
            """
        )

st.divider()

col_merch = st.columns(2)

with col_merch[0]:
    df_amt_days = (
        df_filter.groupby(['category', 'type_days'], observed=False)['amount'].
        sum().
        reset_index(name='total_amount').
        sort_values('total_amount', ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10,6), dpi=100)
    sns.barplot(data=df_amt_days, x='category', y='total_amount', ax=ax, linewidth=1.5, edgecolor='black', palette='deep', hue='type_days')
    ax.set_title('Amount per Category & Type of Days (Business | Weekend)\n ', fontweight='bold')
    ax.set_xlabel('Category', fontweight='bold')
    ax.set_ylabel('Amount (USD)', fontweight='bold')
    ax.set_ylim(bottom=df_amt_days['total_amount'].min()*0.8)
    ax.tick_params(axis='x', labelrotation=60)

    with st.container(width="stretch", height="stretch", border=True):
        st.pyplot(fig)

    with st.expander('Insight - Amount per Category & Type of Days (Business | Weekend)', icon=':material/search_insights:'):
        st.write(
            """
            Consumer behavior varies between weekdays and weekends, showing that some categories are more sensitive to the consumer's free time.
            """
        )

with col_merch[1]:
    df_per_month = (
        df_filter.groupby(['category', 'season'], observed=False)['trans_id'].
        size().
        reset_index(name='total_count')
    )

    fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
    sns.barplot(data=df_per_month, x='category', y='total_count', ax=ax, linewidth=1.5, edgecolor='black',
                palette='deep', hue='season')
    ax.set_title('Count Transactions per Season\n', fontweight='bold')
    ax.set_xlabel('Category', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.tick_params(axis='x', labelrotation=60)

    with st.container(width="stretch", height="stretch", border=True):
        st.pyplot(fig)

    with st.expander('Insight - Amount of Transactions by Category per Season', icon=':material/search_insights:'):
        st.write(
            """
            There is a seasonal influence on transaction volume, indicating that certain categories perform better during specific periods of the year.
            """
        )

st.divider()
cols_merch = st.columns(2)

with cols_merch[0]:
    top_merchants = (
        df_filter.groupby('merchant', observed=False)['amount']
        .sum()
        .nlargest(6)
        .index
    )

    df_merchant = df_filter[df_filter['merchant'].isin(top_merchants)]

    df_merchant_time = (
        df_merchant
        .groupby(['year', 'month', 'merchant'])['amount']
        .sum()
        .reset_index()
    )

    df_merchant_time['date'] = pd.to_datetime(
        df_merchant_time['year'].astype(str) + '-' + df_merchant_time['month'].astype(str),
        format='%Y-%B'
    )

    df_merchant_time = df_merchant_time.sort_values('date')

    df_merchant_time['rolling_mean'] = (
        df_merchant_time
        .groupby('merchant')['amount']
        .transform(lambda x: x.rolling(3, min_periods=1).mean())
    )

    fig, ax = plt.subplots(figsize=(7, 3))

    sns.lineplot(data=df_merchant_time, x='date', y='rolling_mean', hue='merchant', marker='o', ax=ax)

    ax.set_title('Transaction Evolution by Merchant (Trend)\n', fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')

    plt.xticks(rotation=45)

    with st.container(width="stretch", height="stretch", border=True):
        st.pyplot(fig)

    with st.expander('Insight - Transaction Evolution by Merchant (Trend)', icon=':material/search_insights:'):
        st.write(
            """
            The evolution shows clear differences in growth between merchants, highlighting which ones are gaining relevance over time.
            """
        )

with cols_merch[1]:
    df_merchant_time['cumulative_amount'] = (
        df_merchant_time.groupby('merchant', observed=False)['amount'].
        cumsum()
    )

    fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
    sns.lineplot(
        data=df_merchant_time,
        x='date',
        y='cumulative_amount',
        hue='merchant',
        marker='o',
        ax=ax
    )

    ax.set_title('Cumulative Amount per Month\n', fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Amount (USD)', fontweight='bold')
    ax.tick_params(axis='x', labelrotation=60)
    with st.container(width="stretch", height="content", border=True):
        st.pyplot(fig)

    with st.expander('Insight - Cumulative Amount per Month by Merchant', icon=':material/search_insights:'):
        st.write(
            """
            Cumulative growth highlights which merchants have consistent performance over time, helping to identify the most solid players.
            """
        )

st.divider()

df_filter_pivot = df_filter.copy()

df_filter_pivot['date'] = pd.to_datetime(
        df_filter_pivot['year'].astype(str) + '-' + df_filter_pivot['month'].astype(str),
        format='%Y-%B'
    ).dt.strftime('%Y-%B')

df_filter_pivot = (
    df_filter_pivot.groupby(['category', 'date'], observed=False)['trans_id'].
    count().
    reset_index(name='amount_date_cat').
    pivot(index='date', columns='category', values='amount_date_cat')
)

df_filter_pivot = df_filter_pivot.fillna(0).sort_index()

fig, ax = plt.subplots(figsize=(10,6), dpi=100)
sns.heatmap(df_filter_pivot, annot=True, fmt='.0f', linewidths=.75, ax=ax, cmap='YlGnBu')
ax.set_title("Transactions Tendency per Category and Date\n", fontweight='bold', fontsize=12)
ax.set_xlabel('Category', fontsize=8)
ax.set_ylabel('Date', fontsize=8)

col_plot = st.columns([1,3,1])
with col_plot[1]:
    st.pyplot(fig, width='stretch')

    with st.expander('Insight - Transactions Tendency per Category and Date', icon=':material/search_insights:'):
        st.write(
            """
            The heatmap shows clear temporal patterns of consumption by category, allowing you to identify seasonal peaks and changes in behavior over time.
            """
        )