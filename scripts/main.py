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
    /* Light Mode (Default) */
    body {
        --atlas-teal: #054E5A;
        --atlas-white: #FFFFFF;
        --atlas-gray: #A1A9B4;
        --atlas-gold: #E1B77E;
        --accent-green: #5D7875;
        --accent-light-green: #CED9D7;
        --accent-blue: #123F6D;
        
        /* Text colors */
        --text-primary: #054E5A;
        --text-secondary: #333333;
        --text-on-dark: #FFFFFF;
        --text-on-light: #054E5A;
        
        /* Background colors */
        --bg-primary: #FFFFFF;
        --bg-secondary: #CED9D7;
        --bg-accent: #054E5A;
    }
    
    /* Dark Mode */
    body.dark-mode {
        --atlas-teal: #1A7D8C; /* Lighter teal for better contrast */
        --atlas-white: #FFFFFF;
        --atlas-gray: #B8C0CC; /* Lighter gray */
        --atlas-gold: #F0C794; /* Brighter gold */
        --accent-green: #7DA5A0; /* Lighter green */
        --accent-light-green: #2A3A38; /* Darker but still visible */
        --accent-blue: #2A5E94; /* Lighter blue */
        
        /* Text colors for dark mode */
        --text-primary: #E0E0E0;
        --text-secondary: #B0B0B0;
        --text-on-dark: #FFFFFF;
        --text-on-light: #1A7D8C;
        
        /* Background colors for dark mode */
        --bg-primary: #1E1E1E;
        --bg-secondary: #2D3748;
        --bg-accent: #1A7D8C;
        
        color-scheme: dark;
    }
    
    /* Force dark mode for specific elements */
    .dark-mode .stApp {
        background-color: #1E1E1E !important;
    }
    
    .dark-mode [data-testid="stHeader"] {
        background-color: #1E1E1E !important;
    }
    
    .dark-mode [data-testid="stToolbar"] {
        background-color: #2D3748 !important;
    }
    
    .dark-mode [data-testid="stSidebar"] {
        background-color: #2D3748 !important;
    }
    
    .dark-mode [data-testid="stSidebarUserContent"] {
        background-color: #2D3748 !important;
    }
    
    .dark-mode .main-content {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
    }
    
    .dark-mode h1, .dark-mode h2, .dark-mode h3, .dark-mode h4, .dark-mode h5, .dark-mode h6 {
        color: #E0E0E0 !important;
    }
    
    .dark-mode p, .dark-mode span, .dark-mode label, .dark-mode div {
        color: #E0E0E0 !important;
    }
    
    /* Main app background */
    .stApp {
        background-color: var(--bg-primary);
    }
    
    /* Main title styling */
    .main h1 {
        color: var(--text-primary) !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 1rem 0 !important;
        border-bottom: 3px solid var(--atlas-gold) !important;
        margin-bottom: 2rem !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--bg-secondary) !important;
    }
    
    .sidebar .sidebar-content {
        background-color: var(--bg-secondary) !important;
    }
    
    /* Sidebar headers */
    .sidebar h2, .sidebar h3 {
        color: var(--text-primary) !important;
        font-weight: bold !important;
    }
    
    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background-color: var(--atlas-teal) !important;
        border: none !important;
        color: var(--text-on-dark) !important;
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
        color: var(--text-on-light) !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: var(--atlas-teal) !important;
        color: var(--text-on-dark) !important;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background-color: var(--atlas-gold) !important;
        border: none !important;
        color: var(--text-on-light) !important;
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
        background-color: var(--bg-primary) !important;
        border: 2px dashed var(--atlas-teal) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background-color: var(--bg-primary) !important;
        border: 2px solid var(--atlas-teal) !important;
        border-radius: 8px !important;
    }
    
    /* Multiselect text */
    .stMultiSelect label, .stMultiSelect span {
        color: var(--text-primary) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: var(--text-primary) !important;
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
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        border-left: 5px solid var(--accent-blue) !important;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: var(--atlas-gold) !important;
        color: var(--text-on-light) !important;
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
        color: var(--text-primary) !important;
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
        color: var(--text-on-dark) !important;
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
        background-color: var(--bg-primary) !important;
        border: 2px solid var(--atlas-teal) !important;
        border-radius: 8px !important;
    }
    
    /* Sidebar multiselect */
    .sidebar .stMultiSelect > div > div {
        background-color: var(--bg-primary) !important;
        border: 2px solid var(--atlas-teal) !important;
    }
    
    /* Instructions section */
    .instructions {
        background-color: var(--accent-light-green) !important;
        padding: 1.5rem !important;
        border-radius: 8px !important;
        border-left: 5px solid var(--atlas-teal) !important;
        margin: 1rem 0 !important;
        color: var(--text-primary) !important;
    }
    
    .instructions h3 {
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--atlas-gold) !important;
        padding-bottom: 0.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    .instructions strong {
        color: var(--atlas-teal) !important;
    }
    
    /* Custom card styling */
    .custom-card {
        background-color: var(--bg-primary) !important;
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
        color: var(--text-primary) !important;
        font-weight: bold !important;
    }
    
    .stMetric div {
        color: var(--text-primary) !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title with custom styling
st.markdown('<h1 class="main-title">🔄 QAS <-> WIMT Converter</h1>', unsafe_allow_html=True)

# Add the main-title class to the CSS
st.markdown("""
<style>
.main-title {
    color: var(--text-primary) !important;
    text-align: center !important;
    font-weight: bold !important;
    padding: 1rem 0 !important;
    border-bottom: 3px solid var(--atlas-gold) !important;
    margin-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'qas_df' not in st.session_state:
    st.session_state.qas_df = None
if 'wimt_df' not in st.session_state:
    st.session_state.wimt_df = None
if 'matched_data' not in st.session_state:
    st.session_state.matched_data = None

# Check for dark mode preference in query params
dark_mode_param = st.query_params.get('dark_mode', 'false').lower() == 'true'

# Initialize dark mode state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = dark_mode_param

# Add JavaScript for direct dark mode control
st.markdown("""
<script>
// Function to apply dark mode
function applyDarkMode() {
    const doc = window.parent.document;
    const bodyEl = doc.body;
    
    // Add dark-mode class to body
    bodyEl.classList.add('dark-mode');
    
    // Apply dark mode to all Streamlit containers
    const containers = doc.querySelectorAll('[data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="stSidebarUserContent"]');
    containers.forEach(container => {
        container.classList.add('dark-mode');
    });
    
    // Store preference
    localStorage.setItem('atlas_dark_mode', 'true');
    
    // Force dark mode with direct styles
    const darkModeStyles = `
        body.dark-mode, 
        body.dark-mode [data-testid="stAppViewContainer"],
        body.dark-mode [data-testid="stHeader"],
        body.dark-mode [data-testid="stToolbar"],
        body.dark-mode [data-testid="stSidebar"],
        body.dark-mode [data-testid="stSidebarUserContent"] {
            background-color: #1E1E1E !important;
            color: #E0E0E0 !important;
        }
        
        body.dark-mode h1, 
        body.dark-mode h2, 
        body.dark-mode h3, 
        body.dark-mode h4, 
        body.dark-mode h5, 
        body.dark-mode h6,
        body.dark-mode p,
        body.dark-mode span,
        body.dark-mode label,
        body.dark-mode div {
            color: #E0E0E0 !important;
        }
        
        body.dark-mode [data-testid="stSidebar"] {
            background-color: #2D3748 !important;
        }
        
        body.dark-mode .stButton > button {
            background-color: #B8C0CC !important;
            color: #1A7D8C !important;
        }
        
        body.dark-mode .stButton > button[kind="primary"] {
            background-color: #1A7D8C !important;
            color: #FFFFFF !important;
        }
        
        body.dark-mode .stDownloadButton > button {
            background-color: #F0C794 !important;
            color: #1A7D8C !important;
        }
    `;
    
    // Add the styles to the document
    const style = document.createElement('style');
    style.textContent = darkModeStyles;
    doc.head.appendChild(style);
}

// Function to apply light mode
function applyLightMode() {
    const doc = window.parent.document;
    const bodyEl = doc.body;
    
    // Remove dark-mode class from body
    bodyEl.classList.remove('dark-mode');
    
    // Remove dark mode from all Streamlit containers
    const containers = doc.querySelectorAll('[data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="stSidebarUserContent"]');
    containers.forEach(container => {
        container.classList.remove('dark-mode');
    });
    
    // Store preference
    localStorage.setItem('atlas_dark_mode', 'false');
}

// Function to toggle dark mode
function toggleDarkMode(isDark) {
    if (isDark) {
        applyDarkMode();
    } else {
        applyLightMode();
    }
}

// Check for saved preference or URL parameter on page load
window.addEventListener('load', function() {
    // Check URL parameter first
    const urlParams = new URLSearchParams(window.location.search);
    const darkModeParam = urlParams.get('dark_mode');
    
    if (darkModeParam === 'true') {
        applyDarkMode();
        
        // Update the toggle state if needed
        setTimeout(function() {
            const darkModeToggle = window.parent.document.querySelector('button[kind="secondary"]:has(span:contains("Dark Mode"))');
            if (darkModeToggle && !darkModeToggle.classList.contains('toggled')) {
                darkModeToggle.click();
            }
        }, 500);
    } 
    // If no URL parameter, check localStorage
    else if (darkModeParam !== 'false') {
        const savedPreference = localStorage.getItem('atlas_dark_mode');
        
        if (savedPreference === 'true') {
            applyDarkMode();
            
            // Update the toggle state if needed
            setTimeout(function() {
                const darkModeToggle = window.parent.document.querySelector('button[kind="secondary"]:has(span:contains("Dark Mode"))');
                if (darkModeToggle && !darkModeToggle.classList.contains('toggled')) {
                    darkModeToggle.click();
                }
            }, 500);
        }
    }
    
    // Apply dark mode immediately if the toggle is already on
    setTimeout(function() {
        const darkModeToggle = window.parent.document.querySelector('button[kind="secondary"]:has(span:contains("Dark Mode"))');
        if (darkModeToggle && darkModeToggle.classList.contains('toggled')) {
            applyDarkMode();
        }
    }, 100);
});
</script>
""", unsafe_allow_html=True)

# Function to toggle dark mode
def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode
    # Set a flag to show the refresh message
    st.session_state.dark_mode_toggle_clicked = True
    
    # Update query params to persist dark mode setting
    st.query_params.update({'dark_mode': str(st.session_state.dark_mode).lower()})

# Apply dark mode based on session state with more direct styling
if st.session_state.dark_mode:
    # Add direct CSS for dark mode
    st.markdown("""
    <style>
    /* Direct dark mode styling */
    body, 
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarUserContent"] {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #E0E0E0 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #2D3748 !important;
    }
    
    .stButton > button {
        background-color: #B8C0CC !important;
        color: #1A7D8C !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #1A7D8C !important;
        color: #FFFFFF !important;
    }
    
    .stDownloadButton > button {
        background-color: #F0C794 !important;
        color: #1A7D8C !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Also use JavaScript
    st.markdown('<script>toggleDarkMode(true);</script>', unsafe_allow_html=True)
else:
    st.markdown('<script>toggleDarkMode(false);</script>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Dark mode toggle
    st.header("Display Settings")
    dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle", on_change=toggle_dark_mode)
    
    # Add a note about refreshing for dark mode changes
    if st.session_state.get('dark_mode_toggle_clicked', False):
        st.info("Theme changes applied! For complete theme application, please refresh the page.")
        # Add a refresh button
        if st.button("Refresh Page"):
            # Use the proper way to update query params for the refresh
            current_params = dict(st.query_params)
            current_params['dark_mode'] = str(st.session_state.dark_mode).lower()
            query_string = '&'.join([f"{k}={v}" for k, v in current_params.items()])
            
            st.markdown(f"""
            <script>
                window.parent.location.href = window.parent.location.pathname + '?{query_string}';
            </script>
            """, unsafe_allow_html=True)
            st.session_state.dark_mode_toggle_clicked = False
    
    st.divider()
    
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
    
    ### 🌓 **Display Settings**
    You can toggle between light and dark mode using the switch in the sidebar. The app will automatically detect your system preference, but you can manually override it at any time for better readability.
    
    </div>
    """, unsafe_allow_html=True)

# Add footer CSS
st.markdown("""
<style>
.app-footer {
    background: linear-gradient(135deg, var(--atlas-teal) 0%, var(--accent-blue) 100%);
    color: var(--text-on-dark);
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    margin-top: 3rem;
    box-shadow: 0 4px 12px rgba(5, 78, 90, 0.3);
}

.footer-title {
    margin: 0;
    color: var(--atlas-gold);
    font-weight: bold;
}

.footer-subtitle {
    margin: 0.5rem 0;
    font-size: 1.1rem;
    color: var(--accent-light-green);
}

.footer-text {
    margin: 0;
    font-size: 0.9rem;
    color: var(--atlas-gray);
}

.footer-divider {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--accent-green);
}

.footer-small {
    color: var(--accent-light-green);
}
</style>
""", unsafe_allow_html=True)

# Footer with Atlas Copco Group branding
st.divider()
st.markdown("""
<div class="app-footer">
    <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <span style="font-size: 2rem;">🔄</span>
        <h3 class="footer-title">QAS <-> WIMT Converter</h3>
    </div>
    <p class="footer-subtitle">
        <strong>Atlas Copco Group</strong> | Data Comparison & Matching Tool
    </p>
    <p class="footer-text">
        Built with ❤️ using Streamlit & Python | Professional Data Processing Solution
    </p>
    <div class="footer-divider">
        <small class="footer-small">
            Streamline your data comparison workflow with enterprise-grade reliability
        </small>
    </div>
</div>
""", unsafe_allow_html=True)
