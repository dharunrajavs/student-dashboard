"""
AI Chatbot Mentor Service using OpenAI API
"""
import openai
import os
from app.models.student import Student
from app.models.performance import Performance
import json

class ChatbotService:
    """Service for AI-powered academic chatbot mentor"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', 500))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', 0.7))
    
    def get_student_context(self, student_id):
        """Get student academic context for personalized responses"""
        student = Student.query.get(student_id)
        if not student:
            return None
        
        # Get latest performance
        latest_performances = Performance.query.filter_by(
            student_id=student_id
        ).order_by(Performance.created_at.desc()).limit(5).all()
        
        context = {
            'name': student.full_name,
            'department': student.department,
            'semester': student.semester,
            'current_cgpa': student.current_cgpa,
            'coding_ability': student.coding_ability,
            'interests': student.interests,
            'recent_performance': []
        }
        
        for perf in latest_performances:
            context['recent_performance'].append({
                'subject': perf.subject_name,
                'marks': perf.total_marks,
                'attendance': perf.attendance_percentage,
                'grade': perf.grade
            })
        
        return context
    
    def generate_response(self, student_id, message, conversation_history=None):
        """
        Generate AI response using OpenAI API
        """
        if not self.api_key:
            fallback = self._fallback_response(message)
            return {
                'response': fallback,
                'success': True,
                'context_used': False
            }
        
        try:
            # Get student context
            student_context = self.get_student_context(student_id)
            
            # Build system message
            system_message = self._build_system_message(student_context)
            
            # Build conversation messages
            messages = [{"role": "system", "content": system_message}]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages
                    messages.append({"role": "user", "content": msg.get('message', '')})
                    messages.append({"role": "assistant", "content": msg.get('response', '')})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            return {
                'response': ai_response,
                'success': True,
                'context_used': student_context is not None
            }
        
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            fallback = self._fallback_response(message)
            # Handle case where fallback returns a string directly
            if isinstance(fallback, str):
                return {
                    'response': fallback,
                    'success': False,
                    'error': str(e)
                }
            return {
                'response': fallback.get('response', "I'm here to help with your academic queries."),
                'success': False,
                'error': str(e)
            }
    
    def _build_system_message(self, student_context):
        """Build system message with student context"""
        if not student_context:
            return """You are an AI Academic Mentor helping students with their studies. 
            Provide helpful, encouraging, and actionable advice. Be supportive and motivational.
            Focus on study strategies, time management, and academic improvement."""
        
        context_str = f"""You are an AI Academic Mentor named "AcademicAI Assistant".

Student Profile:
- Name: {student_context['name']}
- Department: {student_context['department']}
- Semester: {student_context['semester']}
- Current CGPA: {student_context['current_cgpa']}
- Coding Ability: {student_context.get('coding_ability', 'Not specified')}
- Interests: {student_context.get('interests', 'Not specified')}

Your role is to:
1. Provide personalized study plans based on the student's academic performance
2. Suggest subject-wise improvement strategies
3. Answer academic queries
4. Motivate and encourage the student
5. Recommend resources and study techniques
6. Help with exam preparation
7. Provide career guidance

Be supportive, encouraging, and provide actionable advice. Use the student's context to personalize your responses.
Keep responses concise and helpful (under 200 words)."""

        return context_str
    
    def _fallback_response(self, message):
        """Fallback response when OpenAI API is not available"""
        message_lower = message.lower()
        
        # Study plan queries
        if any(word in message_lower for word in ['study plan', 'how to study', 'study tips']):
            return """Here's a recommended study plan:

1. **Daily Schedule**: Study 3-4 hours daily with 25-min focus sessions (Pomodoro Technique)
2. **Prioritize**: Focus on weak subjects first
3. **Active Learning**: Practice problems, not just reading
4. **Review**: Weekly revision of covered topics
5. **Sleep**: Get 7-8 hours for better retention

Would you like subject-specific guidance?"""
        
        # Improvement strategies
        elif any(word in message_lower for word in ['improve', 'better grades', 'score more']):
            return """To improve your grades:

1. Attend all classes regularly (aim for 90%+ attendance)
2. Complete assignments on time
3. Practice previous year papers
4. Form study groups
5. Ask doubts immediately
6. Make notes during lectures
7. Take mock tests regularly

Focus on understanding concepts, not memorization!"""
        
        # Motivation
        elif any(word in message_lower for word in ['motivate', 'discouraged', 'failed', 'worried']):
            return """Don't be discouraged! Every successful person faced challenges.

Remember:
- Failure is a stepping stone to success
- Your current situation is temporary
- Consistent effort yields results
- Ask for help when needed
- Believe in your abilities

Start with small goals and build momentum. You can do this! 💪"""
        
        # Exam preparation
        elif any(word in message_lower for word in ['exam', 'test', 'preparation']):
            return """Exam Preparation Strategy:

**2 Weeks Before:**
- Complete syllabus coverage
- Make summary notes

**1 Week Before:**
- Solve previous papers
- Practice numericals
- Revise important topics

**2 Days Before:**
- Quick revision only
- Don't start new topics

**Exam Day:**
- Good sleep night before
- Read questions carefully
- Manage time wisely

Best of luck!"""
        
        # Default response
        else:
            return """I'm here to help you with:
- Study plans and strategies
- Subject-wise guidance
- Exam preparation tips
- Career advice
- Motivation and support

What specific area would you like help with?"""
    
    def generate_study_plan(self, student_id):
        """Generate a personalized study plan"""
        student = Student.query.get(student_id)
        if not student:
            return None
        
        performances = Performance.query.filter_by(
            student_id=student_id
        ).order_by(Performance.created_at.desc()).limit(10).all()
        
        # Identify weak subjects
        weak_subjects = []
        strong_subjects = []
        
        for perf in performances:
            if perf.total_marks < 60:
                weak_subjects.append(perf.subject_name)
            elif perf.total_marks >= 80:
                strong_subjects.append(perf.subject_name)
        
        plan = {
            'weak_subjects': list(set(weak_subjects)),
            'strong_subjects': list(set(strong_subjects)),
            'recommendations': []
        }
        
        if weak_subjects:
            plan['recommendations'].append(
                f"Focus extra time on: {', '.join(set(weak_subjects[:3]))}"
            )
        
        plan['recommendations'].append("Study 3-4 hours daily with regular breaks")
        plan['recommendations'].append("Practice problems daily for technical subjects")
        plan['recommendations'].append("Review lecture notes within 24 hours")
        
        return plan


# Singleton instance
chatbot_service = ChatbotService()
