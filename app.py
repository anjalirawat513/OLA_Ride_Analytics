import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection
import queries as q
import streamlit.components.v1 as components

# ---------------------------------------------------
# Streamlit Config
# ---------------------------------------------------
st.set_page_config(page_title="Ride Analytics", layout="wide")
st.title("🚗 Ride Analytics Dashboard")

# ---------------------------------------------------
# Utility: Run SQL Queries
# ---------------------------------------------------
@st.cache_data
def run_query(sql):
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

# Utility: CSV download
def download_button(df, filename="query_results.csv"):
    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv"
    )

# ---------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------
st.sidebar.header("Navigation")
section = st.sidebar.radio(
    "Select Section:",
    ["Streamlit Dashboard", "SQL Queries", "Power BI Dashboard"]
)

# ---------------------------------------------------
# Streamlit Dashboard (Custom Visuals)
# ---------------------------------------------------
if section == "Streamlit Dashboard":
    st.subheader("📊 Streamlit Dashboard")

    try:
        df = run_query("SELECT * FROM OLA_DataSet")
    except Exception as e:
        st.error(f"Could not load data: {e}")
        df = pd.DataFrame()

    if not df.empty:
        tab1, tab2, tab3 = st.tabs(["📈 Ride Trends", "💰 Revenue", "⭐ Ratings"])

        # ---------------- Ride Trends ----------------
        with tab1:
            date_cols = [col for col in df.columns if "date" in col.lower() or "time" in col.lower()]
            if date_cols:
                date_col = date_cols[0]  # pick first match
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

                if "Booking_ID" in df.columns:
                    ride_trend = df.groupby(df[date_col].dt.date)["Booking_ID"].count().reset_index()
                    ride_trend.columns = ["Date", "Total_Rides"]

                    fig = px.line(ride_trend, x="Date", y="Total_Rides", title="Rides Over Time")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("⚠️ Booking_ID column not found for ride counts.")
            else:
                st.info("⚠️ No date column found in dataset.")

        # ---------------- Revenue ----------------
        with tab2:
            if "Payment_Method" in df.columns and "Booking_Value" in df.columns:
                revenue = df.groupby("Payment_Method")["Booking_Value"].sum().reset_index()
                fig = px.bar(revenue, x="Payment_Method", y="Booking_Value", color="Payment_Method",
                             title="Revenue by Payment Method")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("⚠️ Payment_Method or Booking_Value column not found.")

        # ---------------- Ratings ----------------
        with tab3:
            if "Vehicle_Type" in df.columns and "Customer_Rating" in df.columns:
                fig = px.box(df, x="Vehicle_Type", y="Customer_Rating",
                             title="Customer Ratings Distribution")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("⚠️ Vehicle_Type or Customer_Rating column not found.")
    else:
        st.info("No data available to display dashboard.")

