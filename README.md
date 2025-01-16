# Generative AI-Powered Resume Analyzer

## 📖 About the Project
The Resume Analyzer is a Python-based application that uses Generative AI and Natural Language Processing (NLP) to automate resume screening. It extracts essential information, scores resumes based on AI/ML and Generative AI expertise, and outputs results in a structured Excel file.

### Key Features
- **Resume Parsing**: Extracts key details such as Name, Contact Information, Education, Key Skills, and more.
- **Experience Scoring**: Assigns scores for AI/ML and Generative AI expertise based on resume content.
- **Batch Processing**: Processes up to 100 resumes in a single batch.
- **Excel Output**: Generates a neatly formatted Excel file summarizing the analysis.

---

## 🛠 Installation

### Prerequisites
- Python 3.8 or higher
- Required Python packages

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install pandas openpyxl PyPDF2 openai tqdm
   ```

3. Download the `en_core_web_sm` model for spaCy:
   ```bash
   python -m spacy download en_core_web_sm
   ```

---

## 🚀 Usage

### Input
- Place the resumes (PDF format) in a folder named `resumes` within the project directory.

### Running the Application
1. Run the main script:
   ```bash
   python main.py
   ```

2. The results will be saved to an Excel file named `resume_analysis_results.xlsx` in the project directory.

---

## 🧩 Code Overview

### Main Components
1. **Resume Parsing**:
   - Extracts text from PDF resumes using `PyPDF2`.
   - Identifies contact details, education, and skills using regex and NLP.

2. **Experience Scoring**:
   - Assigns scores for Generative AI and AI/ML expertise based on predefined keywords.
   - Calculates an overall score using a weighted scoring mechanism.

3. **Batch Processing**:
   - Handles multiple resumes efficiently using multithreading.

4. **Excel Output**:
   - Saves results to an Excel file with auto-adjusted column widths for better readability.

---

## 📂 Folder Structure
```
project_directory/
├── resumes/                      # Folder containing input PDF resumes
├── main.py                       # Main script to run the analyzer
├── resume_processing.log         # Log file for tracking errors and progress
├── resume_analysis_results.xlsx  # Output Excel file
```

---

## 📊 Example Output
The generated Excel file contains the following columns:
- **Name**: Extracted from the file name.
- **Contact Details**: Includes email, phone, LinkedIn, GitHub, and portfolio links.
- **University, Year of Study, Course, Discipline, CGPA/Percentage**: Education details.
- **Key Skills**: Identified technical skills.
- **Gen AI Experience Score**: Score for Generative AI expertise (1-3).
- **AI/ML Experience Score**: Score for AI/ML expertise (1-3).
- **Supporting Information**: Certifications, internships, and projects.
- **Overall Score**: Calculated based on extracted data.

---

## 🛡 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
