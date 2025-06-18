 import os 
import json 
import sys 
import string
 from nltk.tokenize import word_tokenize 
from datetime import datetime
 from pathlib import Path
 from collections import defaultdict 
from typing import List
 import PyPDF2
 from src.team_comparison import TeamAnalyzer 
from src.skill_gap_analysis import SkillGapAnalyzer
 from src.quantum_similarity import QuantumResumeMatcher 
from src.resume_ranking import ResumeRanker
 from src.heatmap_visualizer import SkillHeatmapGenerator, get_skills_input
 from src.pro_radar import RadarVisualizer
 from src.learning_path import LearningPathGenerator
 from src.shortlist_justification_generator import ShortlistJustificationGenerator 
from src.report_generator import ReportGenerator
def extract_text_from_pdf(pdf_path):
 """Extract text content from PDF resume""" 
try:
 with open(pdf_path, 'rb') as f: 
reader = PyPDF2.PdfReader(f) 
text = ""
 for page in reader.pages: 
text += page.extract_text()
 return text 
except Exception as e:
 print(f"Error reading PDF {pdf_path.name}: {str(e)}") 
return ""
 def display_menu():
 print("\n=== Resume Analysis Suite ===") 
print("1. Team Comparison Analysis") 
print("2. Individual Skill Gap Analysis")
 print("3. Quantum-Inspired Similarity Scoring")
 print("4. Resume Ranking") 
print("5. Generate Skill Heatmaps") 
print("6. Generate Radar Charts") 
print("7. Generate Learning Paths")
 print("8. Generate Shortlist Justifications") 
print("9. Generate Executive PDF Report")
print("10. Run All 
Analyses") print("11. 
Exit")
 return input("Select an option (1-11): ").strip()
 def 
get_skills_input(
 ): while True:
 skills = input("Enter required skills (comma separated): 
").lower().split(',') skills = [skill.strip() for skill in skills if skill.strip()]
 if skills:
 return skills
 print("Error: Please enter at least one skill")
 def validate_resume_dir():
 resume_dir = 
Path('data/resumes/pdf') if not 
resume_dir.exists():
 print(f"Error: Resume directory not found at {resume_dir}")
 return False
 if not any(resume_dir.glob('*.pdf')):
 print(f"Error: No .pdf resume files found in 
{resume_dir}") return False
 return True
 def
return size
 print(f"Please enter a number between 1 and {total_candidates}")
 except ValueError:
 print("Invalid input. Please enter a number.")
 def team_comparison_analysis():
 print("\n=== Team Comparison Analysis ===") 
if not validate_resume_dir():
 return
 analyzer = TeamAnalyzer(Path('data/resumes/pdf')) 
requirements = get_skills_input()
 try:
 # Count total resumes first
 total_candidates = len(list(Path('data/resumes/pdf').glob('*.pdf'))) 
team_size = get_team_size_input(total_candidates)
 team_result = analyzer.recommend_team(requirements, team_size=team_size)
 # Prepare comprehensive output data 
output_data = {
 'team_composition': team_result['team'], 
'skill_coverage': {
 'percentage': team_result['coverage'],
 18
'missing_skills': 
team_result['missing_skills'], 
'required_skills': requirements
 },
 'candidate_metrics': {
 'total_analyzed': 
total_candidates, 'shortlisted': 
len(team_result['team']), 
'requested_team_size': 
team_size
 },
 'analysis_parameters': {
 'entanglement_threshold': 
analyzer.entanglement_threshold, 
'superposition_boost': analyzer.superposition_boost, 
'context_amplifier': analyzer.context_amplifier
 },
 }
 # Enhanced summary output
 print("\n=== Team Recommendation Summary 
===") print(f"\n Candidate Metrics:")
 print(f" - Total Candidates Analyzed: {total_candidates}")
 print(f" - Shortlisted Candidates: {len(team_result['team'])} (of requested 
{team_size})") print(f"\n Skill Coverage:")
print(f"\n Analysis Parameters:")
 print(f" - Entanglement Threshold: {analyzer.entanglement_threshold}") 
print(f" - Superposition Boost: {analyzer.superposition_boost}")
 print(f" - Context Amplifier: {analyzer.context_amplifier}")
 print("\nTeam Members:")
 for i, member in enumerate(team_result['team'], 1):
 print(f"\n {i}. {member['name']} (Score: {member['score']}%)")
 print(f" 
print(f" 
print(f"
 Matched Skills: {', '.join(member['matched']) or 'None'}")
 Missing Skills: {', '.join(member.get('missing', [])) or 'None'}") 
Recommendation: {member.get('recommendation', 'N/A')}")
 # Save results with better organization 
output_dir = Path('outputs/team_analysis') 
output_dir.mkdir(parents=True, exist_ok=True)
 # Generate timestamped filename
 output_file = output_dir / f"team_recommendation.json"
 with open(output_file, 'w', encoding='utf-8') as f: 
json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
 print(f"\nTeam analysis saved to: {output_file}")