# ---------------------------------------------------
# SQL Queries Section (Interactive)
# ---------------------------------------------------
elif section == "SQL Queries":
    st.sidebar.subheader("🔎 Global Filters")

    # Global Filters
    payment_filter = st.sidebar.selectbox("Payment Method", ["All", "UPI", "Card", "Cash", "Wallet"])
    vehicle_filter = st.sidebar.selectbox("Vehicle Type", ["All", "Mini", "Prime Sedan", "Prime SUV"])

    sql_choice = st.sidebar.selectbox(
        "Choose a SQL Question:",
        [
            "Q1: All Successful Bookings",
            "Q2: Avg Ride Distance by Vehicle",
            "Q3: Cancelled Rides by Customers",
            "Q4: Top 5 Customers",
            "Q5: Cancelled by Drivers (Personal/Car)",
            "Q6: Driver Ratings (Prime Sedan)",
            "Q7: Rides with UPI Payment",
            "Q8: Avg Customer Rating by Vehicle",
            "Q9: Total Booking Value (Successful)",
            "Q10: Incomplete Rides & Reasons",
        ]
    )

    # ----------------------------
    # Q1. All Successful Bookings
    # ----------------------------
    if sql_choice == "Q1: All Successful Bookings":
        st.subheader("📋 All Successful Bookings")

        query = q.GET_ALL_BOOKINGS.strip().rstrip(";")
        if vehicle_filter != "All":
            query += f" AND Vehicle_Type = '{vehicle_filter}'"
        if payment_filter != "All":
            query += f" AND Payment_Method = '{payment_filter}'"

        df = run_query(query)

        tab1, tab2 = st.tabs(["📋 Data", "📊 Visualization"])
        with tab1:
            st.dataframe(df, use_container_width=True)
            download_button(df, "successful_bookings.csv")
        with tab2:
            if not df.empty and "Vehicle_Type" in df.columns:
                fig = px.histogram(df, x="Vehicle_Type", title="Bookings by Vehicle Type")
                st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # Q2. Avg Ride Distance
    # ----------------------------
    elif sql_choice == "Q2: Avg Ride Distance by Vehicle":
        st.subheader("📊 Average Ride Distance per Vehicle")
        df = run_query(q.AVG_RIDE_DISTANCE_BY_VEHICLE)

        tab1, tab2 = st.tabs(["📋 Data", "📊 Visualization"])
        with tab1:
            st.dataframe(df)
            download_button(df, "avg_ride_distance.csv")
        with tab2:
            if not df.empty:
                fig = px.bar(df, x="Vehicle_Type", y="AvgDistance", color="Vehicle_Type")
                st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # Q3. Cancelled Rides by Customers
    # ----------------------------
    elif sql_choice == "Q3: Cancelled Rides by Customers":
        st.subheader("❌ Cancelled Rides by Customers")
        df = run_query(q.TOTAL_CANCELLED_BY_CUSTOMERS)
        total_cancelled = df.iloc[0, 0]
        st.metric("Total Cancelled by Customers", total_cancelled)
        download_button(df, "cancelled_by_customers.csv")

    # ----------------------------
    # Q4. Top 5 Customers
    # ----------------------------
    elif sql_choice == "Q4: Top 5 Customers":
        st.subheader("⭐ Top 5 Customers by Total Rides")
        df = run_query(q.TOP_5_CUSTOMERS)

        tab1, tab2 = st.tabs(["📋 Data", "📊 Visualization"])
        with tab1:
            st.dataframe(df)
            download_button(df, "top_5_customers.csv")
        with tab2:
            fig = px.bar(df, x="Customer_ID", y="total_rides", color="total_rides")
            st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # Q5. Cancelled by Drivers
    # ----------------------------
    elif sql_choice == "Q5: Cancelled by Drivers (Personal/Car)":
        st.subheader("🚙 Rides Cancelled by Drivers (Personal/Car Issues)")
        df = run_query(q.CANCELLED_BY_DRIVER_ISSUES)
        cancelled_by_drivers = df.iloc[0, 0]
        st.metric("Driver Cancelled Rides (Personal/Car)", cancelled_by_drivers)
        download_button(df, "cancelled_by_drivers.csv")

    # ----------------------------
    # Q6. Driver Ratings (Prime Sedan)
    # ----------------------------
    elif sql_choice == "Q6: Driver Ratings (Prime Sedan)":
        st.subheader("⭐ Driver Ratings for Prime Sedan")
        df = run_query(q.DRIVER_RATING_STATS_PRIME_SEDAN)

        st.dataframe(df)
        st.metric("Max Rating", df["MaxRating"].iloc[0])
        st.metric("Min Rating", df["MinRating"].iloc[0])
        download_button(df, "prime_sedan_ratings.csv")

    # ----------------------------
    # Q7. Rides with UPI Payment
    # ----------------------------
    elif sql_choice == "Q7: Rides with UPI Payment":
        st.subheader("💳 Rides Paid via UPI")
        df = run_query(q.RIDES_WITH_UPI)
        st.dataframe(df, use_container_width=True)
        download_button(df, "rides_upi.csv")

    # ----------------------------
    # Q8. Avg Customer Rating
    # ----------------------------
    elif sql_choice == "Q8: Avg Customer Rating by Vehicle":
        st.subheader("⭐ Average Customer Rating by Vehicle")
        df = run_query(q.AVG_CUSTOMER_RATING_BY_VEHICLE)

        tab1, tab2 = st.tabs(["📋 Data", "📊 Visualization"])
        with tab1:
            st.dataframe(df)
            download_button(df, "avg_customer_ratings.csv")
        with tab2:
            if not df.empty:
                fig = px.bar(df, x="Vehicle_Type", y="AvgCustomerRating", color="Vehicle_Type")
                st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # Q9. Total Booking Value
    # ----------------------------
    elif sql_choice == "Q9: Total Booking Value (Successful)":
        st.subheader("💰 Total Booking Value (Successful Rides)")
        df = run_query(q.TOTAL_BOOKING_VALUE_SUCCESS)
        total_value = df.iloc[0, 0]
        st.metric("Total Successful Booking Value", f"₹{total_value:,.2f}")
        download_button(df, "total_successful_value.csv")

    # ----------------------------
    # Q10. Incomplete Rides
    # ----------------------------
    elif sql_choice == "Q10: Incomplete Rides & Reasons":
        st.subheader("⚠️ Incomplete Rides with Reasons")
        df = run_query(q.INCOMPLETE_RIDES_WITH_REASON)

        tab1, tab2 = st.tabs(["📋 Data", "📊 Visualization"])
        with tab1:
            st.dataframe(df, use_container_width=True)
            download_button(df, "incomplete_rides.csv")
        with tab2:
            if not df.empty and "Incomplete_Rides_Reason" in df.columns:
                reason_counts = df["Incomplete_Rides_Reason"].value_counts().reset_index()
                reason_counts.columns = ["Reason", "Count"]
                fig = px.bar(reason_counts, x="Reason", y="Count")
                st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Power BI Embedded Dashboard (Unchanged)
# ---------------------------------------------------
elif section == "Power BI Dashboard":
    st.subheader("📊 Power BI Dashboard")

    powerbi_iframe = """
    <iframe title="OLA PB"
            width="100%" height="900"
            src="https://app.powerbi.com/reportEmbed?reportId=060169b1-626c-44be-b5cd-c85f982c065d&autoAuth=true&ctid=f9465cb1-7889-4d9a-b552-fdd0addf0eb1"
            frameborder="0" allowFullScreen="true"></iframe>
    """
    components.html(powerbi_iframe, height=900)
