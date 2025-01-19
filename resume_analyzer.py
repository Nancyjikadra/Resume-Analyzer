import os
import re
import pandas as pd
import PyPDF2
from pathlib import Path
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

class BatchResumeParser:
    def __init__(self):
        self.patterns = {
            'contact': r'(?:e?[,-]?mail|contact|phone|mobile|tel|e-mail)(?:[:\s]+)?([^"\n\r\t]*)',
            'year': r'20[12]\d',
            'cgpa': r'(?:cgpa|gpa)[:\s]*([0-9.]+)(?:/[0-9.]+)?',
            'percentage': r'([0-9]{2,3})(?:\.[0-9]+)?%'
        }
        
        self.skills_patterns = {
            'gen_ai': [
                'llm', 'chatgpt', 'gpt-4', 'claude', 'anthropic', 'transformers',
                'langchain', 'llamaindex', 'vector database', 'embeddings',
                'prompt engineering', 'rag', 'semantic search'
            ],
            'ai_ml': [
                'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'machine learning',
                'deep learning', 'neural networks', 'computer vision', 'nlp',
                'natural language processing', 'pandas', 'numpy', 'opencv'
            ],
            'general': [
                'python', 'java', 'javascript', 'sql', 'aws', 'azure',
                'docker', 'kubernetes', 'react', 'node.js', 'html', 'css'
            ]
        }

        self.edu_patterns = {
            'year': r'\b(19|20)\d{2}\b',  # Matches years like 1990, 2020
            'cgpa': r'\b([0-9]\.[0-9]{1,2})/10\b',  # Matches CGPA like 8.5/10
            'percentage': r'\b([0-9]{1,2}(?:\.[0-9]{1,2})?)%\b',  # Matches percentage like 85%
            'university': r'(?:university|institute|IIT|NIT|college)[:\s]+([^"\n\r\t]*)'
        }


    def extract_text(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = []
                for page in reader.pages:
                    text.append(page.extract_text())
                return '\n'.join(text).lower()
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return ''

    def extract_education_details(self, text: str) -> Dict[str, str]:
        edu_details = {
            'university': '',
            'year': '',
            'course': '',
            'discipline': '',
            'grade': '',
            'grade_value': 0.0  # Added for score calculation
        }

        # Extract university
        uni_pattern = r'\b(?:[A-Za-z]*\s)?(?:IIT|NIT|SVNIT|[A-Za-z]+ University|Institute of Technology|College)\b'
        uni_match = re.findall(uni_pattern, text, re.IGNORECASE)
        if uni_match:
            # Remove any year patterns from the university name
            university_name = max(uni_match, key=len).strip()
            edu_details['university'] = university_name

        # Extract year
        year_match = re.search(self.edu_patterns['year'], text)
        if year_match:
            edu_details['year'] = year_match.group(0)

        # Extract course and discipline
        courses = {
            'b.tech': 'Bachelor of Technology',
            'b.e': 'Bachelor of Engineering',
            'm.tech': 'Master of Technology',
            'bca': 'Bachelor of Computer Applications',
            'mca': 'Master of Computer Applications',
            'ph.d': 'Doctor of Philosophy'
        }

        disciplines = [
            'computer science', 'information technology', 'electronics',
            'mechanical', 'electrical', 'civil', 'computer engineering',
            'data science', 'artificial intelligence'
        ]

        for abbr, full in courses.items():
            if abbr in text.lower():
                edu_details['course'] = full
                break

        for discipline in disciplines:
            if discipline in text.lower():
                edu_details['discipline'] = discipline.title()
                break

        # Extract CGPA/Percentage
        cgpa_match = re.search(self.edu_patterns['cgpa'], text)
        percentage_match = re.search(self.edu_patterns['percentage'], text)

        if cgpa_match:
            cgpa_value = float(cgpa_match.group(1))
            edu_details['grade'] = f"CGPA: {cgpa_value}/10"
            edu_details['grade_value'] = cgpa_value
        elif percentage_match:
            percentage_value = float(percentage_match.group(1))
            edu_details['grade'] = f"{percentage_value}%"
            edu_details['grade_value'] = percentage_value / 10

        return edu_details


    def extract_skills(self, text: str) -> List[str]:
        all_skills = []
        for category, skills in self.skills_patterns.items():
            for skill in skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', text):
                    all_skills.append(skill)
        return list(set(all_skills))

    def calculate_experience_score(self, text: str, category: str) -> int:
        score = 0
        keywords = self.skills_patterns[category]
        matches = sum(1 for keyword in keywords if re.search(r'\b' + re.escape(keyword) + r'\b', text))
        
        if matches >= 4:
            score = 3  # Advanced
        elif matches >= 2:
            score = 2  # Intermediate
        elif matches >= 1:
            score = 1  # Basic
            
        return score

    def extract_supporting_info(self, text: str) -> str:
        info = []
        
        # Look for certifications
        cert_pattern = r'(?:certification|certified|certificate)[:\s]+([^"\n\r\t]*)'
        certs = re.finditer(cert_pattern, text, re.IGNORECASE)
        for cert in certs:
            info.append(f"Certification: {cert.group(1).strip()}")

        # Look for internships
        intern_pattern = r'(?:internship|intern)[:\s]+([^"\n\r\t]*)'
        internships = re.finditer(intern_pattern, text, re.IGNORECASE)
        for internship in internships:
            info.append(f"Internship: {internship.group(1).strip()}")

        # Look for projects
        project_pattern = r'(?:project|developed|implemented)[:\s]+([^"\n\r\t]*)'
        projects = re.finditer(project_pattern, text, re.IGNORECASE)
        for project in projects:
            info.append(f"Project: {project.group(1).strip()}")

        return ' | '.join(info[:5])  # Limit to top 5 items

    def calculate_total_score(self, skills: List[str], education: Dict[str, str], 
                            gen_ai_score: int, ai_ml_score: int, 
                            supporting_info: str) -> int:
        score = 0
        
        # Education Score (25 points)
        if education['university']:
            score += 10  # Having a recognized university
        if education['course']:
            score += 5   # Having a relevant course
        if education['grade_value'] > 0:
            grade_score = min(education['grade_value'], 10)  # Max 10 points for grades
            score += grade_score

        # Skills Score (25 points)
        skill_score = len(skills) * 2  # 2 points per skill
        score += min(skill_score, 25)  # Cap at 25 points

        # Experience Scores (40 points)
        gen_ai_points = gen_ai_score * 10  # Up to 30 points
        ai_ml_points = ai_ml_score * 10    # Up to 30 points
        score += min(gen_ai_points + ai_ml_points, 40)  # Cap at 40 points

        # Supporting Information (10 points)
        if supporting_info:
            info_count = len(supporting_info.split('|'))
            info_score = info_count * 2  # 2 points per item
            score += min(info_score, 10)  # Cap at 10 points

        return round(score)

    def parse_single_resume(self, pdf_path: Path) -> Dict[str, Any]:
        text = self.extract_text(str(pdf_path))
        if not text:
            return {}

        # Extract all information
        contact_matches = re.finditer(self.patterns['contact'], text)
        contact_details = ' | '.join(match.group(1).strip() for match in contact_matches if match.group(1).strip())
        education = self.extract_education_details(text)
        skills = self.extract_skills(text)
        gen_ai_score = self.calculate_experience_score(text, 'gen_ai')
        ai_ml_score = self.calculate_experience_score(text, 'ai_ml')
        supporting_info = self.extract_supporting_info(text)
        
        # Calculate total score
        total_score = self.calculate_total_score(
            skills, education, gen_ai_score, ai_ml_score, supporting_info
        )

        return {
            'Name': pdf_path.stem,
            'Contact Details': contact_details,
            'University': education['university'],
            'Year of Study': education['year'],
            'Course': education['course'],
            'Discipline': education['discipline'],
            'CGPA/Percentage': education['grade'],
            'Key Skills': ', '.join(skills),
            'Gen AI Experience Score': gen_ai_score,
            'AI/ML Experience Score': ai_ml_score,
            'Supporting Information': supporting_info,
            'Total Score': total_score
        }

    def process_resumes(self, folder_path: str, output_file: str):
        """Process multiple resumes in parallel"""
        pdf_files = list(Path(folder_path).glob('*.pdf'))
        results = []
        
        # Process resumes in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=min(10, len(pdf_files))) as executor:
            future_to_pdf = {executor.submit(self.parse_single_resume, pdf_file): pdf_file 
                           for pdf_file in pdf_files}
            
            # Show progress bar
            with tqdm(total=len(pdf_files), desc="Processing Resumes") as pbar:
                for future in as_completed(future_to_pdf):
                    pdf_file = future_to_pdf[future]
                    try:
                        result = future.result()
                        if result:
                            results.append(result)
                    except Exception as e:
                        print(f"Error processing {pdf_file}: {e}")
                    pbar.update(1)

        # Save results to Excel
        if results:
            df = pd.DataFrame(results)
            # Sort by Total Score in descending order
            df = df.sort_values('Total Score', ascending=False)
            df.to_excel(output_file, index=False)
            print(f"\nResults saved to {output_file}")
            print(f"Successfully processed {len(results)} resumes")
        else:
            print("No results to save")

def main():
    # Create directories
    os.makedirs("resumes", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Initialize parser and process resumes
    parser = BatchResumeParser()
    parser.process_resumes(
        folder_path="resumes",
        output_file="output/resume_analysis.xlsx"
    )

if __name__ == "__main__":
    main()
