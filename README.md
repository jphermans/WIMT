# 🔄 QAS <-> WIMT Converter

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**A powerful Streamlit application for comparing and matching data between QAS and WIMT Excel files**

[🚀 Quick Start](#-quick-start) • [📋 Features](#-features) • [🛠️ Installation](#️-installation) • [📖 Usage](#-usage) • [🤝 Contributing](#-contributing)

</div>

---

## 📋 Features

### 🎯 **Core Functionality**
- **📊 Excel File Processing**: Upload and process both `.xlsx` and `.xls` files
- **🔍 Multi-Column Comparison**: Select one or more columns from each file for flexible matching
- **🎛️ Customizable Settings**: Case-sensitive/insensitive comparisons and output options
- **📈 Real-time Preview**: View your data before processing
- **💾 Multiple Export Formats**: Download results as Excel or CSV files

### 🌟 **Advanced Features**
- **🔗 Composite Key Matching**: Combine multiple columns for complex comparisons
- **🎨 Interactive UI**: Clean, intuitive sidebar interface
- **⚡ Fast Processing**: Efficient pandas-based data processing
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔄 Session State Management**: Maintains data across interactions

---

## 🛠️ Installation

### Prerequisites
- 🐍 Python 3.8 or higher
- 📦 pip package manager

### 📥 Clone the Repository
```bash
git clone <repository-url>
cd WIMT
```

### 🔧 Install Dependencies
```bash
pip install -r requirements.txt
```

### 📋 Required Packages
- `streamlit>=1.28.0` - Web app framework
- `pandas>=1.5.0` - Data manipulation and analysis
- `openpyxl>=3.0.0` - Excel file reading/writing
- `xlrd>=2.0.0` - Excel file reading support

---

## 🚀 Quick Start

### 1️⃣ **Launch the Application**
```bash
python -m streamlit run scripts/main.py
```

### 2️⃣ **Access the Web Interface**
Open your browser and navigate to:
```
http://localhost:8501
```

### 3️⃣ **Start Comparing Files**
Follow the step-by-step process in the application!

---

## 📖 Usage

### 🔄 **Step-by-Step Process**

#### 📤 **Step 1: Upload Files**
<div align="center">
<img src="https://img.shields.io/badge/Upload-QAS%20File-blue?style=for-the-badge&logo=microsoft-excel" alt="Upload QAS">
<img src="https://img.shields.io/badge/Upload-WIMT%20File-green?style=for-the-badge&logo=microsoft-excel" alt="Upload WIMT">
</div>

- Use the sidebar to upload your QAS and WIMT Excel files
- Supported formats: `.xlsx`, `.xls`
- Files are automatically processed and previewed

#### 🎯 **Step 2: Select Columns**
<div align="center">
<img src="https://img.shields.io/badge/Select-QAS%20Columns-orange?style=for-the-badge&logo=table" alt="Select QAS Columns">
<img src="https://img.shields.io/badge/Select-WIMT%20Columns-purple?style=for-the-badge&logo=table" alt="Select WIMT Columns">
</div>

- Choose one or more columns from each file
- Multi-select dropdown for flexible selection
- Preview shows column headers and sample data

#### ⚙️ **Step 3: Configure Settings**
<div align="center">
<img src="https://img.shields.io/badge/Case-Sensitive-red?style=for-the-badge&logo=search" alt="Case Sensitive">
<img src="https://img.shields.io/badge/Include-All%20Columns-blue?style=for-the-badge&logo=columns" alt="Include All Columns">
</div>

- **Case Sensitivity**: Toggle case-sensitive matching
- **Output Options**: Include all columns or just selected ones

#### 🔍 **Step 4: Find Matches**
<div align="center">
<img src="https://img.shields.io/badge/Click-Find%20Matches-success?style=for-the-badge&logo=search" alt="Find Matches">
</div>

- Click the "Find Matches" button to start comparison
- Results appear in real-time
- Match count displayed

#### 💾 **Step 5: Download Results**
<div align="center">
<img src="https://img.shields.io/badge/Download-Excel-green?style=for-the-badge&logo=microsoft-excel" alt="Download Excel">
<img src="https://img.shields.io/badge/Download-CSV-blue?style=for-the-badge&logo=file-text" alt="Download CSV">
</div>

- Download as Excel (.xlsx) or CSV format
- Files named automatically with timestamp

---

## 🎨 **Interface Overview**

### 🎛️ **Sidebar Components**
| Component | Description | Icon |
|-----------|-------------|------|
| **File Upload** | Upload QAS and WIMT Excel files | 📤 |
| **Column Selection** | Multi-select dropdowns for columns | 🎯 |
| **Settings** | Comparison and output options | ⚙️ |
| **Find Matches** | Execute comparison process | 🔍 |

### 📊 **Main Content Areas**
| Section | Purpose | Features |
|---------|---------|----------|
| **File Previews** | Display uploaded data | 📋 First 10 rows, column info |
| **Results Table** | Show matching records | 📈 Sortable, scrollable |
| **Download Section** | Export options | 💾 Excel & CSV formats |

---

## 🔧 **Advanced Usage**

### 🔗 **Multi-Column Matching**
When multiple columns are selected, the app creates composite keys:
- **Example**: Columns A + B → Combined key "ValueA|ValueB"
- **Matching**: Finds rows where all selected columns match
- **Flexible**: Different column combinations for each file

### 📊 **Output Options**
1. **Include All Columns**: 
   - Merges complete rows from both files
   - Adds suffixes (_QAS, _WIMT) to distinguish sources
   
2. **Selected Columns Only**:
   - Shows only the columns used for comparison
   - Cleaner output for focused analysis

---

## 🎯 **Use Cases**

### 💼 **Business Applications**
- **📊 Data Reconciliation**: Compare datasets from different sources
- **🔍 Quality Assurance**: Identify matching records across systems
- **📈 Data Migration**: Verify data transfer accuracy
- **🔄 System Integration**: Match records between platforms

### 🏭 **Industry Examples**
- **🏦 Finance**: Reconcile transaction records
- **🏥 Healthcare**: Match patient data across systems
- **🛒 E-commerce**: Compare product catalogs
- **📚 Education**: Align student records

---

## 🚨 **Troubleshooting**

### ❗ **Common Issues**

#### 📁 **File Upload Problems**
```
❌ Error: File format not supported
✅ Solution: Use .xlsx or .xls files only
```

#### 🔍 **No Matches Found**
```
❌ Issue: 0 matches returned
✅ Check: Column data types and case sensitivity
✅ Verify: Selected columns contain comparable data
```

#### 💾 **Download Issues**
```
❌ Error: Download failed
✅ Solution: Ensure results exist before downloading
✅ Check: Browser download permissions
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 **Bug Reports**
- Use GitHub Issues
- Include error messages
- Provide sample data (anonymized)

### 💡 **Feature Requests**
- Describe the use case
- Explain expected behavior
- Consider implementation complexity

### 🔧 **Code Contributions**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Streamlit Team** for the amazing framework
- **Pandas Community** for powerful data processing tools
- **Contributors** who help improve this project

---

<div align="center">

### 🌟 **Star this repository if you find it helpful!** 🌟

**Made with ❤️ and Python**

[⬆️ Back to Top](#-qas---wimt-converter)

</div>
