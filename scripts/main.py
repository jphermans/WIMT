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

# Main title
st.title("QAS <-> WIMT Converter")

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
    1. **Upload Files**: Upload both QAS and WIMT Excel files using the sidebar
    2. **Select Columns**: Choose one or more columns to compare from each file (you can select multiple columns)
    3. **Configure Settings**: Set comparison options (case sensitivity, output format)
    4. **Find Matches**: Click the "Find Matches" button to compare the selected columns
    5. **Download Results**: Download the matching results as Excel or CSV file
    
    **Multi-column comparison**: When multiple columns are selected, the app will combine them to create a composite key for matching. For example, if you select columns A and B from both files, it will match rows where both A and B values are the same.
    
    The app will find all rows where the selected columns have matching values and create a new file with the results.
    """)

# Footer
st.divider()
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>QAS <-> WIMT Converter | Built with Streamlit</small>
    </div>
    """,
    unsafe_allow_html=True
)
