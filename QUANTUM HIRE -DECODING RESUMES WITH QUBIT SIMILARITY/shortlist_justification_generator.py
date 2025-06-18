import os
import json
import random
from pathlib import Path
from typing import List, Dict, Union
from datetime import datetime
import PyPDF2  # For PDF text extraction
from pdfminer.high_level import extract_text  # Alternative PDF text extraction

class ShortlistJustificationGenerator:
    def __init__(self):
        # Skill importance levels
        self.skill_importance = {
            'python': 'critical',
            'aws': 'high',
            'machine learning': 'high',
            'ml': 'high',
            'react': 'medium',
            'react.js': 'medium',
            'devops': 'medium',
            'data analysis': 'medium',
            'docker': 'low',
            'kubernetes': 'low',
            'k8s': 'low',
            'c++': 'high',
            'cpp': 'high',
            'java': 'high'  # Java importance
        }
        
        # Positive phrases for matches
        self.match_phrases = {
            'critical': ["exceptional skills in", "expert-level knowledge of", "deep expertise in"],
            'high': ["strong experience with", "proficient in", "substantial background in"],
            'medium': ["working knowledge of", "demonstrated skills in", "experience with"],
            'low': ["familiarity with", "exposure to", "basic knowledge of"]
        }
        
        # Negative phrases for missing skills
        self.missing_phrases = {
            'critical': ["lacks required expertise in", "missing critical skills in", "no demonstrated experience with"],
            'high': ["limited experience with", "missing important skills in", "needs development in"],
            'medium': ["could improve in", "would benefit from more experience in", "has some gaps in"],
            'low': ["limited exposure to", "could gain familiarity with", "has minimal experience with"]
        }
        
        # Adjusted decision thresholds
        self.thresholds = {
            'auto_shortlist': 2,  # Lowered from 4
            'consider': 1,        # Lowered from 2
            'reject': 0
        }
        
        # Expanded skill aliases
        self.skill_aliases = {
            'py': 'python',
            'python3': 'python',
            'python2': 'python',
            'cplusplus': 'c++',
            'cpp': 'c++',
            'java8': 'java',
            'java11': 'java',
            'j2ee': 'java',
            'pandas': 'python',
            'numpy': 'python',
            'django': 'python',
            'flask': 'python',
            'spring': 'java',
            'hibernate': 'java',
            'tensorflow': 'machine learning',
            'pytorch': 'machine learning',
            'scikit-learn': 'machine learning',
            'reactjs': 'react',
            'aws cloud': 'aws',
            'amazon web services': 'aws'
        }

    def normalize_skill_name(self, skill: str) -> str:
        """Convert skill names to standard form"""
        skill = skill.lower().strip()
        return self.skill_aliases.get(skill, skill)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file using PyPDF2"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""  # Handle None returns
                return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {str(e)}")
            return ""

    def extract_skills_from_pdf(self, pdf_path: str) -> List[str]:
        """Extract skills from a PDF resume"""
        text = self.extract_text_from_pdf(pdf_path)
        return self.extract_skills_from_text(text)

    def extract_skills_from_text(self, text: str) -> List[str]:
        """Improved skill extraction from resume text"""
        text = text.lower()
        found_skills = []
        
        # Check for both explicit mentions and related terms
        for skill in self.skill_importance.keys():
            # Check standard name
            if skill in text:
                found_skills.append(skill)
                continue
                
            # Check aliases
            for alias, canonical in self.skill_aliases.items():
                if alias in text and canonical == skill:
                    found_skills.append(skill)
                    break
        
        return list(set(found_skills))  # Remove duplicates

    def calculate_candidate_score(self, candidate_skills: List[str], required_skills: List[str]) -> Dict[str, Union[int, List[str]]]:
        """Calculate a candidate's score based on skill matches"""
        candidate_skills = [self.normalize_skill_name(s) for s in candidate_skills]
        required_skills = [self.normalize_skill_name(s) for s in required_skills]
        
        matched_skills = []
        missing_skills = []
        score = 0
        
        for skill in required_skills:
            if skill in candidate_skills:
                matched_skills.append(skill)
                importance = self.skill_importance.get(skill, 'medium')
                score += {'critical': 3, 'high': 2, 'medium': 1, 'low': 0.5}[importance]
            else:
                missing_skills.append(skill)
        
        # Add partial credit for related skills
        for skill in candidate_skills:
            if skill in self.skill_aliases.values() and skill not in matched_skills:
                score += 0.3  # Small bonus for related skills
        
        return {
            'score': score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills
        }

    def generate_justification(self, candidate_name: str, candidate_skills: List[str], required_skills: List[str]) -> Dict[str, Union[str, int, List[str]]]:
        """Generate complete justification for a candidate"""
        result = self.calculate_candidate_score(candidate_skills, required_skills)
        score = result['score']
        matched = result['matched_skills']
        missing = result['missing_skills']
        
        # Generate positive justification parts
        positive_parts = []
        for skill in matched:
            importance = self.skill_importance.get(skill, 'medium')
            phrase = random.choice(self.match_phrases[importance])
            positive_parts.append(f"{phrase} {skill}")
        
        # Generate negative justification parts
        negative_parts = []
        for skill in missing:
            importance = self.skill_importance.get(skill, 'medium')
            phrase = random.choice(self.missing_phrases[importance])
            negative_parts.append(f"{phrase} {skill}")
        
        # Determine recommendation
        if score >= self.thresholds['auto_shortlist']:
            recommendation = "Strong Shortlist"
            decision = "shortlisted"
        elif score >= self.thresholds['consider']:
            recommendation = "Consider with Reservations"
            decision = "considered"
        else:
            recommendation = "Not Recommended"
            decision = "not recommended"
        
        # Generate final justification text
        justification_parts = []
        
        if positive_parts:
            justification_parts.append(f"{candidate_name} is {decision} due to {self._join_phrases(positive_parts)}")
        
        if negative_parts:
            justification_parts.append(f"However, they have {self._join_phrases(negative_parts)}")
        
        if not positive_parts and not negative_parts:
            justification_parts.append(f"{candidate_name} has no significant matching skills for this position")
        
        # Normalize score to 0-10 scale
        normalized_score = min(10, max(0, score * 2))  # Scale from 0-5 to 0-10
        justification = " ".join(justification_parts) + f". Overall score: {normalized_score:.1f}/10"
        
        return {
            'candidate_name': candidate_name,
            'justification': justification,
            'recommendation': recommendation,
            'score': normalized_score,
            'matched_skills': matched,
            'missing_skills': missing
        }

    def _join_phrases(self, phrases: List[str]) -> str:
        """Join phrases in a human-readable way"""
        if len(phrases) == 1:
            return phrases[0]
        elif len(phrases) == 2:
            return f"{phrases[0]} and {phrases[1]}"
        else:
            return ", ".join(phrases[:-1]) + f", and {phrases[-1]}"

    def process_pdf_resumes(self, pdf_dir: str, required_skills: List[str]) -> Dict[str, Dict]:
        """Process all PDF resumes in a directory"""
        pdf_dir = Path(pdf_dir)
        results = {}
        
        for pdf_file in pdf_dir.glob("*.pdf"):
            candidate_name = pdf_file.stem.replace('_', ' ').title()
            skills = self.extract_skills_from_pdf(str(pdf_file))
            results[candidate_name] = self.generate_justification(candidate_name, skills, required_skills)
        
        return results

    def generate_report(self, justification_data: Dict, output_dir: Union[str, Path] = "outputs/shortlist_justifications") -> str:
        """Generate a formatted report file"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{justification_data['candidate_name'].replace(' ', '_')}_justification.txt"
        filepath = output_dir / filename
        
        report_content = [
            f"Candidate Evaluation Report",
            "=" * 40,
            f"Candidate: {justification_data['candidate_name']}",
            f"Recommendation: {justification_data['recommendation']}",
            f"Score: {justification_data['score']:.1f}/10",
            "\nJustification:",
            justification_data['justification'],
            "\nMatched Skills:",
            ", ".join(justification_data['matched_skills']) if justification_data['matched_skills'] else "None",
            "\nMissing Skills:",
            ", ".join(justification_data['missing_skills']) if justification_data['missing_skills'] else "None",
            "\nGenerated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_content))
        
        return str(filepath)


if __name__ == "__main__":
    # Example usage with PDF resumes
    generator = ShortlistJustificationGenerator()
    
    # Get required skills from user
    required_skills = input("Enter required skills (comma separated): ").strip().split(',')
    required_skills = [skill.strip() for skill in required_skills if skill.strip()]
    
    if not required_skills:
        print("Error: Please enter at least one required skill")
        exit()
    
    # Process all PDF resumes in the specified directory
    pdf_directory = "data/resumes"  # Directory containing PDF resumes
    if not os.path.exists(pdf_directory):
        print(f"Error: Directory '{pdf_directory}' not found")
        exit()
    
    results = generator.process_pdf_resumes(pdf_directory, required_skills)
    
    # Generate reports
    output_dir = "outputs/shortlist_justifications"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n=== Results ===")
    for candidate_name, data in results.items():
        report_path = generator.generate_report(data, output_dir)
        print(f"\n{candidate_name}: {data['recommendation']} (Score: {data['score']:.1f}/10)")
        print(data['justification'])
    
    print(f"\nAll reports saved to {output_dir}")
