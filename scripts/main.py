import streamlit as st
import pandas as pd
import io

# Set page configuration
st.set_page_config(
    page_title="QAS <-> WIMT Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Atlas Copco Group branding
st.markdown("""
<style>
    /* Atlas Copco Group Color Variables */
    :root {
        --atlas-teal: #054E5A;
        --atlas-white: #FFFFFF;
        --atlas-gray: #A1A9B4;
        --atlas-gold: #E1B77E;
        --accent-green: #5D7875;
        --accent-light-green: #CED9D7;
        --accent-blue: #123F6D;
    }
    
    /* Main app background */
    .stApp {
        background-color: var(--atlas-white);
    }
    
    /* Main title styling */
    .main h1 {
        color: var(--atlas-teal) !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 1rem 0 !important;
        border-bottom: 3px solid var(--atlas-gold) !important;
        margin-bottom: 2rem !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--accent-light-green) !important;
    }
    
    .sidebar .sidebar-content {
        background-color: var(--accent-light-green) !important;
    }
    
    /* Sidebar headers */
    .sidebar h2, .sidebar h3 {
        color: var(--atlas-teal) !important;
        font-weight: bold !important;
    }
    
    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background-color: var(--atlas-teal) !important;
        border: none !important;
        color: var(--atlas-white) !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: var(--accent-blue) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(5, 78, 90, 0.3) !important;
    }
    
    /* Secondary buttons */
    .stButton > button {
        background-color: var(--atlas-gray) !important;
        border: 2px solid var(--atlas-teal) !important;
        color: var(--atlas-teal) !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: var(--atlas-teal) !important;
        color: var(--atlas-white) !important;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background-color: var(--atlas-gold) !important;
        border: none !important;
        color: var(--atlas-teal) !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: var(--accent-green) !important;
        color: var(--atlas-white) !important;
        transform: translateY(-2px) !important;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background-color: var(--atlas-white) !important;
        border: 2px dashed var(--atlas-teal) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background-color: var(--atlas-white) !important;
        border: 2px solid var(--atlas-teal) !important;
        border-radius: 8px !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: var(--atlas-teal) !important;
        font-weight: 500 !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: var(--accent-green) !important;
        color: var(--atlas-white) !important;
        border-radius: 8px !important;
        border-left: 5px solid var(--atlas-gold) !important;
    }
    
    /* Info messages */
    .stInfo {
        background-color: var(--accent-light-green) !important;
        color: var(--atlas-teal) !important;
        border-radius: 8px !important;
        border-left: 5px solid var(--accent-blue) !important;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: var(--atlas-gold) !important;
        color: var(--atlas-teal) !important;
        border-radius: 8px !important;
        border-left: 5px solid var(--atlas-teal) !important;
    }
    
    /* Error messages */
    .stError {
        background-color: #ff6b6b !important;
        color: var(--atlas-white) !important;
        border-radius: 8px !important;
        border-left: 5px solid #d63031 !important;
    }
    
    /* Subheaders */
    .main h2, .main h3 {
        color: var(--atlas-teal) !important;
        font-weight: bold !important;
        border-bottom: 2px solid var(--atlas-gold) !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 2px solid var(--atlas-teal) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    /* Dataframe headers */
    .stDataFrame thead th {
        background-color: var(--atlas-teal) !important;
        color: var(--atlas-white) !important;
        font-weight: bold !important;
    }
    
    /* Dataframe rows */
    .stDataFrame tbody tr:nth-child(even) {
        background-color: var(--accent-light-green) !important;
    }
    
    /* Dividers */
    .stDivider {
        border-color: var(--atlas-gold) !important;
        border-width: 2px !important;
    }
    
    /* Footer styling */
    .footer {
        background-color: var(--atlas-teal) !important;
        color: var(--atlas-white) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin-top: 2rem !important;
    }
    
    /* Sidebar file uploader */
    .sidebar .stFileUploader {
        background-color: var(--atlas-white) !important;
        border: 2px solid var(--atlas-teal) !important;
        border-radius: 8px !important;
    }
    
    /* Sidebar multiselect */
    .sidebar .stMultiSelect > div > div {
        background-color: var(--atlas-white) !important;
        border: 2px solid var(--atlas-teal) !important;
    }
    
    /* Instructions section */
    .instructions {
        background-color: var(--accent-light-green) !important;
        padding: 1.5rem !important;
        border-radius: 8px !important;
        border-left: 5px solid var(--atlas-teal) !important;
        margin: 1rem 0 !important;
    }
    
    /* Custom card styling */
    .custom-card {
        background-color: var(--atlas-white) !important;
        padding: 1.5rem !important;
        border-radius: 8px !important;
        border: 2px solid var(--atlas-gray) !important;
        box-shadow: 0 2px 4px rgba(5, 78, 90, 0.1) !important;
        margin: 1rem 0 !important;
    }
    
    /* Metric styling */
    .stMetric {
        background-color: var(--accent-light-green) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--atlas-teal) !important;
    }
    
    .stMetric label {
        color: var(--atlas-teal) !important;
        font-weight: bold !important;
    }
    
    .stMetric div {
        color: var(--accent-blue) !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title with custom styling
st.markdown('<h1 style="color: #054E5A; text-align: center; font-weight: bold; padding: 1rem 0; border-bottom: 3px solid #E1B77E; margin-bottom: 2rem;">🔄 QAS <-> WIMT Converter</h1>', unsafe_allow_html=True)

# Initialize session state
if 'qas_df' not in st.session_state:
    st.session_state.qas_df = None
if 'wimt_df' not in st.session_state:
    st.session_state.wimt_df = None
if 'matched_data' not in st.session_state:
    st.session_state.matched_data = None

# Sidebar
with st.sidebar:
    st.header("File Upload")
    
    # QAS file upload
    st.subheader("QAS File")
    qas_file = st.file_uploader(
        "Upload QAS Excel file:",
        type=['xlsx', 'xls'],
        key="qas_upload"
    )
    
    # WIMT file upload
    st.subheader("WIMT File")
    wimt_file = st.file_uploader(
        "Upload WIMT Excel file:",
        type=['xlsx', 'xls'],
        key="wimt_upload"
    )
    
    st.divider()
    
    # Column selection (only show if both files are uploaded)
    if qas_file and wimt_file:
        st.subheader("Column Selection")
        
        # Load the files
        try:
            st.session_state.qas_df = pd.read_excel(qas_file)
            st.session_state.wimt_df = pd.read_excel(wimt_file)
            
            # QAS column selection
            qas_columns = st.multiselect(
                "Select QAS columns to compare:",
                options=st.session_state.qas_df.columns.tolist(),
                key="qas_columns"
            )
            
            # WIMT column selection
            wimt_columns = st.multiselect(
                "Select WIMT columns to compare:",
                options=st.session_state.wimt_df.columns.tolist(),
                key="wimt_columns"
            )
            
            st.divider()
            
            # Settings
            st.subheader("Settings")
            case_sensitive = st.checkbox("Case sensitive comparison", value=False)
            include_all_columns = st.checkbox("Include all columns in output", value=True)
            
            # Compare button (only show if columns are selected)
            if qas_columns and wimt_columns and st.button("Find Matches", type="primary", use_container_width=True):
                try:
                    # Create composite keys for comparison
                    qas_temp = st.session_state.qas_df.copy()
                    wimt_temp = st.session_state.wimt_df.copy()
                    
                    # Create comparison keys by combining selected columns
                    qas_key_parts = []
                    wimt_key_parts = []
                    
                    for col in qas_columns:
                        if case_sensitive:
                            qas_key_parts.append(qas_temp[col].astype(str))
                        else:
                            qas_key_parts.append(qas_temp[col].astype(str).str.lower())
                    
                    for col in wimt_columns:
                        if case_sensitive:
                            wimt_key_parts.append(wimt_temp[col].astype(str))
                        else:
                            wimt_key_parts.append(wimt_temp[col].astype(str).str.lower())
                    
                    # Combine columns with separator
                    qas_temp['_compare_key'] = qas_key_parts[0] if len(qas_key_parts) == 1 else qas_key_parts[0].str.cat(qas_key_parts[1:], sep='|')
                    wimt_temp['_compare_key'] = wimt_key_parts[0] if len(wimt_key_parts) == 1 else wimt_key_parts[0].str.cat(wimt_key_parts[1:], sep='|')
                    
                    if include_all_columns:
                        # Merge dataframes on the comparison key
                        merged_df = pd.merge(
                            qas_temp, 
                            wimt_temp, 
                            on='_compare_key', 
                            how='inner',
                            suffixes=('_QAS', '_WIMT')
                        )
                        merged_df = merged_df.drop('_compare_key', axis=1)
                        st.session_state.matched_data = merged_df
                    else:
                        # Only include the selected columns and matches
                        qas_matches = qas_temp[qas_temp['_compare_key'].isin(wimt_temp['_compare_key'])]
                        wimt_matches = wimt_temp[wimt_temp['_compare_key'].isin(qas_temp['_compare_key'])]
                        
                        # Combine the matching rows
                        qas_selected = qas_matches[qas_columns].copy()
                        wimt_selected = wimt_matches[wimt_columns].copy()
                        
                        # Add suffixes to column names
                        qas_selected.columns = [f"{col}_QAS" for col in qas_selected.columns]
                        wimt_selected.columns = [f"{col}_WIMT" for col in wimt_selected.columns]
                        
                        # Reset indices and concatenate
                        qas_selected = qas_selected.reset_index(drop=True)
                        wimt_selected = wimt_selected.reset_index(drop=True)
                        
                        st.session_state.matched_data = pd.concat([qas_selected, wimt_selected], axis=1)
                    
                    st.success(f"Found {len(st.session_state.matched_data)} matches!")
                    
                except Exception as e:
                    st.error(f"Error during comparison: {str(e)}")
            
            elif qas_columns or wimt_columns:
                if not qas_columns:
                    st.warning("Please select at least one QAS column")
                if not wimt_columns:
                    st.warning("Please select at least one WIMT column")
        
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("QAS File Preview")
    if st.session_state.qas_df is not None:
        st.dataframe(st.session_state.qas_df.head(10), use_container_width=True)
        st.info(f"Shape: {st.session_state.qas_df.shape[0]} rows × {st.session_state.qas_df.shape[1]} columns")
    else:
        st.info("Upload a QAS Excel file to see preview")

with col2:
    st.subheader("WIMT File Preview")
    if st.session_state.wimt_df is not None:
        st.dataframe(st.session_state.wimt_df.head(10), use_container_width=True)
        st.info(f"Shape: {st.session_state.wimt_df.shape[0]} rows × {st.session_state.wimt_df.shape[1]} columns")
    else:
        st.info("Upload a WIMT Excel file to see preview")

# Results section
if st.session_state.matched_data is not None:
    st.divider()
    st.subheader("Matching Results")
    
    col3, col4 = st.columns([3, 1])
    
    with col3:
        st.dataframe(st.session_state.matched_data, use_container_width=True)
        st.info(f"Total matches found: {len(st.session_state.matched_data)}")
    
    with col4:
        st.subheader("Download Results")
        
        # Convert to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.matched_data.to_excel(writer, sheet_name='Matches', index=False)
        
        st.download_button(
            label="📥 Download Excel",
            data=output.getvalue(),
            file_name="qas_wimt_matches.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Convert to CSV
        csv_data = st.session_state.matched_data.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name="qas_wimt_matches.csv",
            mime="text/csv"
        )

# Instructions
if st.session_state.qas_df is None or st.session_state.wimt_df is None:
    st.divider()
    st.subheader("How to use:")
    st.markdown("""
    <div class="instructions">
    
    ### 📋 **Step-by-Step Guide**
    
    1. **📤 Upload Files**: Upload both QAS and WIMT Excel files using the sidebar
    2. **🎯 Select Columns**: Choose one or more columns to compare from each file (you can select multiple columns)
    3. **⚙️ Configure Settings**: Set comparison options (case sensitivity, output format)
    4. **🔍 Find Matches**: Click the "Find Matches" button to compare the selected columns
    5. **💾 Download Results**: Download the matching results as Excel or CSV file
    
    ### 🔗 **Multi-column Comparison**
    When multiple columns are selected, the app will combine them to create a composite key for matching. For example, if you select columns A and B from both files, it will match rows where both A and B values are the same.
    
    ### ✅ **Result**
    The app will find all rows where the selected columns have matching values and create a new file with the results.
    
    </div>
    """, unsafe_allow_html=True)

# Footer with Atlas Copco Group branding
st.divider()
st.markdown("""
<div class="footer" style="background: linear-gradient(135deg, #054E5A 0%, #123F6D 100%); color: white; padding: 2rem; border-radius: 12px; text-align: center; margin-top: 3rem; box-shadow: 0 4px 12px rgba(5, 78, 90, 0.3);">
    <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <span style="font-size: 2rem;">🔄</span>
        <h3 style="margin: 0; color: #E1B77E; font-weight: bold;">QAS <-> WIMT Converter</h3>
    </div>
    <p style="margin: 0.5rem 0; font-size: 1.1rem; color: #CED9D7;">
        <strong>Atlas Copco Group</strong> | Data Comparison & Matching Tool
    </p>
    <p style="margin: 0; font-size: 0.9rem; color: #A1A9B4;">
        Built with ❤️ using Streamlit & Python | Professional Data Processing Solution
    </p>
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #5D7875;">
        <small style="color: #CED9D7;">
            Streamline your data comparison workflow with enterprise-grade reliability
        </small>
    </div>
</div>
""", unsafe_allow_html=True)
