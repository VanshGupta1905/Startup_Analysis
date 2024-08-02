import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('startup_cleaned.csv')
st.set_page_config(layout='wide',page_title='Startup Analysis')
st.sidebar.title("Startup Funding Analysis")
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year
def load_overall_analysis():
    st.title('Overall Analysis')
    total=df['amount'].sum()
    max_funding=df.groupby('startup')['amount'].sum().sort_values(ascending=False).values[0]
    avg=df.groupby('startup')['amount'].sum().mean()
    col1,col2,col3,col4=st.columns(4)
    total_funded_startups=df['startup'].nunique()
    with col1:
        st.metric( 'Total Funding ',str(total)+' Cr')
    with col2:
        st.metric('Max Funding ',str(max_funding)+' Cr')
    with col3:
        st.metric('Average',str(round(avg))+ ' Cr')
    with col4:
        st.metric('No. of Total Funded Startups ',str(total_funded_startups))
    st.header('MoM graph')
    select_option=st.selectbox('Selected Type',['Total','Count'])
    if select_option=='Total':
        temp = df.groupby(['month', 'year'])['amount'].sum().reset_index()
        temp['x_axis'] = temp['month'].astype('str') + '-' + temp['year'].astype('str')
    else:
        temp = df.groupby(['month', 'year'])['amount'].count().reset_index()
        temp['x_axis'] = temp['month'].astype('str') + '-' + temp['year'].astype('str')

    fig3,ax3=plt.subplots()
    ax3.plot(temp['x_axis'],temp['amount'])
    st.pyplot(fig3)

def load_investor_details(investor):
    st.title(investor)
    investor_records=df[df['investors'].str.contains(investor)]
    st.subheader('Most Recent Investment')
    st.dataframe(investor_records.head())
    col1,col2=st.columns(2)

    with col1:
        biggest_investment=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False)[:5]
        st.subheader('Biggest Investments')
        fig,ax=plt.subplots()

        ax.bar(biggest_investment.index,biggest_investment.values)
        st.pyplot(fig)
    with col2:
        st.subheader('Sectors Invested In')
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        fig1,ax1=plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
    col3,col4=st.columns(2)
    with col3:
        st.subheader('Cities')
        vertical_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)
    with col4:
        st.subheader('Round')
        vertical_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)


option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investors'])
if option=='Overall Analysis':
    load_overall_analysis()

elif option=='Startup':
    st.title('Startup')
    st.sidebar.selectbox('Select Investor', df['startup'].unique().tolist())
    st.sidebar.button('Find Startup Details')

else:

    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn=st.sidebar.button('Find Investor Details')
    if btn:
        load_investor_details(selected_investor)

