import streamlit as st
import pandas as pd
import io
import re

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
if 'duplicate_analysis' not in st.session_state:
    st.session_state.duplicate_analysis = None

# Duplicate detection functions
def detect_serial_columns(df):
    """Detect columns that likely contain serial numbers"""
    serial_patterns = [
        r'serial', r'sn\b', r'serial_number', r'serialnumber', 
        r'serial_no', r'serialno', r'part_number', r'partnumber',
        r'item_number', r'itemnumber', r'asset_number', r'assetnumber'
    ]
    
    serial_columns = []
    for col in df.columns:
        col_lower = col.lower()
        for pattern in serial_patterns:
            if re.search(pattern, col_lower):
                serial_columns.append(col)
                break
    
    return serial_columns

def detect_model_qas_columns(df):
    """Detect columns that contain Model_QAS or similar"""
    model_patterns = [
        r'model_qas', r'modelqas', r'model', r'qas', 
        r'model_type', r'modeltype', r'product_model', r'productmodel'
    ]
    
    model_columns = []
    for col in df.columns:
        col_lower = col.lower()
        for pattern in model_patterns:
            if re.search(pattern, col_lower):
                model_columns.append(col)
                break
    
    return model_columns

def analyze_duplicates(df):
    """Analyze duplicates based on serial numbers and Model_QAS columns"""
    if df is None or df.empty:
        return None
    
    # Detect relevant columns
    serial_cols = detect_serial_columns(df)
    model_cols = detect_model_qas_columns(df)
    
    # If no relevant columns found, return empty analysis
    if not serial_cols and not model_cols:
        return {
            'has_duplicates': False,
            'duplicate_count': 0,
            'total_rows': len(df),
            'duplicate_percentage': 0.0,
            'duplicate_rows': pd.DataFrame(),
            'clean_data': df.copy(),
            'columns_used': [],
            'message': 'No serial number or Model_QAS columns detected for duplicate analysis.'
        }
    
    # Combine all relevant columns for duplicate detection
    duplicate_check_cols = serial_cols + model_cols
    
    # Remove duplicates from the list
    duplicate_check_cols = list(set(duplicate_check_cols))
    
    # Create a subset with only the relevant columns for duplicate checking
    if duplicate_check_cols:
        # Create composite key for duplicate detection
        df_temp = df.copy()
        
        # Handle missing values by converting to string
        composite_key_parts = []
        for col in duplicate_check_cols:
            if col in df_temp.columns:
                composite_key_parts.append(df_temp[col].fillna('').astype(str).str.lower())
        
        if composite_key_parts:
            # Create composite key
            df_temp['_duplicate_key'] = composite_key_parts[0]
            for part in composite_key_parts[1:]:
                df_temp['_duplicate_key'] = df_temp['_duplicate_key'] + '|' + part
            
            # Find duplicates
            duplicate_mask = df_temp.duplicated(subset=['_duplicate_key'], keep=False)
            duplicate_rows = df[duplicate_mask].copy()
            
            # Clean data (remove duplicates, keep first occurrence)
            clean_data = df_temp.drop_duplicates(subset=['_duplicate_key'], keep='first')
            clean_data = clean_data.drop('_duplicate_key', axis=1)
            
            # Calculate statistics
            duplicate_count = duplicate_mask.sum()
            total_rows = len(df)
            duplicate_percentage = (duplicate_count / total_rows * 100) if total_rows > 0 else 0
            
            return {
                'has_duplicates': duplicate_count > 0,
                'duplicate_count': duplicate_count,
                'total_rows': total_rows,
                'duplicate_percentage': duplicate_percentage,
                'duplicate_rows': duplicate_rows,
                'clean_data': clean_data,
                'columns_used': duplicate_check_cols,
                'message': f'Duplicate analysis completed using columns: {", ".join(duplicate_check_cols)}'
            }
    
    # Fallback if no valid columns found
    return {
        'has_duplicates': False,
        'duplicate_count': 0,
        'total_rows': len(df),
        'duplicate_percentage': 0.0,
        'duplicate_rows': pd.DataFrame(),
        'clean_data': df.copy(),
        'columns_used': [],
        'message': 'No valid columns found for duplicate analysis.'
    }

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
                    
                    # Perform duplicate analysis on the matched data
                    st.session_state.duplicate_analysis = analyze_duplicates(st.session_state.matched_data)
                    
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
    
    # Column selection for analysis
    analysis_column = st.selectbox(
        "Select a column to analyze:",
        options=st.session_state.matched_data.columns.tolist()
    )
    
    col3, col4 = st.columns([3, 1])
    
    with col3:
        # Display the dataframe with highlighting for the selected column
        st.dataframe(
            st.session_state.matched_data,
            use_container_width=True,
            column_config={
                analysis_column: st.column_config.Column(
                    analysis_column,
                    help=f"Selected column for analysis"
                )
            }
        )
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
    
    # Duplicate Analysis Section
    if st.session_state.duplicate_analysis is not None:
        st.divider()
        st.subheader("🔍 Duplicate Analysis")
        
        analysis = st.session_state.duplicate_analysis
        
        # Display analysis message
        st.info(analysis['message'])
        
        # Create metrics columns
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(
                label="Total Records",
                value=analysis['total_rows']
            )
        
        with metric_col2:
            st.metric(
                label="Duplicate Records",
                value=analysis['duplicate_count'],
                delta=f"-{analysis['duplicate_count']} duplicates" if analysis['has_duplicates'] else "No duplicates"
            )
        
        with metric_col3:
            st.metric(
                label="Clean Records",
                value=len(analysis['clean_data']),
                delta=f"{len(analysis['clean_data']) - analysis['total_rows']} after cleanup"
            )
        
        with metric_col4:
            st.metric(
                label="Duplicate %",
                value=f"{analysis['duplicate_percentage']:.1f}%"
            )
        
        # Show columns used for duplicate detection
        if analysis['columns_used']:
            st.write("**Columns used for duplicate detection:**")
            cols_display = ", ".join([f"`{col}`" for col in analysis['columns_used']])
            st.markdown(f"- {cols_display}")
        
        # Display duplicate records if any found
        if analysis['has_duplicates'] and not analysis['duplicate_rows'].empty:
            st.divider()
            
            # Create tabs for different views
            dup_tab1, dup_tab2, dup_tab3 = st.tabs(["🚨 Duplicate Records", "✅ Clean Data", "📊 Duplicate Patterns"])
            
            with dup_tab1:
                st.subheader(f"Duplicate Records ({len(analysis['duplicate_rows'])} rows)")
                st.warning(f"Found {analysis['duplicate_count']} duplicate records based on serial numbers and Model_QAS columns.")
                
                # Display duplicate records with highlighting
                st.dataframe(
                    analysis['duplicate_rows'],
                    use_container_width=True,
                    column_config={
                        col: st.column_config.Column(
                            col,
                            help=f"Duplicate detection column" if col in analysis['columns_used'] else None
                        ) for col in analysis['columns_used']
                    }
                )
                
                # Download duplicate records
                dup_csv = analysis['duplicate_rows'].to_csv(index=False)
                st.download_button(
                    label="📥 Download Duplicate Records",
                    data=dup_csv,
                    file_name="duplicate_records.csv",
                    mime="text/csv",
                    help="Download only the duplicate records for review"
                )
            
            with dup_tab2:
                st.subheader(f"Clean Data ({len(analysis['clean_data'])} rows)")
                st.success(f"Clean dataset with duplicates removed (kept first occurrence of each duplicate).")
                
                # Display clean data
                st.dataframe(
                    analysis['clean_data'],
                    use_container_width=True
                )
                
                # Download clean data
                clean_output = io.BytesIO()
                with pd.ExcelWriter(clean_output, engine='openpyxl') as writer:
                    analysis['clean_data'].to_excel(writer, sheet_name='Clean_Data', index=False)
                clean_output.seek(0)
                
                col_clean1, col_clean2 = st.columns(2)
                
                with col_clean1:
                    st.download_button(
                        label="📥 Download Clean Excel",
                        data=clean_output.getvalue(),
                        file_name="qas_wimt_clean_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        help="Download clean data without duplicates as Excel file"
                    )
                
                with col_clean2:
                    clean_csv = analysis['clean_data'].to_csv(index=False)
                    st.download_button(
                        label="📄 Download Clean CSV",
                        data=clean_csv,
                        file_name="qas_wimt_clean_data.csv",
                        mime="text/csv",
                        help="Download clean data without duplicates as CSV file"
                    )
            
            with dup_tab3:
                st.subheader("Duplicate Patterns Analysis")
                
                if analysis['columns_used']:
                    # Analyze patterns in duplicate data
                    dup_df = analysis['duplicate_rows']
                    
                    # Create composite key for grouping duplicates
                    if len(analysis['columns_used']) > 0:
                        # Show duplicate groups
                        st.write("**Duplicate Groups:**")
                        
                        # Create a composite key to group duplicates
                        composite_parts = []
                        for col in analysis['columns_used']:
                            if col in dup_df.columns:
                                composite_parts.append(dup_df[col].fillna('').astype(str))
                        
                        if composite_parts:
                            composite_key = composite_parts[0]
                            for part in composite_parts[1:]:
                                composite_key = composite_key + ' | ' + part
                            
                            # Count occurrences of each duplicate pattern
                            duplicate_counts = composite_key.value_counts()
                            
                            # Display top duplicate patterns
                            st.write(f"Top {min(10, len(duplicate_counts))} most common duplicate patterns:")
                            
                            pattern_data = []
                            for pattern, count in duplicate_counts.head(10).items():
                                pattern_data.append({
                                    'Pattern': pattern,
                                    'Occurrences': count,
                                    'Percentage': f"{(count / len(dup_df) * 100):.1f}%"
                                })
                            
                            pattern_df = pd.DataFrame(pattern_data)
                            st.dataframe(pattern_df, use_container_width=True)
                            
                            # Visualize duplicate patterns
                            if len(duplicate_counts) > 1:
                                st.bar_chart(duplicate_counts.head(10))
                else:
                    st.info("No specific columns were used for duplicate detection.")
        
        else:
            st.success("🎉 No duplicates found! Your data is clean.")
            
            # Still offer download of the original data
            st.divider()
            st.subheader("Download Original Data")
            
            original_output = io.BytesIO()
            with pd.ExcelWriter(original_output, engine='openpyxl') as writer:
                st.session_state.matched_data.to_excel(writer, sheet_name='Original_Data', index=False)
            
            col_orig1, col_orig2 = st.columns(2)
            
            with col_orig1:
                st.download_button(
                    label="📥 Download Original Excel",
                    data=original_output.getvalue(),
                    file_name="qas_wimt_original_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col_orig2:
                original_csv = st.session_state.matched_data.to_csv(index=False)
                st.download_button(
                    label="📄 Download Original CSV",
                    data=original_csv,
                    file_name="qas_wimt_original_data.csv",
                    mime="text/csv"
                )
    
    # Column Value Analysis Section
    if analysis_column:
        st.divider()
        st.subheader(f"Analysis of '{analysis_column}'")
        
        # Get value counts for the selected column
        value_counts = st.session_state.matched_data[analysis_column].value_counts()
        value_percent = st.session_state.matched_data[analysis_column].value_counts(normalize=True) * 100
        
        # Determine if we need to limit the display (if too many unique values)
        unique_count = st.session_state.matched_data[analysis_column].nunique()
        if unique_count > 10:
            show_top_n = st.slider("Number of top values to display:", min_value=5, max_value=min(50, unique_count), value=10)
            display_counts = value_counts.nlargest(show_top_n)
            display_percent = value_percent.nlargest(show_top_n)
        else:
            display_counts = value_counts
            display_percent = value_percent
        
        # Create visualization tabs for different chart types
        chart_tab1, chart_tab2, chart_tab3 = st.tabs(["Bar Chart", "Pie Chart", "Time Series (if applicable)"])
        
        with chart_tab1:
            st.bar_chart(display_counts)
            
            # Add a download button for the chart data
            chart_data = pd.DataFrame({
                'Value': display_counts.index,
                'Count': display_counts.values,
                'Percentage': display_percent.values
            })
            csv = chart_data.to_csv(index=False)
            st.download_button(
                label="Download Chart Data",
                data=csv,
                file_name=f"{analysis_column}_distribution.csv",
                mime="text/csv"
            )
        
        with chart_tab2:
            # Create a pie chart using Plotly if available, otherwise use a workaround
            try:
                import plotly.express as px
                fig = px.pie(
                    values=display_counts.values,
                    names=display_counts.index,
                    title=f"Distribution of {analysis_column}"
                )
                # Use Atlas Copco colors
                fig.update_traces(
                    marker=dict(
                        colors=['#054E5A', '#E1B77E', '#A1A9B4', '#5D7875', '#CED9D7', '#123F6D'] * 10
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            except ImportError:
                # Fallback if plotly is not available
                st.write("Percentage Distribution:")
                for value, percentage in zip(display_percent.index, display_percent.values):
                    st.write(f"- **{value}**: {percentage:.2f}%")
                st.info("Install plotly for interactive pie charts: `pip install plotly`")
        
        with chart_tab3:
            # Check if the column might contain date information
            is_date = False
            if pd.api.types.is_datetime64_any_dtype(st.session_state.matched_data[analysis_column]):
                is_date = True
            elif 'date' in analysis_column.lower() or 'time' in analysis_column.lower():
                try:
                    # Try to convert to datetime
                    date_series = pd.to_datetime(st.session_state.matched_data[analysis_column])
                    is_date = True
                    # Create a temporary column with the converted dates
                    st.session_state.matched_data['_temp_date'] = date_series
                except:
                    is_date = False
            
            if is_date:
                # Group by date and count
                if '_temp_date' in st.session_state.matched_data.columns:
                    time_series = st.session_state.matched_data['_temp_date'].dt.date.value_counts().sort_index()
                    # Remove temporary column
                    st.session_state.matched_data = st.session_state.matched_data.drop('_temp_date', axis=1)
                else:
                    time_series = st.session_state.matched_data[analysis_column].dt.date.value_counts().sort_index()
                
                # Convert to DataFrame for better display
                time_df = pd.DataFrame(time_series)
                time_df.columns = ['Count']
                st.line_chart(time_df)
            else:
                st.info("This column doesn't appear to contain date/time data.")
        
        # Interactive Filtering
        st.divider()
        st.subheader("Interactive Filtering")
        
        # Get unique values for the selected column
        unique_values = st.session_state.matched_data[analysis_column].dropna().unique().tolist()
        
        # Allow user to select values to filter by
        filter_values = st.multiselect(
            f"Filter results where {analysis_column} equals:",
            options=unique_values
        )
        
        if filter_values:
            # Filter the dataframe
            filtered_df = st.session_state.matched_data[st.session_state.matched_data[analysis_column].isin(filter_values)]
            
            # Show the filtered results
            st.subheader(f"Filtered Results ({len(filtered_df)} rows)")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                column_config={
                    analysis_column: st.column_config.Column(
                        analysis_column,
                        help=f"Filtered by selected values"
                    )
                }
            )
            
            # Add download option for filtered results
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download Filtered Results",
                data=csv,
                file_name=f"filtered_{analysis_column}.csv",
                mime="text/csv"
            )
        
        # Multiple Column Comparison
        st.divider()
        st.subheader("Multi-Column Comparison")
        
        # Allow selecting multiple columns for comparison
        multi_column_analysis = st.checkbox("Compare with other columns")
        
        if multi_column_analysis:
            # Get all columns except the already selected one
            other_columns = [col for col in st.session_state.matched_data.columns if col != analysis_column]
            
            comparison_columns = st.multiselect(
                "Select columns to compare with:",
                options=other_columns
            )
            
            if comparison_columns:
                # Add the primary analysis column to the list
                all_columns = [analysis_column] + comparison_columns
                
                # Create a comparison dataframe with value counts for each selected column
                comparison_data = {}
                for col in all_columns:
                    # Get top 10 values for each column
                    top_values = st.session_state.matched_data[col].value_counts().nlargest(10)
                    # Convert index to string to avoid type comparison issues
                    top_values.index = top_values.index.map(str)
                    comparison_data[col] = top_values
                
                # Create a DataFrame for display with string index
                comparison_df = pd.DataFrame(comparison_data).fillna(0)
                
                # Display comparison table
                st.subheader("Value Count Comparison")
                st.dataframe(comparison_df, use_container_width=True)
                
                # Create a grouped bar chart
                st.subheader("Visual Comparison")
                st.bar_chart(comparison_df)
                
                # Add download option for comparison data
                csv = comparison_df.to_csv()
                st.download_button(
                    label="Download Comparison Data",
                    data=csv,
                    file_name="column_comparison.csv",
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
    5. **🔍 Duplicate Analysis**: Automatically checks for duplicates based on serial numbers and Model_QAS columns
    6. **💾 Download Results**: Download matching results, clean data, or duplicate records as Excel or CSV files
    
    ### 🔗 **Multi-column Comparison**
    When multiple columns are selected, the app will combine them to create a composite key for matching. For example, if you select columns A and B from both files, it will match rows where both A and B values are the same.
    
    ### 🚨 **Duplicate Detection**
    After finding matches, the app automatically analyzes the results for duplicates based on:
    - **Serial Numbers**: Columns containing "serial", "SN", "part_number", etc.
    - **Model_QAS**: Columns containing "model_qas", "model", "qas", etc.
    
    The duplicate analysis provides:
    - **Statistics**: Total records, duplicate count, and percentage
    - **Clean Data**: Dataset with duplicates removed (keeping first occurrence)
    - **Duplicate Records**: Only the duplicate entries for review
    - **Pattern Analysis**: Most common duplicate patterns and visualizations
    
    ### ✅ **Result**
    The app will find all rows where the selected columns have matching values, check for duplicates, and provide multiple download options for clean or original data.
    
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
