import os
from collections import defaultdict

class LearningPathGenerator:
    def __init__(self):
        # Enhanced resource database with better organization
        self.resources = {
            'python': [
                {'title': 'Python Crash Course (Book)', 'type': 'book', 'level': 'Beginner', 'duration': '30h', 'url': 'https://nostarch.com/pythoncrashcourse'},
                {'title': 'Automate the Boring Stuff (Online Course)', 'type': 'course', 'level': 'Beginner', 'duration': '25h', 'url': 'https://automatetheboringstuff.com'},
                {'title': 'Python Data Science Handbook (Book)', 'type': 'book', 'level': 'Intermediate', 'duration': '40h', 'url': 'https://jakevdp.github.io/PythonDataScienceHandbook/'},
                {'title': 'Fluent Python (Book)', 'type': 'book', 'level': 'Advanced', 'duration': '50h', 'url': 'https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/'},
                {'title': 'Real Python Tutorials', 'type': 'tutorials', 'level': 'All', 'duration': '100h', 'url': 'https://realpython.com'}
            ],
            'aws': [
                {'title': 'AWS Cloud Practitioner Essentials', 'type': 'course', 'level': 'Beginner', 'duration': '15h', 'url': 'https://aws.amazon.com/training/digital/'},
                {'title': 'AWS Solutions Architect Associate', 'type': 'course', 'level': 'Intermediate', 'duration': '40h', 'url': 'https://aws.amazon.com/certification/certified-solutions-architect-associate/'},
                {'title': 'AWS Developer Guide', 'type': 'docs', 'level': 'Intermediate', 'duration': '30h', 'url': 'https://docs.aws.amazon.com'}
            ],
            'machine learning': [
                {'title': 'Hands-On Machine Learning with Scikit-Learn', 'type': 'book', 'level': 'Beginner', 'duration': '35h', 'url': 'https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/'},
                {'title': 'Fast.ai Practical Deep Learning', 'type': 'course', 'level': 'Intermediate', 'duration': '60h', 'url': 'https://course.fast.ai'},
                {'title': 'Andrew Ng Machine Learning Course', 'type': 'course', 'level': 'Beginner', 'duration': '55h', 'url': 'https://www.coursera.org/learn/machine-learning'}
            ],
            'data analysis': [
                {'title': 'Python for Data Analysis (Book)', 'type': 'book', 'level': 'Beginner', 'duration': '30h', 'url': 'https://www.oreilly.com/library/view/python-for-data/9781491957653/'},
                {'title': 'Data Science from Scratch (Book)', 'type': 'book', 'level': 'Intermediate', 'duration': '40h', 'url': 'https://www.oreilly.com/library/view/data-science-from/9781492041122/'}
            ],
            # Default fallback resources
            '_default': [
                {'title': 'LinkedIn Learning', 'type': 'platform', 'level': 'Beginner', 'duration': '20h', 'url': 'https://www.linkedin.com/learning/'},
                {'title': 'Coursera Professional Development', 'type': 'course', 'level': 'Beginner', 'duration': '30h', 'url': 'https://www.coursera.org/'},
                {'title': 'Udemy Online Courses', 'type': 'platform', 'level': 'All', 'duration': '40h', 'url': 'https://www.udemy.com/'}
            ]
        }

    def _get_resources_for_skill(self, skill, current_level='Beginner'):
        """Get appropriate resources filtered by level with fallback"""
        skill_resources = self.resources.get(skill.lower(), self.resources['_default'])
        
        # Filter resources by level (include resources at or below current level)
        filtered_resources = [
            res for res in skill_resources 
            if res['level'].lower() == current_level.lower() or 
               (current_level.lower() == 'beginner' and res['level'].lower() in ['beginner', 'all']) or
               (current_level.lower() == 'intermediate' and res['level'].lower() in ['beginner', 'intermediate', 'all']) or
               (current_level.lower() == 'advanced' and res['level'].lower() in ['beginner', 'intermediate', 'advanced', 'all'])
        ]
        
        return filtered_resources if filtered_resources else skill_resources[:2]

    def generate_learning_path(self, missing_skills, current_level='Beginner'):
        """Generate comprehensive learning path with level-appropriate resources"""
        path = defaultdict(list)
        total_hours = 0
        
        for skill in missing_skills:
            resources = self._get_resources_for_skill(skill, current_level)
            
            # Select 2-3 most appropriate resources per skill
            selected_resources = resources[:3] if len(resources) > 3 else resources
            path[skill] = selected_resources
            total_hours += sum(int(res['duration'][:-1]) for res in selected_resources)
        
        return {
            'learning_path': dict(path),
            'total_hours': total_hours,
            'missing_skills': missing_skills
        }

    def create_learning_report(self, candidate_name, analysis_result, output_dir):
        """Generate detailed learning report with better formatting"""
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{candidate_name.replace(' ', '_')}_learning_path.txt")
        
        report_lines = [
            "PERSONALIZED LEARNING PATH REPORT",
            "="*50,
            f"Candidate: {candidate_name}",
            f"Missing Skills: {', '.join([s.capitalize() for s in analysis_result['missing_skills']])}",
            f"Estimated Training Time: {analysis_result['total_hours']} hours",
            "\nRECOMMENDED LEARNING RESOURCES:",
            ""
        ]
        
        for skill, resources in analysis_result['learning_path'].items():
            report_lines.append(f"\nSKILL: {skill.upper()}")
            report_lines.append("-" * (6 + len(skill)))
            for i, resource in enumerate(resources, 1):
                report_lines.append(f"\n{i}. {resource['title']}")
                report_lines.append(f"   • Type: {resource['type'].title()}")
                report_lines.append(f"   • Level: {resource['level']}")
                report_lines.append(f"   • Duration: {resource['duration']}")
                report_lines.append(f"   • URL: {resource['url']}")
            report_lines.append("\n" + "="*50)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        
        return output_path

    def process_resumes(self, resume_dir, required_skills, output_dir):
        """Process all resumes and generate comprehensive learning paths"""
        required_skills = [skill.lower().strip() for skill in required_skills]
        generated_reports = []
        
        for filename in os.listdir(resume_dir):
            if filename.endswith('.txt'):
                candidate_name = filename[:-4].replace('_', ' ').title()
                resume_path = os.path.join(resume_dir, filename)
                
                with open(resume_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                missing_skills = [
                    skill for skill in required_skills 
                    if skill and skill not in content
                ]
                
                if missing_skills:
                    path = self.generate_learning_path(missing_skills)
                    report_path = self.create_learning_report(candidate_name, path, output_dir)
                    generated_reports.append(report_path)
        
        return generated_reports
