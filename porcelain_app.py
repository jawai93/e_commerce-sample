import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
import matplotlib.pyplot as plt
import base64
from PIL import Image

LOGO_IMAGE = "logo.png"
st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:2.5em !important;
        padding-top: 75px !important;
    }
    .logo-img {
        float:right;
    }
    .graph-img {

    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text"> Porcelain's Sales Report </p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("## YEAR 2018, 2019 and 2020")

st.markdown("# Introduction")
st.markdown("In this report, we are going to analyze Porcelain's e-commerce and in-store dataset that contains transactions occuring over 3 years - 2018, 2019 and 2020.")
st.markdown("The goal of this analysis is to identify key trends and patterns \
to gain insights on our customer's loyalty to the brand. We will then use these insights to come up with an action plan to acquire suitable customers and earning their loyalty.")

st.markdown("# Data Preparation")
st.markdown("Before I performed any data analysis on the invoice data, I used Microsoft Excel and Python to clean and transform the data into a format where I can easily load into my\
	analytics tool. Here are some key points on the data of this process:")
st.markdown("### Invoice Data")
st.markdown("""
	1. Merged in-store and E-commerce data into 1 sheet, added column 'Source' to identify source of transaction.
	2. Added 2 more columns to identity if the transactions were made on the weekday or weekend. 
	3. Removed any duplicate records from the invoice data.
	4. Removed transactions made outside the years of 2018,2019 and 2020.
	5. Reformatted dates to be uniform.""")

st.markdown("### Customer Info Data")
st.markdown("""
	1. There is missing data in the dataset. Instead of removing them, I categorized them as a different group.
	For example, those without referralSource are categorized as 'non-referral'.
	2. Reformatted dates to be uniform.
	""")

st.sidebar.title("Customer Analysis")

DATA_URL = ("C:/Users/JasonWong/Desktop/Porcelain/final_merge.csv")

@st.cache(persist=True)
def load_data():
	data = pd.read_csv(DATA_URL)
	return data

data = load_data()


st.sidebar.subheader("Total Sales($), Orders(#) and Customers(#) by year")
sales_data=data[['year', 'item_cost', 'unique_identifier']].groupby(['year'], as_index=False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
                                 orders=pd.NamedAgg(column='unique_identifier', aggfunc='count'),
                                 customers=pd.NamedAgg(column='unique_identifier', aggfunc='nunique'),
                                )

if not st.sidebar.checkbox("Hide", True): 
	st.markdown("### Total Sales($), Orders(#) and Customers(#) by year")
	fig = px.bar(sales_data, x="year", y="sales", title="Sales by Year")
	fig.update_xaxes(type='category')
	st.plotly_chart(fig)

	fig = px.bar(sales_data, x="year", y="orders", title="Number of Orders by Year")
	fig.update_xaxes(type='category')
	st.plotly_chart(fig)

	fig = px.bar(sales_data, x="year", y="customers", title="Number of Unique Customers by Year")
	fig.update_xaxes(type='category')
	st.plotly_chart(fig)
# fig = px.bar(sales_data, x='Sentiment', y='Tweets')


st.markdown("#### 1d. Observation")
st.markdown("""
	1. Sales increased from 2018 to 2019 but declined in 2020
	2. Number of orders increased from 2018 to 2019 but declined in 2020
	3. However,  number of unique customers have **increased** steadily over the 3 years
	""")


data_2018=data[data.year==2018]
data_2019=data[data.year==2019]
data_2020=data[data.year==2020]
data_source = data[['source','year_month','item_cost','unique_identifier']].groupby(['source', 'year_month'], as_index=False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
                                 orders=pd.NamedAgg(column='unique_identifier', aggfunc='count'),
                                 customers=pd.NamedAgg(column='unique_identifier', aggfunc='nunique'),
                                )

st.subheader("2. Annual Sales by Month")

st.markdown("**2a. 2018 Sales by Month**")
best_month2018=data_2018[['source','year_month','item_cost','unique_identifier']].groupby(['year_month'], as_index=False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
                                 orders=pd.NamedAgg(column='unique_identifier', aggfunc='count'),
                                 customers=pd.NamedAgg(column='unique_identifier', aggfunc='nunique'),
                                )
fig_source_18 = px.line(best_month2018, x='year_month', y='sales')

st.plotly_chart(fig_source_18)

st.markdown("**2b. 2019 Sales by Month**")
best_month2019=data_2019[['source','year_month','item_cost','unique_identifier']].groupby(['year_month'], as_index=False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
                                 orders=pd.NamedAgg(column='unique_identifier', aggfunc='count'),
                                 customers=pd.NamedAgg(column='unique_identifier', aggfunc='nunique'),
                                )

fig_source_19 = px.line(best_month2019, x='year_month', y='sales')
st.plotly_chart(fig_source_19)

st.markdown("**2c. 2020 Sales by Month**")
best_month2020=data_2020[['source','year_month','item_cost','unique_identifier']].groupby(['year_month'], as_index=False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
                                 orders=pd.NamedAgg(column='unique_identifier', aggfunc='count'),
                                 customers=pd.NamedAgg(column='unique_identifier', aggfunc='nunique'),
                                )

fig_source_20 = px.line(best_month2020, x='year_month', y='sales')
st.plotly_chart(fig_source_20)


st.markdown("#### 2d. Observation")
st.markdown("The best performing months in terms of total sales for the years 2018, 2019 and 2020 are February 2018, August 2019 and October 2020.")
st.markdown("Now, let's breakdown the sales based on the source of sales. Are these sales made online or in-store? Please see Section 3, You can toggle the sources on the sidebar to view the table and graphs.")

st.sidebar.subheader("3. Sales breakdown by source")
st.subheader("3. Sales breakdown by source")
sources = data_source['source'].unique()
choice = st.sidebar.radio('Select Source', sources)
if len(choice) > 0:
	st.markdown("**3a. Table - Monthly sales 2018, 2019 & 2020 by Source**")
	df_1 = data_source[data_source['source']==choice]
	st.write(df_1)
	fig_choice_sales = px.line(df_1, x="year_month", y="sales")
	fig_choice_customer = px.line(df_1, x="year_month", y="customers")
	st.markdown("**3b. Graph - Monthly sales 2018, 2019 & 2020 by Source**")
	st.plotly_chart(fig_choice_sales)
	st.markdown("**3c. Graph - Monthly Customers 2018, 2019 & 2020 by Source**")
	st.plotly_chart(fig_choice_customer)

st.markdown("#### 3d. Observation")
st.markdown("Looking at the differences between in-store and online transactions, we can see the following:")
st.markdown("""
	1. There are 4 increasingly large peaks for online sales and number of customers.
	2. There are 2 peaks February 2018 and Aug 2019 for in-store sales.
	3. There is a decline in in-store sales and customers in April 2020, due to the pandemic.
	""")

st.subheader("4. Top customers by Year")

st.markdown("**4a. 2018 Top 10 Customers by Sales**")
top_cust_2018 = data_2018[['unique_identifier', 'order_date', 'item_cost']].groupby(['unique_identifier'], as_index = False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
                                 number_of_products=pd.NamedAgg(column='order_date', aggfunc='count'),
                                )
top_cust_2018.sort_values('sales')
st.write(top_cust_2018.head(10).sort_values('sales', ascending=False))

st.markdown("**4b. 2019 Top 10 Customers by Sales**")
top_cust_2019 = data_2019[['unique_identifier', 'order_date', 'item_cost']].groupby(['unique_identifier'], as_index = False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
                                 number_of_products=pd.NamedAgg(column='order_date', aggfunc='count'),
                                )
top_cust_2019.sort_values('sales')
st.write(top_cust_2019.head(10).sort_values('sales', ascending=False))

st.markdown("**4c. 2020 Top 10 Customers by Sales**")
top_cust_2020 = data_2020[['unique_identifier', 'order_date', 'item_cost']].groupby(['unique_identifier'], as_index = False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
                                 number_of_products=pd.NamedAgg(column='order_date', aggfunc='count'),
                                )
top_cust_2020.sort_values('sales')
st.write(top_cust_2020.head(10).sort_values('sales', ascending=False))

st.markdown("#### 4d. Observation")
st.markdown("Observing the top 10 customers each year, we can identify:")
st.markdown("""
	1. There are 4 customers who have been the top spenders in all 3 years - 2MK08062, 20116676, 36409789, 29L85238".
	2. How do we retain these loyal customers?
	3. How do we attract new customers to become loyal customers?
	""")

st.subheader("5. Customer Distribution")
img1 = Image.open("sales_dist_age.jpg")
img2 = Image.open("user_dist_age.jpg")
st.markdown("**5a. Sales Distribution by Age**")
st.image(img1)

st.markdown("**5b. Customer Distribution by Age**")
st.image(img2)

st.markdown("#### 5c. Observation")
st.markdown("""
	1. Majority of customers in the last 3 years are in the age range of 25-35.
	2. Majority of sales are in the age range of 25-35 as well.
	3. There is a group of customers which did not provide their age. I did not
	remove them from the data becuase the expenditure of that group totals up to almost $10M,
	which is very significant.
	4. Most of the customer referrals are from "AMEX 2021 Promotions"
	""")

st.markdown("#### 6. Additional Insights")
st.markdown("""
	1. Explore what products are popular among the age groups 
	2. Explore how much and how often each age group spend in-store and online
	3. Explore the trends on the weekend and weekdays
	4. Explore how many days since their last purchase
	4. Calculate the cost of customer Acquisition from the different promotions/packages
	""")

st.markdown("#### 7. Action Plan(Business)")
st.markdown("""
	1. Customize promotions and product recommendations according to age groups
	2. Explore how much and how often each age group spend in-store and online

	""")

st.markdown("#### 7. Action Plan(Internal)")
st.markdown("In order for the action plans above to be feasible, I suggest the following changes to be made")
st.markdown("""
	1. Add additional data points to collect to obtain a more accurate and comprehensive overview of the business:
		a. Dates should be reported with a uniform format
		b. Transactions will need to be 
	2. Customize promotions and product recommendations according to age groups
	2. Explore how much and how often each age group spend in-store and online

	""")
# total=data.groupby(['year'], as_index=False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
#                                  orders=pd.NamedAgg(column='unique_identifier', aggfunc='count'),
#                                 )
# data_sales_2018 = px.data.gapminder().query("year == 2018")
