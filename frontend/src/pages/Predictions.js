import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { predictionsAPI } from '../services/api';
import toast from 'react-hot-toast';

const Predictions = () => {
  const { student } = useAuth();
  const [gpaResult, setGpaResult] = useState(null);
  const [scholarshipResult, setScholarshipResult] = useState(null);
  const [careerResult, setCareerResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Default student ID if student data not loaded
  const studentId = student?.id || 1;
  const studentCgpa = student?.current_cgpa || 7.0;
  const studentInterests = student?.interests || 'Technology';
  const studentSkills = student?.skills || 'Programming';
  const studentCodingAbility = student?.coding_ability || 'intermediate';

  const predictGPA = async () => {
    setLoading(true);
    try {
      const response = await predictionsAPI.predictGPA({
        student_id: studentId,
        internal_marks: 75,
        attendance_percentage: 85,
        assignment_score: 80,
        lab_performance: 78,
        previous_gpa: studentCgpa,
        study_hours_per_week: 20,
        participation_score: 75
      });
      setGpaResult(response.data);
      toast.success('GPA prediction generated!');
    } catch (error) {
      toast.error('Failed to predict GPA');
    } finally {
      setLoading(false);
    }
  };

  const predictScholarship = async () => {
    setLoading(true);
    try {
      const response = await predictionsAPI.predictScholarship({
        student_id: studentId,
        gpa: studentCgpa,
        attendance_percentage: 85,
        family_income: 400000,
        extracurricular_score: 70,
        discipline_score: 95,
        research_publications: 0
      });
      setScholarshipResult(response.data);
      toast.success('Scholarship eligibility checked!');
    } catch (error) {
      toast.error('Failed to check scholarship eligibility');
    } finally {
      setLoading(false);
    }
  };

  const recommendCareer = async () => {
    setLoading(true);
    try {
      const response = await predictionsAPI.recommendCareer({
        student_id: studentId,
        gpa: studentCgpa,
        subject_scores: { 'Computer Science': 85, 'Mathematics': 80 },
        interests: studentInterests?.split(',') || ['Technology'],
        skills: studentSkills?.split(',') || ['Programming'],
        coding_ability: studentCodingAbility
      });
      setCareerResult(response.data);
      toast.success('Career recommendations generated!');
    } catch (error) {
      toast.error('Failed to generate career recommendations');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>AI Predictions</h2>
      
      <div style={{ display: 'grid', gap: '20px', marginTop: '20px' }}>
        {/* GPA Prediction */}
        <div className="glass" style={{ padding: '24px', borderRadius: '12px' }}>
          <h3>📊 Semester GPA Predictor</h3>
          <button onClick={predictGPA} disabled={loading} className="btn btn-primary" style={{ marginTop: '12px' }}>
            {loading ? 'Predicting...' : 'Predict GPA'}
          </button>
          {gpaResult && (
            <div style={{ marginTop: '16px', padding: '16px', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
              <h4>Predicted GPA: {gpaResult.predicted_gpa}</h4>
              <p>Confidence: {gpaResult.confidence_score}%</p>
              <p>Grade: {gpaResult.grade_category}</p>
              <p>{gpaResult.interpretation}</p>
            </div>
          )}
        </div>

        {/* Scholarship Prediction */}
        <div className="glass" style={{ padding: '24px', borderRadius: '12px' }}>
          <h3>🎓 Scholarship Eligibility</h3>
          <button onClick={predictScholarship} disabled={loading} className="btn btn-primary" style={{ marginTop: '12px' }}>
            {loading ? 'Checking...' : 'Check Eligibility'}
          </button>
          {scholarshipResult && (
            <div style={{ marginTop: '16px', padding: '16px', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
              <h4>Status: {scholarshipResult.eligible ? '✅ Eligible' : '❌ Not Eligible'}</h4>
              <p>Probability: {scholarshipResult.probability}%</p>
            </div>
          )}
        </div>

        {/* Career Recommendations */}
        <div className="glass" style={{ padding: '24px', borderRadius: '12px' }}>
          <h3>💼 Career Recommendations</h3>
          <button onClick={recommendCareer} disabled={loading} className="btn btn-primary" style={{ marginTop: '12px' }}>
            {loading ? 'Generating...' : 'Get Recommendations'}
          </button>
          {careerResult && careerResult.recommendations && (
            <div style={{ marginTop: '16px' }}>
              {careerResult.recommendations.slice(0, 3).map((career, index) => (
                <div key={index} style={{ padding: '16px', background: 'var(--bg-tertiary)', borderRadius: '8px', marginBottom: '12px' }}>
                  <h4>{career.title}</h4>
                  <p>Match Score: {career.match_score}%</p>
                  <p>Salary Range: {career.salary_range}</p>
                  <p style={{ fontSize: '14px', marginTop: '8px' }}>{career.why_recommended}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Predictions;
