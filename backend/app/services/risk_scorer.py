"""
Risk Scoring Service for early warning system
"""
from app.models.student import Student
from app.models.performance import Performance
from sqlalchemy import func

class RiskScoringService:
    """Service for calculating student risk scores (0-100 scale)"""
    
    def calculate_risk_score(self, student_id):
        """
        Calculate comprehensive risk score for a student
        0 = No risk (excellent performance)
        100 = Critical risk (immediate intervention needed)
        """
        student = Student.query.get(student_id)
        if not student:
            return None
        
        # Get recent performance data
        recent_performances = Performance.query.filter_by(
            student_id=student_id
        ).order_by(Performance.created_at.desc()).limit(10).all()
        
        if not recent_performances:
            return {
                'risk_score': 50,
                'risk_level': 'Unknown',
                'factors': ['Insufficient data'],
                'recommendations': ['Add performance data for accurate assessment']
            }
        
        risk_score = 0
        risk_factors = []
        
        # 1. GPA Risk (25 points)
        gpa_risk, gpa_factors = self._calculate_gpa_risk(student.current_cgpa)
        risk_score += gpa_risk
        risk_factors.extend(gpa_factors)
        
        # 2. Attendance Risk (20 points)
        avg_attendance = sum(p.attendance_percentage for p in recent_performances) / len(recent_performances)
        attendance_risk, attendance_factors = self._calculate_attendance_risk(avg_attendance)
        risk_score += attendance_risk
        risk_factors.extend(attendance_factors)
        
        # 3. Performance Trend Risk (20 points)
        trend_risk, trend_factors = self._calculate_trend_risk(recent_performances)
        risk_score += trend_risk
        risk_factors.extend(trend_factors)
        
        # 4. Assignment & Lab Risk (15 points)
        avg_assignment = sum(p.assignment_score for p in recent_performances) / len(recent_performances)
        avg_lab = sum(p.lab_performance for p in recent_performances) / len(recent_performances)
        assignment_risk, assignment_factors = self._calculate_assignment_risk(avg_assignment, avg_lab)
        risk_score += assignment_risk
        risk_factors.extend(assignment_factors)
        
        # 5. Study Hours Risk (10 points)
        avg_study_hours = sum(p.study_hours_per_week for p in recent_performances) / len(recent_performances)
        study_risk, study_factors = self._calculate_study_hours_risk(avg_study_hours)
        risk_score += study_risk
        risk_factors.extend(study_factors)
        
        # 6. Discipline Risk (10 points)
        avg_discipline = sum(p.discipline_score for p in recent_performances) / len(recent_performances)
        discipline_risk, discipline_factors = self._calculate_discipline_risk(avg_discipline)
        risk_score += discipline_risk
        risk_factors.extend(discipline_factors)
        
        # Determine risk level
        risk_level = self._get_risk_level(risk_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_score, risk_factors, student, recent_performances
        )
        
        return {
            'risk_score': round(risk_score, 2),
            'risk_level': risk_level,
            'factors': list(set(risk_factors)),
            'recommendations': recommendations,
            'breakdown': {
                'gpa_risk': gpa_risk,
                'attendance_risk': attendance_risk,
                'trend_risk': trend_risk,
                'assignment_risk': assignment_risk,
                'study_hours_risk': study_risk,
                'discipline_risk': discipline_risk
            },
            'metrics': {
                'current_cgpa': student.current_cgpa,
                'average_attendance': round(avg_attendance, 2),
                'average_assignment_score': round(avg_assignment, 2),
                'average_study_hours': round(avg_study_hours, 2)
            }
        }
    
    def _calculate_gpa_risk(self, gpa):
        """Calculate risk based on GPA"""
        risk = 0
        factors = []
        
        if gpa < 5.0:
            risk = 25
            factors.append('Critical: GPA below 5.0')
        elif gpa < 6.0:
            risk = 20
            factors.append('High risk: GPA below 6.0')
        elif gpa < 7.0:
            risk = 10
            factors.append('Moderate: GPA below 7.0')
        elif gpa < 8.0:
            risk = 5
            factors.append('Low risk: GPA can be improved')
        
        return risk, factors
    
    def _calculate_attendance_risk(self, attendance):
        """Calculate risk based on attendance"""
        risk = 0
        factors = []
        
        if attendance < 60:
            risk = 20
            factors.append('Critical: Attendance below 60%')
        elif attendance < 75:
            risk = 15
            factors.append('High risk: Attendance below minimum 75%')
        elif attendance < 85:
            risk = 8
            factors.append('Moderate: Attendance could be better')
        elif attendance < 90:
            risk = 3
            factors.append('Low risk: Good attendance')
        
        return risk, factors
    
    def _calculate_trend_risk(self, performances):
        """Calculate risk based on performance trend"""
        if len(performances) < 3:
            return 0, []
        
        # Get last 3 performances
        recent_3 = performances[:3]
        recent_marks = [p.total_marks for p in recent_3]
        
        # Calculate trend
        if len(recent_marks) >= 2:
            trend = recent_marks[0] - recent_marks[-1]
            
            if trend < -15:  # Declining significantly
                return 20, ['Declining performance trend']
            elif trend < -5:  # Declining moderately
                return 10, ['Gradual decline in performance']
            elif trend > 10:  # Improving
                return 0, []
            else:
                return 5, ['Stagnant performance']
        
        return 0, []
    
    def _calculate_assignment_risk(self, avg_assignment, avg_lab):
        """Calculate risk based on assignments and lab work"""
        risk = 0
        factors = []
        
        if avg_assignment < 50:
            risk += 8
            factors.append('Poor assignment completion')
        elif avg_assignment < 70:
            risk += 4
            factors.append('Below average assignment scores')
        
        if avg_lab < 50:
            risk += 7
            factors.append('Poor lab performance')
        elif avg_lab < 70:
            risk += 3
            factors.append('Below average lab performance')
        
        return risk, factors
    
    def _calculate_study_hours_risk(self, study_hours):
        """Calculate risk based on study hours"""
        risk = 0
        factors = []
        
        if study_hours < 10:
            risk = 10
            factors.append('Insufficient study hours (< 10 hrs/week)')
        elif study_hours < 15:
            risk = 5
            factors.append('Low study hours')
        
        return risk, factors
    
    def _calculate_discipline_risk(self, discipline_score):
        """Calculate risk based on discipline"""
        risk = 0
        factors = []
        
        if discipline_score < 70:
            risk = 10
            factors.append('Discipline issues noted')
        elif discipline_score < 85:
            risk = 5
            factors.append('Minor discipline concerns')
        
        return risk, factors
    
    def _get_risk_level(self, risk_score):
        """Determine risk level from score"""
        if risk_score >= 70:
            return 'Critical'
        elif risk_score >= 50:
            return 'High'
        elif risk_score >= 30:
            return 'Moderate'
        elif risk_score >= 15:
            return 'Low'
        else:
            return 'Minimal'
    
    def _generate_recommendations(self, risk_score, factors, student, performances):
        """Generate actionable recommendations"""
        recommendations = []
        
        if risk_score >= 70:
            recommendations.append('Immediate counseling session required')
            recommendations.append('Contact parents/guardians')
            recommendations.append('Develop intensive improvement plan')
        elif risk_score >= 50:
            recommendations.append('Schedule meeting with faculty advisor')
            recommendations.append('Attend remedial classes')
            recommendations.append('Join peer study groups')
        elif risk_score >= 30:
            recommendations.append('Increase study hours to 20+ per week')
            recommendations.append('Focus on weak subjects')
            recommendations.append('Improve attendance to 85%+')
        else:
            recommendations.append('Maintain current performance level')
            recommendations.append('Consider participating in extra activities')
        
        # Add specific recommendations based on factors
        avg_attendance = sum(p.attendance_percentage for p in performances) / len(performances)
        if avg_attendance < 75:
            recommendations.append('URGENT: Improve attendance to meet minimum requirement')
        
        if student.current_cgpa < 6.0:
            recommendations.append('Focus on core subjects to improve CGPA')
        
        return recommendations


# Singleton instance
risk_scoring_service = RiskScoringService()
