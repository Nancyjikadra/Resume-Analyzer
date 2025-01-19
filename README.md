# Resume Analyzer

This project provides a tool to process multiple resumes (in PDF format) and extract relevant information, such as contact details, education, skills, and experience scores. The tool uses regular expressions to extract specific patterns from the resumes and calculates a total score based on various criteria.

## Requirements

Before running the code, ensure you have the following installed:

- Python 3.x
- Required Python libraries:
  - `os`
  - `re`
  - `pandas`
  - `PyPDF2`
  - `pathlib`
  - `tqdm`
  
You can install the necessary libraries using `pip`:

```bash
pip install pandas PyPDF2 tqdm
```

## Prerequisites

1. **Input Folder**: Create a folder named `resumes` in the same directory where the script is located. Place all your resume PDF files in this folder.
   
2. **Output Folder**: The script will automatically create an `output` folder to save the results in an Excel file named `resume_analysis.xlsx`.

## How to Use

1. Place your resume PDFs in the `resumes` folder.
2. Run the script using the following command:

```bash
python Resume_Analyzer.py
```

3. The script will process all the resumes in the `resumes` folder, extract the relevant details, calculate scores, and save the results in an Excel file (`resume_analysis.xlsx`) inside the `output` folder.

### Input Folder Structure

```
/project-folder
    /resumes
        resume1.pdf
        resume2.pdf
        resume3.pdf
        ...
    /output
        resume_analysis.xlsx
    batch_resume_parser.py
```

## How It Works

The script performs the following tasks:

1. **Extract Text from PDFs**: It uses `PyPDF2` to extract text from each resume.
2. **Parse Contact Details**: The script identifies contact information such as email, phone number, etc.
3. **Extract Education Details**: It identifies the university, course, discipline, and grade (CGPA/Percentage).
4. **Identify Skills**: The script identifies key skills such as AI/ML, Gen AI, and general programming skills.
5. **Experience Scoring**: The script calculates experience scores based on the number of relevant keywords found in the resume.
6. **Supporting Information**: The script extracts additional information such as certifications, internships, and projects.
7. **Score Calculation**: It calculates a total score based on education, skills, experience, and supporting information.
8. **Save Results**: The results are saved in an Excel file (`resume_analysis.xlsx`), sorted by the total score.

## Output

The output will be an Excel file (`resume_analysis.xlsx`) containing the following columns:

- `Name`: The name of the resume (derived from the filename).
- `Contact Details`: Extracted contact information (email, phone, etc.).
- `University`: Extracted university name.
- `Year of Study`: Extracted year of study.
- `Course`: Extracted course name.
- `Discipline`: Extracted discipline.
- `CGPA/Percentage`: Extracted CGPA or percentage.
- `Key Skills`: List of extracted key skills.
- `Gen AI Experience Score`: Score for Gen AI experience.
- `AI/ML Experience Score`: Score for AI/ML experience.
- `Supporting Information`: Extracted supporting information (certifications, internships, projects).
- `Total Score`: The calculated total score based on the extracted information.

## Notes

- The script processes resumes in parallel for faster execution using `ThreadPoolExecutor`.
- The resumes are sorted by their total score in descending order before being saved to the output file.
- Ensure that the resumes are in PDF format and stored in the `resumes` folder.

## License

This project is licensed under the MIT License.
