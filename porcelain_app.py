import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
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
st.markdown("Porcelain is a cult-premium skincare brand from Singapore with a vision to marry craftsmanship and technology to create a future of skincare.\
	The report details the analysis and findings of Porcelain's e-commerce and in-store dataset that contains transactions that occurred over 3 years - 2018, 2019 and 2020.")
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

DATA_URL = ("./final_merge.csv")

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
df_total_sales = data[['source','year_month','item_cost','unique_identifier']].groupby(['source'], as_index=False).agg(sales=pd.NamedAgg(column='item_cost', aggfunc='sum'),
                                 orders=pd.NamedAgg(column='unique_identifier', aggfunc='count'),
                                 customers=pd.NamedAgg(column='unique_identifier', aggfunc='nunique'),
                                )
df_total_sales["sales_%"] = 100 * df_total_sales["sales"] / df_total_sales["sales"].sum()
df_total_sales["orders_%"] = 100 * df_total_sales["orders"] / df_total_sales["orders"].sum()
df_total_sales["customers_%"] = 100 * df_total_sales["customers"] / df_total_sales["customers"].sum()
fig_sales_pct = px.bar(df_total_sales, x="sales_%", y="source", orientation='h')
fig_orders_pct = px.bar(df_total_sales, x="orders_%", y="source", orientation='h')
fig_cust_pct = px.bar(df_total_sales, x="customers_%", y="source", orientation='h')

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

st.markdown("**3d. Percentage Distribution by Source**")
st.markdown("***Sales***")
st.plotly_chart(fig_sales_pct)
st.markdown("***Orders***")
st.plotly_chart(fig_orders_pct)
st.markdown("***Customers***")
st.plotly_chart(fig_cust_pct)

st.markdown("#### 3d. Observation")
st.markdown("Looking at the differences between in-store and online transactions, we can see the following:")
st.markdown("""
	1. There are 4 increasingly large peaks for online sales and number of customers.
	2. There are 2 peaks in February 2018 and Aug 2019 for in-store sales.
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

img6 = Image.open("no_of_purchases.jpg")
st.markdown("**4d. No of Purchases per User, Distribution of users per Purchase frequency, No. of users per Age groups**")
st.image(img6)

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

st.subheader("6. Sales by item type")
img3 = Image.open("sales_by_itemtype.jpg")
st.markdown("**6a. Sales Distribution by Item Type**")
st.image(img3)

st.markdown("#### 6b. Observation")
st.markdown("""
	1. Transactions of Services ilarger than the other product significantly, more than twice of the runner up.
	2. The most popular Service is the 'Quintessential Facial' service.
	""")

st.subheader("7. Sales on weekday/weekend per source")
img4 = Image.open("day_end_sales.jpg")
st.markdown("**7a.  Sales on weekday/weekend per source**")
st.image(img4)

st.markdown("#### 7b. Observation")
st.markdown("""
	1. The ratio of in-store to online sales during weekdays and weekends are similar.
	2. The transactions in-store are much larger than the ones online.
	""")

st.subheader("8. Sales per ReferralSource")
img5 = Image.open("sales_referral.jpg")
st.markdown("**8a.  Sales per ReferralSource**")
st.image(img5)

st.markdown("#### 8b. Observation")
st.markdown("""
	1. The leading referral source for customers is "AMEX 2021 Promottions", followed by customers who did not provide their referral source.
	2. The name of the referral source "Amex 2021" is confusing because none of the customers in the dataset used it in 2021. 
	""")

st.markdown("#### 6. Additional Insights")
st.markdown("")
st.markdown("""
	1. Explore what products are popular among the age groups 
	2. Explore how much and how often each age group spend in-store and online
	3. Explore the trends on the weekend and weekdays
	4. Explore how many days since their last purchase
	5. Calculate the cost of customer acquisition from the different promotions/packages, the conversion rate.
	6. How many of the new customers gained from the spikes and how many of them returned?
	""")

st.markdown("#### 7. Action Plan(Business)")
st.markdown("""
	1. Customize promotions and product recommendations according to age groups
	2. Explore how much and how often each age group spend in-store and online
	3. Send follow-up emails to users with promotions and sales after they are inactive for 100 days since last visit
	4. From the results we can clearly see that the in-store transactions are larger than the ones online. We can explore the following,
	perform a cost benefit analysis between boosting your online presence or to open a new branch in Singapore/China. Since most of your in-store busisness are contributed from services,
	it makes sense the next step of expansion is to opena a brnach but more data will be required to justify this decision. 
	""")

st.markdown("#### 7. Action Plan(Internal)")
st.markdown("In order for the action plans above to be feasible, I suggest the following changes to be made")
st.markdown("""
	1. Add additional data points to collect to obtain a more accurate and comprehensive overview of the business:
		a. Dates should be reported with a uniform format
		b. Transactions should be tracked with a unique id just like there is a unique id for users
		c. gender of customers can help gain more insights as well
		d. In-store transactions should be categorized into the branches you have. This allows you to see which branch may be overbooked.
		This is a good indicator to determine whether or not to open the 4th branch in Singapore.

	2. Naming convention for promotions/referrals can be clearer and have a time period associated with it for easier traceability
	3. Products and services should be categorized even further. For example, for products, we can categorize them to serum, clenaser, toner, moisturizer
	or by their line. Services can be categorized into facial, fusion, body etc. This allows us to better track the popularity of your product.
	4. We can add web analytics to your e-commerce sites to gain insights of your web traffic. We can identify the averge browsing times of the your customers,
	rates of cart abandonment as well as appointment abandonment.

	""")
