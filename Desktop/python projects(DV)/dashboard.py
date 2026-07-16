import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Blood Bank Management System",
    page_icon="🩸",
    layout="wide",
    
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
   .main-header {
        font-size: 2.5rem;
        color: #ff4b4b;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #fff0f0, #ffe0e0);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
   .card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
   .card-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff4b4b;
    }
   .card-label {
        font-size: 1rem;
        color: #333;
    }
   .status-badge {
        background: #28a745;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
    }
   .status-pending {
        background: #ffc107;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def init_connection():
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=BloodBank_Project;Trusted_Connection=yes')
        return conn
    except:
        st.error("❌ Database connection failed. Make sure SQL Server is running.")
        st.stop()
        return None

conn = init_connection()

# Sidebar navigation with icons
st.sidebar.markdown("# 🩸 Blood Bank System")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "🩸 Blood Stock", "⏳ Emergency Requests", "👥 Donors", "🏥 Hospitals", "📊 Reports", "➕ Add Donor"]
)

# Dashboard Page
if menu == "🏠 Dashboard":
    st.markdown('<div class="main-header">📊 Blood Bank Dashboard</div>', unsafe_allow_html=True)

    # Metrics
    donors = pd.read_sql("SELECT COUNT(*) as count FROM DONORS", conn)
    avail_bags = pd.read_sql("SELECT COUNT(*) as count FROM BLOOD_STOCK WHERE Inventory_Status='AVAILABLE' AND Expiry_Date > GETDATE()", conn)
    pending_req = pd.read_sql("SELECT COUNT(*) as count FROM EMERGENCY_REQUESTS WHERE Fulfillment_Status='PENDING'", conn)
    hospitals = pd.read_sql("SELECT COUNT(*) as count FROM HOSPITALS", conn)
    total_donations = pd.read_sql("SELECT SUM(Total_Donations) as total FROM DONORS", conn)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🩸 Total Donors", donors['count'][0], delta=None)
    col2.metric("📦 Available Bags", avail_bags['count'][0], delta=None)
    col3.metric("⏳ Pending Requests", pending_req['count'][0], delta=None)
    col4.metric("🏥 Hospitals", hospitals['count'][0], delta=None)
    col5.metric("❤️ Total Donations", total_donations['total'][0] if total_donations['total'][0] else 0, delta=None)

    st.markdown("---")

    # Two columns for charts
    left, right = st.columns(2)

    with left:
        st.subheader("Blood Group Availability")
        df_stock = pd.read_sql("SELECT Blood_Group, Available_Bags FROM vw_BloodStock", conn)
        fig = px.bar(df_stock, x='Blood_Group', y='Available_Bags', title="Available Blood Bags by Group", color='Available_Bags', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Donor Blood Group Distribution")
        df_donors = pd.read_sql("SELECT Blood_Group, COUNT(*) as Total FROM DONORS GROUP BY Blood_Group", conn)
        fig2 = px.pie(df_donors, values='Total', names='Blood_Group', title="Donor Composition", hole=0.3)
        st.plotly_chart(fig2, use_container_width=True)

    # Recent activity
    st.subheader("📋 Recent Emergency Requests")
    recent = pd.read_sql("SELECT TOP 5 Request_ID, Hospital_Name, Required_Blood_Group, Units_Requested, Fulfillment_Status FROM EMERGENCY_REQUESTS r JOIN HOSPITALS h ON r.Hospital_ID = h.Hospital_ID ORDER BY Request_ID DESC", conn)
    st.dataframe(recent, use_container_width=True)

# Blood Stock Page
elif menu == "🩸 Blood Stock":
    st.markdown('<div class="main-header">🩸 Blood Stock Management</div>', unsafe_allow_html=True)

    df = pd.read_sql("SELECT * FROM vw_BloodStock", conn)

    # Display as cards for each blood group
    cols = st.columns(4)
    for idx, row in df.iterrows():
        with cols[idx % 4]:
            st.markdown(f"""
            <div class="card">
                <div style="font-size:2rem;">🩸</div>
                <div class="card-value">{row['Blood_Group']}</div>
                <div class="card-label">Total: {row['Total_Bags']} | Available: {row['Available_Bags']}</div>
                <div class="card-label">Expired: {row['Expired_Bags']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Detailed Stock Table")
    st.dataframe(df, use_container_width=True)

    # Expiry alert
    st.subheader("⚠️ Expiring Soon (Next 7 days)")
    expiring = pd.read_sql("SELECT Bag_ID, Blood_Group, Expiry_Date FROM BLOOD_STOCK WHERE Expiry_Date BETWEEN GETDATE() AND DATEADD(DAY,7,GETDATE()) AND Inventory_Status='AVAILABLE'", conn)
    if len(expiring) > 0:
        st.warning(f"{len(expiring)} bags will expire soon!")
        st.dataframe(expiring)
    else:
        st.success("No bags expiring in next 7 days.")

# Emergency Requests Page
elif menu == "⏳ Emergency Requests":
    st.markdown('<div class="main-header">🚨 Emergency Requests</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["⏳ Pending Requests", "✅ Approved Requests"])

    with tab1:
        pending = pd.read_sql("SELECT Request_ID, Hospital_Name, Required_Blood_Group, Units_Requested, Urgency_Level, Patient_Name, Request_Timestamp FROM vw_PendingRequests", conn)
        st.dataframe(pending, use_container_width=True)

        # Approve request section
        st.subheader("Approve a Request")
        req_id = st.number_input("Enter Request ID to approve", min_value=1, step=1)
        if st.button("✅ Approve Request", type="primary"):
            try:
                cursor = conn.cursor()
                cursor.execute(f"EXEC sp_ApproveRequest {req_id}")
                cursor.commit()
                st.success(f"Request #{req_id} approved successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error approving request: {e}")

    with tab2:
        approved = pd.read_sql("SELECT Request_ID, Hospital_Name, Required_Blood_Group, Units_Requested FROM EMERGENCY_REQUESTS r JOIN HOSPITALS h ON r.Hospital_ID = h.Hospital_ID WHERE Fulfillment_Status='APPROVED'", conn)
        st.dataframe(approved, use_container_width=True)

# Donors Page
elif menu == "👥 Donors":
    st.markdown('<div class="main-header">👥 Donor Management</div>', unsafe_allow_html=True)

    donors = pd.read_sql("SELECT Donor_ID, Donor_Name, Blood_Group, City, Total_Donations, Last_Donation_Date, Eligibility_Status FROM DONORS", conn)
    st.dataframe(donors, use_container_width=True)

    # Filter by city
    cities = donors['City'].unique()
    selected_city = st.selectbox("Filter by City", ["All"] + list(cities))
    if selected_city!= "All":
        donors = donors[donors['City'] == selected_city]
        st.dataframe(donors)

    # Stats
    total_donors = len(donors)
    active_donors = len(donors[donors['Eligibility_Status'] == 'ELIGIBLE'])
    st.info(f"📊 Total Donors: {total_donors} | 🟢 Eligible: {active_donors}")

# Hospitals Page
elif menu == "🏥 Hospitals":
    st.markdown('<div class="main-header">🏥 Registered Hospitals</div>', unsafe_allow_html=True)
    hospitals = pd.read_sql("SELECT Hospital_ID, Hospital_Name, City, Phone, Contact_Person, Authorized_Status FROM HOSPITALS", conn)
    st.dataframe(hospitals, use_container_width=True)

# Reports Page
elif menu == "📊 Reports":
    st.markdown('<div class="main-header">📊 Analytical Reports</div>', unsafe_allow_html=True)

    report_type = st.selectbox("Select Report", ["Donation Trends", "Hospital Request Analysis", "Blood Group Demand"])

    if report_type == "Donation Trends":
        df = pd.read_sql("SELECT YEAR(Donation_Date) as Year, MONTH(Donation_Date) as Month, COUNT(*) as Donations FROM DONATION_HISTORY GROUP BY YEAR(Donation_Date), MONTH(Donation_Date) ORDER BY Year, Month", conn)
        fig = px.line(df, x='Month', y='Donations', color='Year', title="Monthly Donation Trends")
        st.plotly_chart(fig)

    elif report_type == "Hospital Request Analysis":
        df = pd.read_sql("SELECT h.Hospital_Name, COUNT(r.Request_ID) as Total_Requests, SUM(CASE WHEN r.Fulfillment_Status='APPROVED' THEN 1 ELSE 0 END) as Approved FROM HOSPITALS h LEFT JOIN EMERGENCY_REQUESTS r ON h.Hospital_ID = r.Hospital_ID GROUP BY h.Hospital_Name", conn)
        fig = px.bar(df, x='Hospital_Name', y=['Total_Requests', 'Approved'], title="Hospital Requests vs Approval", barmode='group')
        st.plotly_chart(fig)

    else:
        df = pd.read_sql("SELECT Required_Blood_Group, SUM(Units_Requested) as Total_Demand FROM EMERGENCY_REQUESTS WHERE Fulfillment_Status='PENDING' GROUP BY Required_Blood_Group", conn)
        fig = px.bar(df, x='Required_Blood_Group', y='Total_Demand', title="Current Blood Demand by Group")
        st.plotly_chart(fig)

# Add Donor Page - COMPLETELY FIXED
elif menu == "➕ Add Donor":
    st.markdown('<div class="main-header">➕ Register New Donor</div>', unsafe_allow_html=True)

    with st.form("add_donor_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            blood_group = st.selectbox("Blood Group", ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
            dob = st.date_input("Date of Birth", min_value=datetime(1950,1,1), max_value=datetime.now())
            cnic = st.text_input("CNIC (Format: 35201-1234567-8)")
        with col2:
            phone = st.text_input("Phone Number")
            city = st.text_input("City")
            address = st.text_area("Address")

        submitted = st.form_submit_button("Register Donor", type="primary")

        if submitted:
            try:
                cursor = conn.cursor()
                cursor.execute(f"""
                    EXEC sp_RegisterDonor
                        @Donor_Name='{name}',
                        @Blood_Group='{blood_group}',
                        @DOB='{dob}',
                        @CNIC='{cnic}',
                        @Phone='{phone}',
                        @City='{city}',
                        @Address='{address}'
                """)
                cursor.commit()
                st.success(f"✅ Donor {name} registered successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")