import json
from collections import defaultdict
from pathlib import Path
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Set, Tuple, Optional

class TeamAnalyzer:
    def __init__(self, resume_dir: str):
        self.resume_dir = Path(resume_dir)
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            raise ImportError(
                "Quantum linguistic processor missing! Please install:\n"
                "python -m spacy download en_core_web_lg"
            )
        
        # Enhanced quantum-inspired skill ontology
        self.skill_ontology = {
            'react': {
                'related': ['javascript', 'frontend', 'redux', 'hooks', 'jsx'],
                'contexts': ['web app', 'spa', 'component-based', 'virtual dom'],
                'patterns': ['react.js', 'reactjs', 'react native'],
                'entanglement': {
                    'javascript': 0.95,
                    'angular': 0.65,
                    'vue': 0.7
                }
            },
            'python': {
                'related': ['django', 'flask', 'data science', 'pandas', 'numpy'],
                'contexts': ['scripting', 'automation', 'machine learning', 'ai'],
                'patterns': ['python 3', 'python scripting'],
                'entanglement': {
                    'data analysis': 0.85,
                    'machine learning': 0.9,
                    'automation': 0.75
                }
            },
        }
        
        # Quantum parameters
        self.entanglement_threshold = 0.65
        self.superposition_boost = 1.3
        self.context_amplifier = 1.2
        self.skill_weights = defaultdict(lambda: 1.0)
        self.entanglement_cache = {}

    def _quantum_entanglement(self, skill1: str, skill2: str) -> float:
        """Calculate quantum-inspired entanglement between skills"""
        cache_key = frozenset({skill1, skill2})
        if cache_key in self.entanglement_cache:
            return self.entanglement_cache[cache_key]
        
        # Check direct quantum entanglements
        if skill1 in self.skill_ontology and skill2 in self.skill_ontology[skill1].get('entanglement', {}):
            score = self.skill_ontology[skill1]['entanglement'][skill2]
            self.entanglement_cache[cache_key] = score
            return score
            
        # Check pattern matches
        skill1_patterns = self.skill_ontology.get(skill1, {}).get('patterns', [])
        skill2_patterns = self.skill_ontology.get(skill2, {}).get('patterns', [])
        
        if any(p in skill2 for p in skill1_patterns) or any(p in skill1 for p in skill2_patterns):
            self.entanglement_cache[cache_key] = 0.9
            return 0.9
            
        # Calculate semantic similarity with quantum boost
        vec1 = self.nlp(skill1).vector
        vec2 = self.nlp(skill2).vector
        
        if not vec1.any() or not vec2.any():
            return 0.0
            
        base_sim = cosine_similarity([vec1], [vec2])[0][0]
        
        # Apply quantum-inspired boosts
        if skill2 in self.skill_ontology.get(skill1, {}).get('related', []):
            base_sim = min(base_sim * self.superposition_boost, 1.0)
        elif any(ctx in skill2 for ctx in self.skill_ontology.get(skill1, {}).get('contexts', [])):
            base_sim = min(base_sim * self.context_amplifier, 1.0)
        
        self.entanglement_cache[cache_key] = base_sim
        return base_sim

    def analyze_candidate(self, resume_path: Path, required_skills: List[str]) -> Dict:
        """Analyze a candidate with quantum-inspired matching"""
        try:
            with open(resume_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract and infer skills
            explicit_skills = {s.lower() for s in required_skills if s.lower() in content}
            inferred_skills = self._infer_skills_from_context(content)
            all_skills = explicit_skills.union(inferred_skills)
            
            # Quantum-enhanced matching
            matched = []
            missing = []
            for req_skill in required_skills:
                req_skill = req_skill.lower()
                if req_skill in all_skills:
                    matched.append(req_skill)
                    continue
                    
                # Quantum-style superposition check
                max_sim = max([self._quantum_entanglement(req_skill, cand_skill) 
                             for cand_skill in all_skills], default=0)
                if max_sim > self.entanglement_threshold:
                    matched.append(f"{req_skill} (inferred)")
                else:
                    missing.append(req_skill)
            
            # Calculate gap score (quantum-inspired weighting)
            base_score = len(matched) / len(required_skills)
            context_boost = 0.1 if any('inferred' in s for s in matched) else 0
            final_score = min(base_score + context_boost, 1.0) * 100
            
            return {
                'name': resume_path.stem.replace('_', ' ').title(),
                'matched': matched,
                'missing': missing,
                'score': round(final_score, 1),
                'recommendation': self._generate_recommendation(matched, missing)
            }
            
        except Exception as e:
            print(f"Quantum analysis error for {resume_path.name}: {str(e)}")
            return {
                'name': resume_path.stem.replace('_', ' ').title(),
                'matched': [],
                'missing': required_skills,
                'score': 0,
                'recommendation': "Analysis failed"
            }

    def _infer_skills_from_context(self, text: str) -> Set[str]:
        """Extract skills using NLP + quantum-inspired context analysis"""
        doc = self.nlp(text.lower())
        inferred_skills = set()
        
        for token in doc:
            # Direct skill matches
            if token.text in self.skill_ontology:
                inferred_skills.add(token.text)
                
            # Contextual inference (quantum-inspired fuzzy matching)
            for skill, data in self.skill_ontology.items():
                for ctx_word in data['contexts']:
                    if ctx_word in text and self._quantum_entanglement(token.text, skill) > 0.7:
                        inferred_skills.add(skill)
                        
        return inferred_skills

    def _generate_recommendation(self, matched: List[str], missing: List[str]) -> str:
        """Quantum-style probabilistic recommendation"""
        match_ratio = len(matched) / (len(matched) + len(missing))
        if match_ratio > 0.75:
            return "Strong quantum match - recommend interview"
        elif any('inferred' in s for s in matched):
            return "Potential quantum match - suggest technical screening"
        else:
            return "Partial match - consider upskilling plan"

    def recommend_team(self, required_skills: List[str], team_size: int = 3) -> Dict:
        """Recommend a quantum-optimized team"""
        candidates = []
        for resume in self.resume_dir.glob('*.txt'):
            analysis = self.analyze_candidate(resume, required_skills)
            candidates.append(analysis)
        
        # Quantum-inspired team composition
        candidates.sort(key=lambda x: x['score'], reverse=True)
        team = candidates[:team_size]
        
        # Calculate team coverage (entangled skills count as partial matches)
        team_skills = set()
        for member in team:
            team_skills.update([s.replace(' (inferred)', '') for s in member['matched']])
        
        coverage = len([s for s in required_skills if s.lower() in team_skills]) / len(required_skills)
        
        return {
            'team': team,  # Changed from 'members' to 'team' to match usage
            'coverage': round(coverage * 100, 1),
            'missing_skills': [s for s in required_skills 
                             if s.lower() not in team_skills]
        }
