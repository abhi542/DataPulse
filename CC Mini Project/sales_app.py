import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Realtime Sales Dashboard",
                   page_icon='app icon.png',
                   layout='wide')


st.sidebar.header("Select Filters:")

#Parameters from the Dataset
@st.cache_data
def get_excel_data():

    df = pd.read_excel(
        io='sales_data.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )

    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_excel_data()


city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Selection Query
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# Main Page

st.title(":bar_chart: Realtime Dashboard")



# Top KPIs
total_sales = int(df_selection["Total"].sum())
avg_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(avg_rating, 0)) #to show sart emoji
avg_sale_of_a_transaction = round(df_selection["Total"].mean(), 2)


left_col, mid_col, right_col = st.columns(3)

with left_col:
    st.subheader("Total Sales:")
    st.subheader(f"$ {total_sales:,}")

with mid_col:
    st.subheader("Average Rating:")

    st.subheader(f"{avg_rating} {star_rating}")

with right_col:
    st.subheader("Average Sale Per Transaction:")
    st.subheader(f"$ {avg_sale_of_a_transaction}")

st.markdown("---")


# st.dataframe(df_selection)


# Sales by Product
sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)



#Sales by Hour
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_hourly_sales, use_container_width=True)
right_col.plotly_chart(fig_product_sales, use_container_width=True)

# Custom CSS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)