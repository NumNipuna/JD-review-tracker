import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Job Description Review Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR BRANDING & STYLING ---
# Using a professional corporate theme (Deep Blues, Teals, and Clean Greys)
st.markdown("""
    <style>
        /* 1. Set the outermost canvas frame background to a soft, professional light grey */
        [data-testid="stAppViewContainer"] {
            background-color: #052F4A !important;
        }

        /* 2. Make the header and core element block wrappers transparent so they don't break layout colors */
        [data-testid="stHeader"], [data-testid="stVerticalBlock"] {
            background-color: transparent !important;
        }

        /* 3. Force all user chart/content container blocks to be crisp white cards with clean borders */
        [data-testid="stElementContainer"] div[data-testid="stMarkdownContainer"] {
            background-color: transparent !important;
        }
        
        /* 4. Fix Plotly chart background containers specifically so they don't leak */
        .js-plotly-plot .plotly, .user-select-none {
            background-color: #ffffff !important;
            border-radius: 12px;
        }

        /* 5. Custom Isolated Metric Card UI styling (Stays pure white, floating over the grey background) */
        .metric-card {
            background-color: #E7E5E4 !important; /* Explicitly forces the card itself to stay this color */
            padding: 10px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Modern, soft UI shadow */
            border-left: 10px solid #FFDF20;
            text-align: center;
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50 !important;
        }
        .metric-label {
            font-size: 13px;
            color: #4A5565 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 3px;
        }
        
        /* Customize space between title and top */
        
        [data-testid="stAppViewContainer"] .block-container {
            padding-top: 1.5rem !important;    /* Default is close to 6rem; changing to 1.5rem brings everything up crisply */
            padding-bottom: 2rem !important;
        /*-----------------------------------------------------------------------------*/
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
# Dashboard sync with excel live
def get_file_modified_time(filepath):
    """Gets the last time the Excel sheet was saved."""
    try:
        return os.path.getmtime(filepath)
    except OSError:
        return 0

@st.cache_data(ttl=5) # 💡 Automatically clears cache memory every 5 seconds
def load_data(file_path):
    # Loading the sheet directly from your computer path live
    df = pd.read_excel(file_path, sheet_name="Vstak")
    
    # Clean string spaces
    df['Status'] = df['Status'].str.strip()
    df['Department'] = df['Department'].str.strip()
    df['Job Title'] = df['Job Title'].str.strip()
    return df

# Your actual absolute path to the data
excel_file_path = "C:/Users/Asus/Desktop/Python/JD/Master JD.xlsx"

try:
    # We pass the modified time into the loader. 
    # If the file changes on your desktop, Streamlit notices instantly!
    file_mtime = get_file_modified_time(excel_file_path)
    df = load_data(excel_file_path)
except FileNotFoundError:
    st.error(f"⚠️ Could not find 'Master JD.xlsx' at {excel_file_path}.")
    st.stop()


# --- FUNCTION TO CONVERT IMAGE TO BASE64 ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
# --- SIDEBAR & LOGO ---

logo_path = r"C:\Users\Asus\Desktop\Python\JD\logo.png"


if os.path.exists(logo_path):
    # 1. Convert the image
    img_base64 = get_base64_image(logo_path)
    
    # 2. Design your custom HTML & CSS styling wrapper
    custom_sidebar_html = f"""
    <div style="
        display: flex; 
        justify-content: center;   /* Horizontal Alignment: center, flex-start (left), flex-end (right) */
        align-items: center;
        margin-top: -40px;          /* Custom top space */
        margin-bottom: 25px;       /* Custom bottom space */
        padding: 5px;
    ">
        <img src="data:image/png;base64,{img_base64}" style="
            width: 150px;          /* Set explicit fixed width */
            height: auto;          /* Maintain original aspect ratio */
            border-radius: 2px;    /* Optional: rounded edges */
            box-shadow: 0px 0px 0px rgba(0,0,0,0); /* Optional: soft UI drop shadow */
        ">
    </div>
    """
    
    # 3. Inject it into the sidebar
    st.sidebar.markdown(custom_sidebar_html, unsafe_allow_html=True)
else:
    st.sidebar.warning("⚠️ Logo path not found.")




# --- ADD THIS REFRESH BUTTON ---
left_co, cent_co, right_co = st.sidebar.columns([0.5, 3, 0.5])

with cent_co:
    if st.button("🔄 Clear Cache & Sync Excel"):
        st.cache_data.clear()
        st.toast("Data synced with Excel successfully!", icon="✅")
        st.rerun()

st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("Use the filters below to drill down into specific areas.")

# Sidebar Filters
departments = sorted(df['Department'].dropna().unique())
selected_dept = st.sidebar.multiselect("Select Department", options=departments, default=departments)

# Filter dataframe based on department selection
df_filtered = df[df['Department'].isin(selected_dept)]

# Dynamically update Job Titles based on selected departments
job_titles = sorted(df_filtered['Job Title'].dropna().unique())
selected_jobs = st.sidebar.multiselect("Select Job Title", options=job_titles, default=job_titles)

# Final filtered dataframe
df_filtered = df_filtered[df_filtered['Job Title'].isin(selected_jobs)]

# --- MAIN CONTENT HEADER ---


main_head_col, snap_btn_col = st.columns([3, 1])

with main_head_col:
    st.title("📋 Job Description Review Tracker")
    st.markdown("Real-time tracking of Master Job Description completion statuses across departments.")

with snap_btn_col:
    # JavaScript Capture Component embedded inside the panel block layout canvas
    screenshot_js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
    function captureDashboard() {
        const element = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
        html2canvas(element, { useCORS: true, backgroundColor: '#052F4A', scale: 2 }).then(canvas => {
            let link = document.createElement('a');
            link.download = 'JD_Dashboard_Snapshot.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        });
    }
    </script>
    <div style="text-align: right; margin-top: 20px;">
        <button onclick="captureDashboard()" style="
            background-color: #FFDF20; color: #052F4A; border: none; padding: 10px 18px; 
            font-weight: bold; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        ">📸 Capture Dashboard</button>
    </div>
    """
    st.components.v1.html(screenshot_js, height=70)
st.markdown("---")

# --- KPI METRICS LAYER ---
total_tasks = len(df_filtered)
total_department = 23
done_tasks = len(df_filtered[df_filtered['Status'] == 'Done'])
pending_tasks = len(df_filtered[df_filtered['Status'] == 'Pending'])
completion_rate = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0
col1, col2, col3, col4 = st.columns(4)

#----My calculations----
status_done_departments = len(df_filtered[df_filtered['Status'] == 'Done']['Department'].unique().tolist()) # at least one status is done
status_pending_departments = len(df_filtered[df_filtered['Status'] == 'Pending']['Department'].unique().tolist()) # at least one status is pending
completed_department = status_done_departments-status_pending_departments
pending_department = total_department-completed_department

dept_counts = df_filtered.groupby(['Department', 'Status']).size().unstack(fill_value=0)

for status in ['Done', 'Pending']:
    if status not in dept_counts.columns:
        dept_counts[status] = 0

# 2. Calculate Total Tasks per department and the final Completion Percentage
dept_counts['Total Tasks'] = dept_counts['Done'] + dept_counts['Pending']
dept_counts['Progress %'] = (dept_counts['Done'] / dept_counts['Total Tasks'] * 100).round(1)

Overall_Progress = sum(dept_counts['Progress %']) *100 /2300

with col1:
    st.markdown(f'<div class="metric-card" style="border-left-color: #3498db;"><div class="metric-value">{total_department}</div><div class="metric-label">total department</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card" style="border-left-color: #e74c3c;"><div class="metric-value">{completed_department}</div><div class="metric-label">completed department</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card" style="border-left-color: #2ecc71;"><div class="metric-value">{pending_department}</div><div class="metric-label">pending department</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card" style="border-left-color: #f1c40f;"><div class="metric-value">{Overall_Progress:.2f}%</div><div class="metric-label">Overall Progress</div></div>', unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)

# --- VISUALIZATIONS SECTION ---
chart_col1, chart_col2 = st.columns([1, 1])

# Color definitions matching a clean business palette
color_map = {'Done': '#2ecc71', 'Pending': '#e74c3c'}  #3498db

with chart_col1:
    st.subheader("Overall Status Breakdown")
    if total_tasks > 0:
        status_counts = df_filtered['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig_pie = px.pie(
            status_counts, 
            values='Count', 
            names='Status',
            color='Status',
            color_discrete_map=color_map,
            hole=0.4,
        )
        fig_pie.update_traces(textinfo='percent+value', textfont_size=14)
        
        #Change the chart design
        fig_pie.update_layout(
            paper_bgcolor='#0e1117',  # Outer chart background canvas card
            plot_bgcolor='#0e1117',   # Inner pie slice region background
            margin=dict(t=40, b=40, l=40, r=40), 
            height=350, 
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    else:
        st.info("No data available for the current filter selection.")

with chart_col2:
    st.subheader("Progress by Department")
    if total_tasks > 0:
        # Grouping data for a stacked bar chart
        dept_status = df_filtered.groupby(['Department', 'Status']).size().unstack(fill_value=0).reset_index()
        
        # Ensure both columns exist for plotting
        for status in ['Done', 'Pending']:
            if status not in dept_status.columns:
                dept_status[status] = 0

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(y=dept_status['Department'], x=dept_status['Done'], name='Done', orientation='h', marker_color='#2ecc71'))
        fig_bar.add_trace(go.Bar(y=dept_status['Department'], x=dept_status['Pending'], name='Pending', orientation='h', marker_color='#e74c3c'))
        
        fig_bar.update_layout(
            barmode='stack',
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            xaxis_title="Number of Tasks",
            yaxis=dict(autorange="reversed") # Keeps alphabetical flow crisp
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No data available for the current filter selection.")

st.markdown("---")

# --- ADVANCED ADDED VISUALIZATION: DRILL-DOWN HEATMAP / MATRIX ---
st.subheader("🔍 Job Title Progress Deep-Dive")
st.markdown("This enhanced chart visualizes the precise amount of work remaining or finalized for individual roles within your filtered selection.")

if total_tasks > 0:
    job_status = df_filtered.groupby(['Job Title', 'Status']).size().unstack(fill_value=0).reset_index()
    for status in ['Done', 'Pending']:
        if status not in job_status.columns:
            job_status[status] = 0
            
    job_status['Total'] = job_status['Done'] + job_status['Pending']
    job_status['Completion %'] = (job_status['Done'] / job_status['Total'] * 100).round(1)
    job_status = job_status.sort_values(by='Completion %', ascending=True)

    fig_job = px.bar(
        job_status,
        x='Completion %',
        y='Job Title',
        orientation='h',
        text='Completion %',
        labels={'Completion %': 'Percentage Completed (%)'},
        color='Completion %',
        color_continuous_scale=px.colors.sequential.Blugrn,
        height=max(400, len(job_status) * 35) # Responsive sizing to prevent title overlapping
    )
    fig_job.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_job.update_layout(xaxis=dict(range=[0, 115])) # Extra padding room for labels
    st.plotly_chart(fig_job, use_container_width=True)

# --- RETAINED RAW DATA TABLE FOR AUDITING ---
st.markdown("---")
st.subheader("📝 Detailed Task Breakdown")
st.markdown("Filter and inspect individual specific tasks, or export the curated view below.")

# Formatting and displaying the clean table view
view_df = df_filtered[['Department', 'Job Title', 'Task Category (Main Duty)', 'Specific Task', 'Status']].reset_index(drop=True)
st.dataframe(view_df, use_container_width=True)