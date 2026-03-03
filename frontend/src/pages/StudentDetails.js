import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { studentsAPI, predictionsAPI } from '../services/api';
import toast from 'react-hot-toast';
import './Dashboard.css';

const StudentDetails = () => {
  const { studentId } = useParams();
  const navigate = useNavigate();
  const [student, setStudent] = useState(null);
  const [performance, setPerformance] = useState([]);
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAddPerformance, setShowAddPerformance] = useState(false);
  const [performanceForm, setPerformanceForm] = useState({
    semester: 1,
    subject_name: '',
    internal_marks: '',
    external_marks: '',
    attendance_percentage: '',
    assignment_score: '',
    lab_performance: ''
  });

  useEffect(() => {
    if (studentId) {
      fetchStudentData();
    }
  }, [studentId]);

  const fetchStudentData = async () => {
    try {
      setLoading(true);
      const [profileRes, perfRes] = await Promise.all([
        studentsAPI.getProfile(studentId),
        studentsAPI.getPerformance(studentId)
      ]);
      
      setStudent(profileRes.data);
      setPerformance(perfRes.data.records || []);
      
      // Try to get risk score
      try {
        const riskRes = await predictionsAPI.calculateRiskScore(studentId);
        setPredictions(riskRes.data);
      } catch (e) {
        console.log('Risk score not available');
      }
    } catch (error) {
      console.error('Error fetching student:', error);
      toast.error('Failed to load student data');
      navigate('/students');
    } finally {
      setLoading(false);
    }
  };

  const handleAddPerformance = async (e) => {
    e.preventDefault();
    try {
      const data = {
        student_id: parseInt(studentId),
        semester: parseInt(performanceForm.semester),
        subject_name: performanceForm.subject_name,
        internal_marks: parseFloat(performanceForm.internal_marks) || 0,
        external_marks: parseFloat(performanceForm.external_marks) || 0,
        attendance_percentage: parseFloat(performanceForm.attendance_percentage) || 0,
        assignment_score: parseFloat(performanceForm.assignment_score) || 0,
        lab_performance: parseFloat(performanceForm.lab_performance) || 0
      };
      
      await studentsAPI.addPerformance(data);
      toast.success('Performance record added');
      setShowAddPerformance(false);
      setPerformanceForm({
        semester: student?.semester || 1,
        subject_name: '',
        internal_marks: '',
        external_marks: '',
        attendance_percentage: '',
        assignment_score: '',
        lab_performance: ''
      });
      fetchStudentData();
    } catch (error) {
      console.error('Error adding performance:', error);
      toast.error(error.response?.data?.error || 'Failed to add performance record');
    }
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-state" style={{ padding: '60px', textAlign: 'center' }}>
          <div className="spinner"></div>
          <p>Loading student details...</p>
        </div>
      </div>
    );
  }

  if (!student) {
    return (
      <div className="dashboard-container">
        <div className="empty-state" style={{ padding: '60px', textAlign: 'center' }}>
          <h2>Student Not Found</h2>
          <Link to="/students" className="btn btn-primary" style={{ marginTop: '16px' }}>
            Back to Students List
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">{student.first_name} {student.last_name}</h1>
          <p className="page-subtitle">{student.roll_number} • {student.department}</p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <Link to="/students" className="btn btn-secondary">
            ← Back to Students
          </Link>
          <button 
            className="btn btn-primary"
            onClick={() => setShowAddPerformance(true)}
          >
            + Add Performance
          </button>
        </div>
      </div>

      {/* Student Info Cards */}
      <div className="dashboard-grid" style={{ marginBottom: '24px' }}>
        {/* Basic Info */}
        <div className="card">
          <div className="card-header">
            <h3>Personal Information</h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Full Name:</span>
                <span style={{ fontWeight: '500' }}>{student.full_name}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Roll Number:</span>
                <code style={{ background: 'var(--bg-secondary)', padding: '2px 8px', borderRadius: '4px' }}>{student.roll_number}</code>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Gender:</span>
                <span>{student.gender || 'Not specified'}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Phone:</span>
                <span>{student.phone || 'Not provided'}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Joined:</span>
                <span>{new Date(student.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Academic Info */}
        <div className="card">
          <div className="card-header">
            <h3>Academic Information</h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Department:</span>
                <span style={{ fontWeight: '500' }}>{student.department}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Semester:</span>
                <span className="badge badge-info">Semester {student.semester}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Batch:</span>
                <span>{student.batch || 'N/A'}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Current CGPA:</span>
                <span style={{
                  fontWeight: 'bold', fontSize: '18px',
                  color: student.current_cgpa >= 8 ? 'var(--success)' : 
                         student.current_cgpa >= 6 ? 'var(--warning)' : 'var(--danger)'
                }}>
                  {student.current_cgpa?.toFixed(2) || '0.00'}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Coding Ability:</span>
                <span className={`badge ${
                  student.coding_ability === 'advanced' ? 'badge-success' :
                  student.coding_ability === 'intermediate' ? 'badge-warning' : 'badge-secondary'
                }`}>
                  {student.coding_ability || 'N/A'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Skills & Interests */}
        <div className="card">
          <div className="card-header">
            <h3>Skills & Interests</h3>
          </div>
          <div className="card-body">
            <div style={{ marginBottom: '16px' }}>
              <label style={{ color: 'var(--text-secondary)', display: 'block', marginBottom: '8px' }}>Interests:</label>
              <p style={{ margin: 0 }}>{student.interests || 'No interests specified'}</p>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ color: 'var(--text-secondary)', display: 'block', marginBottom: '8px' }}>Skills:</label>
              <p style={{ margin: 0 }}>{student.skills || 'No skills specified'}</p>
            </div>
            <div>
              <label style={{ color: 'var(--text-secondary)', display: 'block', marginBottom: '8px' }}>Family Income:</label>
              <p style={{ margin: 0 }}>
                {student.family_income ? `₹${student.family_income.toLocaleString()}/year` : 'Not provided'}
              </p>
            </div>
          </div>
        </div>

        {/* Risk Score */}
        <div className="card">
          <div className="card-header">
            <h3>Risk Assessment</h3>
          </div>
          <div className="card-body" style={{ textAlign: 'center' }}>
            {predictions ? (
              <>
                <div style={{
                  width: '100px', height: '100px', borderRadius: '50%', margin: '0 auto 16px',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  background: predictions.risk_score > 60 ? 'var(--danger-bg)' :
                             predictions.risk_score > 40 ? 'var(--warning-bg)' : 'var(--success-bg)',
                  border: `3px solid ${predictions.risk_score > 60 ? 'var(--danger)' :
                          predictions.risk_score > 40 ? 'var(--warning)' : 'var(--success)'}`
                }}>
                  <span style={{ fontSize: '28px', fontWeight: 'bold' }}>{predictions.risk_score}%</span>
                </div>
                <span className={`badge ${
                  predictions.risk_level === 'high' ? 'badge-danger' :
                  predictions.risk_level === 'medium' ? 'badge-warning' : 'badge-success'
                }`} style={{ fontSize: '14px', padding: '6px 16px' }}>
                  {predictions.risk_level?.toUpperCase()} RISK
                </span>
              </>
            ) : (
              <p style={{ color: 'var(--text-secondary)' }}>No risk assessment available</p>
            )}
          </div>
        </div>
      </div>

      {/* Performance Records */}
      <div className="card">
        <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3>Performance Records ({performance.length})</h3>
          <button 
            className="btn btn-sm btn-primary"
            onClick={() => setShowAddPerformance(true)}
          >
            + Add Record
          </button>
        </div>
        <div className="card-body" style={{ padding: 0 }}>
          {performance.length === 0 ? (
            <div className="empty-state" style={{ padding: '40px', textAlign: 'center' }}>
              <p>No performance records yet</p>
              <button 
                className="btn btn-primary" 
                style={{ marginTop: '16px' }}
                onClick={() => setShowAddPerformance(true)}
              >
                Add First Record
              </button>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: 'var(--bg-secondary)' }}>
                    <th style={{ padding: '12px 16px', textAlign: 'left', borderBottom: '1px solid var(--border-color)' }}>Subject</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>Semester</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>Internal</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>External</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>Attendance</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>Assignment</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>Lab</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>GPA</th>
                  </tr>
                </thead>
                <tbody>
                  {performance.map((record, index) => (
                    <tr key={index} style={{ borderBottom: '1px solid var(--border-color)' }}>
                      <td style={{ padding: '12px 16px', fontWeight: '500' }}>{record.subject_name}</td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                        <span className="badge badge-info">Sem {record.semester}</span>
                      </td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>{record.internal_marks || '-'}</td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>{record.external_marks || '-'}</td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                        <span style={{ 
                          color: record.attendance_percentage >= 75 ? 'var(--success)' : 'var(--danger)'
                        }}>
                          {record.attendance_percentage}%
                        </span>
                      </td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>{record.assignment_score || '-'}</td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>{record.lab_performance || '-'}</td>
                      <td style={{ padding: '12px 16px', textAlign: 'center', fontWeight: 'bold' }}>
                        {record.gpa?.toFixed(2) || '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Add Performance Modal */}
      {showAddPerformance && (
        <div className="modal-overlay" style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center',
          zIndex: 1000
        }}>
          <div className="modal-content card" style={{ 
            width: '100%', maxWidth: '500px', maxHeight: '90vh', overflow: 'auto' 
          }}>
            <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3>Add Performance Record</h3>
              <button 
                onClick={() => setShowAddPerformance(false)}
                style={{ 
                  background: 'none', border: 'none', fontSize: '24px', cursor: 'pointer',
                  color: 'var(--text-secondary)'
                }}
              >
                ×
              </button>
            </div>
            <div className="card-body">
              <form onSubmit={handleAddPerformance}>
                <div className="form-group">
                  <label>Subject Name *</label>
                  <input
                    type="text"
                    className="form-input"
                    value={performanceForm.subject_name}
                    onChange={(e) => setPerformanceForm({...performanceForm, subject_name: e.target.value})}
                    required
                    placeholder="e.g., Data Structures"
                  />
                </div>
                
                <div className="form-row" style={{ display: 'flex', gap: '16px' }}>
                  <div className="form-group" style={{ flex: 1 }}>
                    <label>Semester</label>
                    <select
                      className="form-select"
                      value={performanceForm.semester}
                      onChange={(e) => setPerformanceForm({...performanceForm, semester: e.target.value})}
                    >
                      {[1,2,3,4,5,6,7,8].map(s => (
                        <option key={s} value={s}>Semester {s}</option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group" style={{ flex: 1 }}>
                    <label>Internal Marks</label>
                    <input
                      type="number"
                      className="form-input"
                      value={performanceForm.internal_marks}
                      onChange={(e) => setPerformanceForm({...performanceForm, internal_marks: e.target.value})}
                      placeholder="0-40"
                      min="0"
                      max="40"
                    />
                  </div>
                </div>
                
                <div className="form-row" style={{ display: 'flex', gap: '16px' }}>
                  <div className="form-group" style={{ flex: 1 }}>
                    <label>External Marks</label>
                    <input
                      type="number"
                      className="form-input"
                      value={performanceForm.external_marks}
                      onChange={(e) => setPerformanceForm({...performanceForm, external_marks: e.target.value})}
                      placeholder="0-60"
                      min="0"
                      max="60"
                    />
                  </div>
                  <div className="form-group" style={{ flex: 1 }}>
                    <label>Attendance %</label>
                    <input
                      type="number"
                      className="form-input"
                      value={performanceForm.attendance_percentage}
                      onChange={(e) => setPerformanceForm({...performanceForm, attendance_percentage: e.target.value})}
                      placeholder="0-100"
                      min="0"
                      max="100"
                    />
                  </div>
                </div>
                
                <div className="form-row" style={{ display: 'flex', gap: '16px' }}>
                  <div className="form-group" style={{ flex: 1 }}>
                    <label>Assignment Score</label>
                    <input
                      type="number"
                      className="form-input"
                      value={performanceForm.assignment_score}
                      onChange={(e) => setPerformanceForm({...performanceForm, assignment_score: e.target.value})}
                      placeholder="0-100"
                      min="0"
                      max="100"
                    />
                  </div>
                  <div className="form-group" style={{ flex: 1 }}>
                    <label>Lab Performance</label>
                    <input
                      type="number"
                      className="form-input"
                      value={performanceForm.lab_performance}
                      onChange={(e) => setPerformanceForm({...performanceForm, lab_performance: e.target.value})}
                      placeholder="0-100"
                      min="0"
                      max="100"
                    />
                  </div>
                </div>
                
                <div style={{ display: 'flex', gap: '12px', marginTop: '24px' }}>
                  <button 
                    type="button" 
                    className="btn btn-secondary btn-full"
                    onClick={() => setShowAddPerformance(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary btn-full">
                    Add Record
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentDetails;
