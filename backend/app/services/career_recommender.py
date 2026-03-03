"""
Service for Career Recommendation based on academic profile
"""
import numpy as np

class CareerRecommendationService:
    """Service for recommending career paths"""
    
    def __init__(self):
        self.career_database = self._initialize_career_database()
    
    def _initialize_career_database(self):
        """Initialize career database with requirements and details"""
        return [
            {
                'title': 'Software Engineer',
                'categories': ['Technology', 'Engineering'],
                'required_skills': ['Programming', 'Problem Solving', 'Data Structures'],
                'preferred_subjects': ['Computer Science', 'Mathematics', 'Programming'],
                'min_gpa': 6.5,
                'coding_level': 'intermediate',
                'salary_range': '₹6-25 LPA',
                'growth_potential': 'Very High',
                'courses': ['Data Structures', 'Algorithms', 'Web Development', 'System Design'],
                'certifications': ['AWS Certified', 'Google Cloud Professional', 'Microsoft Azure'],
                'companies': ['Google', 'Microsoft', 'Amazon', 'TCS', 'Infosys']
            },
            {
                'title': 'Data Scientist',
                'categories': ['Technology', 'Analytics'],
                'required_skills': ['Python', 'Machine Learning', 'Statistics', 'SQL'],
                'preferred_subjects': ['Mathematics', 'Statistics', 'Computer Science'],
                'min_gpa': 7.0,
                'coding_level': 'intermediate',
                'salary_range': '₹8-30 LPA',
                'growth_potential': 'Very High',
                'courses': ['Machine Learning', 'Deep Learning', 'Data Analytics', 'Big Data'],
                'certifications': ['Google Data Analytics', 'IBM Data Science', 'TensorFlow Developer'],
                'companies': ['Google', 'Amazon', 'Flipkart', 'LinkedIn', 'Meta']
            },
            {
                'title': 'Full Stack Developer',
                'categories': ['Technology', 'Web Development'],
                'required_skills': ['JavaScript', 'React', 'Node.js', 'Database'],
                'preferred_subjects': ['Computer Science', 'Web Technologies'],
                'min_gpa': 6.0,
                'coding_level': 'intermediate',
                'salary_range': '₹5-20 LPA',
                'growth_potential': 'High',
                'courses': ['React.js', 'Node.js', 'MongoDB', 'REST APIs'],
                'certifications': ['Meta Front-End Developer', 'MongoDB Certified'],
                'companies': ['Startups', 'Product Companies', 'Service Companies']
            },
            {
                'title': 'AI/ML Engineer',
                'categories': ['Technology', 'Artificial Intelligence'],
                'required_skills': ['Python', 'TensorFlow', 'PyTorch', 'Mathematics'],
                'preferred_subjects': ['Mathematics', 'Computer Science', 'AI'],
                'min_gpa': 7.5,
                'coding_level': 'advanced',
                'salary_range': '₹10-40 LPA',
                'growth_potential': 'Very High',
                'courses': ['Deep Learning', 'NLP', 'Computer Vision', 'Reinforcement Learning'],
                'certifications': ['TensorFlow Developer', 'AWS ML Specialty', 'Google ML Engineer'],
                'companies': ['Google', 'Meta', 'OpenAI', 'NVIDIA', 'Research Labs']
            },
            {
                'title': 'DevOps Engineer',
                'categories': ['Technology', 'Infrastructure'],
                'required_skills': ['Docker', 'Kubernetes', 'CI/CD', 'Cloud'],
                'preferred_subjects': ['Computer Science', 'Networking'],
                'min_gpa': 6.5,
                'coding_level': 'intermediate',
                'salary_range': '₹7-25 LPA',
                'growth_potential': 'High',
                'courses': ['Docker', 'Kubernetes', 'AWS', 'Jenkins', 'Terraform'],
                'certifications': ['AWS DevOps', 'Kubernetes Certified', 'Docker Certified'],
                'companies': ['Amazon', 'Netflix', 'Uber', 'Airbnb']
            },
            {
                'title': 'Business Analyst',
                'categories': ['Business', 'Analytics'],
                'required_skills': ['Excel', 'SQL', 'Communication', 'Problem Solving'],
                'preferred_subjects': ['Mathematics', 'Business', 'Economics'],
                'min_gpa': 6.0,
                'coding_level': 'beginner',
                'salary_range': '₹5-18 LPA',
                'growth_potential': 'Medium',
                'courses': ['Business Analytics', 'Excel', 'Tableau', 'Power BI'],
                'certifications': ['CBAP', 'Google Analytics', 'Tableau Certified'],
                'companies': ['Consulting Firms', 'Banks', 'E-commerce', 'Startups']
            },
            {
                'title': 'Cybersecurity Analyst',
                'categories': ['Technology', 'Security'],
                'required_skills': ['Network Security', 'Ethical Hacking', 'Cryptography'],
                'preferred_subjects': ['Computer Science', 'Networking', 'Security'],
                'min_gpa': 6.5,
                'coding_level': 'intermediate',
                'salary_range': '₹6-22 LPA',
                'growth_potential': 'High',
                'courses': ['Ethical Hacking', 'Network Security', 'Penetration Testing'],
                'certifications': ['CEH', 'CISSP', 'CompTIA Security+'],
                'companies': ['Cybersecurity Firms', 'Banks', 'Government', 'Consulting']
            },
            {
                'title': 'Product Manager',
                'categories': ['Business', 'Management'],
                'required_skills': ['Product Strategy', 'User Experience', 'Communication'],
                'preferred_subjects': ['Business', 'Computer Science', 'Management'],
                'min_gpa': 7.0,
                'coding_level': 'beginner',
                'salary_range': '₹10-35 LPA',
                'growth_potential': 'Very High',
                'courses': ['Product Management', 'UX Design', 'Agile', 'Business Strategy'],
                'certifications': ['Google PM Certificate', 'Pragmatic Marketing', 'Scrum Master'],
                'companies': ['Google', 'Amazon', 'Startups', 'Product Companies']
            }
        ]
    
    def recommend(self, student_data):
        """
        Recommend career paths based on student profile
        Input:
        - subject_strengths: dict of subject scores
        - gpa: current GPA
        - interests: list of interests
        - coding_ability: beginner/intermediate/advanced
        - skills: list of skills
        """
        recommendations = []
        
        for career in self.career_database:
            score = self._calculate_match_score(career, student_data)
            
            if score > 30:  # Threshold for recommendation
                career_recommendation = career.copy()
                career_recommendation['match_score'] = round(score, 2)
                career_recommendation['match_level'] = self._get_match_level(score)
                career_recommendation['why_recommended'] = self._generate_explanation(career, student_data, score)
                career_recommendation['preparation_tips'] = self._get_preparation_tips(career, student_data)
                
                recommendations.append(career_recommendation)
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _calculate_match_score(self, career, student_data):
        """Calculate match score between career and student profile"""
        score = 0
        
        # GPA match (20 points)
        gpa = student_data.get('gpa', 0)
        if gpa >= career['min_gpa']:
            score += 20
        elif gpa >= career['min_gpa'] - 0.5:
            score += 15
        elif gpa >= career['min_gpa'] - 1.0:
            score += 10
        
        # Coding ability match (20 points)
        coding_ability = student_data.get('coding_ability', 'beginner')
        coding_levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        
        student_level = coding_levels.get(coding_ability, 1)
        required_level = coding_levels.get(career['coding_level'], 2)
        
        if student_level >= required_level:
            score += 20
        elif student_level == required_level - 1:
            score += 15
        
        # Subject match (30 points)
        subject_scores = student_data.get('subject_scores', {})
        subject_match = 0
        
        for subject in career['preferred_subjects']:
            for student_subject, marks in subject_scores.items():
                if subject.lower() in student_subject.lower():
                    subject_match += min(10, marks / 10)
        
        score += min(30, subject_match)
        
        # Interest match (20 points)
        interests = student_data.get('interests', [])
        if isinstance(interests, str):
            interests = [i.strip() for i in interests.split(',')]
        
        interest_match = 0
        for interest in interests:
            for category in career['categories']:
                if interest.lower() in category.lower() or category.lower() in interest.lower():
                    interest_match += 10
        
        score += min(20, interest_match)
        
        # Skills match (10 points)
        skills = student_data.get('skills', [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(',')]
        
        skill_match = 0
        for skill in skills:
            for req_skill in career['required_skills']:
                if skill.lower() in req_skill.lower() or req_skill.lower() in skill.lower():
                    skill_match += 5
        
        score += min(10, skill_match)
        
        return score
    
    def _get_match_level(self, score):
        """Get match level description"""
        if score >= 80:
            return 'Excellent Match'
        elif score >= 65:
            return 'Very Good Match'
        elif score >= 50:
            return 'Good Match'
        elif score >= 35:
            return 'Moderate Match'
        else:
            return 'Low Match'
    
    def _generate_explanation(self, career, student_data, score):
        """Generate AI explanation for recommendation"""
        explanations = []
        
        gpa = student_data.get('gpa', 0)
        if gpa >= career['min_gpa']:
            explanations.append(f"Your GPA of {gpa} meets the requirement for this role")
        
        coding_ability = student_data.get('coding_ability', 'beginner')
        if coding_ability == career['coding_level']:
            explanations.append(f"Your {coding_ability} coding ability aligns with this career")
        
        subject_scores = student_data.get('subject_scores', {})
        strong_subjects = [subj for subj, score in subject_scores.items() if score >= 75]
        
        for subject in career['preferred_subjects']:
            for strong_subject in strong_subjects:
                if subject.lower() in strong_subject.lower():
                    explanations.append(f"Your strong performance in {strong_subject} is valuable for this role")
                    break
        
        if not explanations:
            explanations.append("This career path offers good growth opportunities")
        
        return '. '.join(explanations[:3]) + '.'
    
    def _get_preparation_tips(self, career, student_data):
        """Get personalized preparation tips"""
        tips = []
        
        # Add course recommendations
        tips.append(f"Focus on these courses: {', '.join(career['courses'][:3])}")
        
        # Add certification recommendations
        tips.append(f"Consider getting certified in: {career['certifications'][0]}")
        
        # Add skill gap analysis
        coding_ability = student_data.get('coding_ability', 'beginner')
        if coding_ability != career['coding_level']:
            tips.append(f"Improve your coding skills to {career['coding_level']} level")
        
        # Add GPA improvement if needed
        gpa = student_data.get('gpa', 0)
        if gpa < career['min_gpa']:
            tips.append(f"Work on improving your GPA to at least {career['min_gpa']}")
        
        return tips


# Singleton instance
career_recommendation_service = CareerRecommendationService()
