import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { reportsAPI } from '../services/api';
import toast from 'react-hot-toast';

const StudentProfile = () => {
  const { student, user } = useAuth();
  const [downloading, setDownloading] = useState(false);
  const [emailing, setEmailing] = useState(false);

  const handleDownloadPDF = async () => {
    setDownloading(true);
    try {
      const response = await reportsAPI.generatePDF();
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `academic_report_${student?.roll_number || 'student'}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      toast.success('Report downloaded successfully!');
    } catch (error) {
      toast.error('Failed to download report');
    } finally {
      setDownloading(false);
    }
  };

  const handleEmailReport = async () => {
    setEmailing(true);
    try {
      await reportsAPI.emailReport();
      toast.success('Report sent to your email!');
    } catch (error) {
      toast.error('Failed to send email');
    } finally {
      setEmailing(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2 style={{ margin: 0, color: 'var(--text-primary)' }}>Student Profile</h2>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="btn-primary"
            style={{
              padding: '10px 20px',
              borderRadius: '8px',
              border: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              cursor: downloading ? 'not-allowed' : 'pointer',
              opacity: downloading ? 0.7 : 1
            }}
          >
            📄 {downloading ? 'Generating...' : 'Download PDF'}
          </button>
          <button
            onClick={handleEmailReport}
            disabled={emailing}
            className="btn-secondary"
            style={{
              padding: '10px 20px',
              borderRadius: '8px',
              border: '1px solid var(--border-color)',
              background: 'var(--bg-card)',
              color: 'var(--text-primary)',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              cursor: emailing ? 'not-allowed' : 'pointer',
              opacity: emailing ? 0.7 : 1
            }}
          >
            ✉️ {emailing ? 'Sending...' : 'Email Report'}
          </button>
        </div>
      </div>

      {student && (
        <>
          {/* Profile Card */}
          <div className="glass" style={{ padding: '32px', borderRadius: '16px', marginBottom: '24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '24px', marginBottom: '24px' }}>
              <div style={{
                width: '80px',
                height: '80px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, var(--primary-start), var(--primary-end))',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '32px',
                color: 'white',
                fontWeight: 'bold'
              }}>
                {student.first_name?.charAt(0)}{student.last_name?.charAt(0)}
              </div>
              <div>
                <h3 style={{ margin: 0, fontSize: '24px', color: 'var(--text-primary)' }}>
                  {student.full_name || `${student.first_name} ${student.last_name}`}
                </h3>
                <p style={{ margin: '4px 0 0', color: 'var(--text-secondary)' }}>
                  {student.roll_number} • {student.department}
                </p>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
              <InfoItem label="Roll Number" value={student.roll_number} icon="🎓" />
              <InfoItem label="Department" value={student.department} icon="🏛️" />
              <InfoItem label="Semester" value={student.semester} icon="📅" />
              <InfoItem label="Batch" value={student.batch || 'N/A'} icon="📚" />
              <InfoItem label="Current CGPA" value={student.current_cgpa?.toFixed(2) || 'N/A'} icon="📊" highlight />
              <InfoItem label="Coding Ability" value={student.coding_ability || 'Not specified'} icon="💻" />
            </div>
          </div>

          {/* Additional Info */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
            {/* Skills & Interests */}
            <div className="glass" style={{ padding: '24px', borderRadius: '16px' }}>
              <h4 style={{ margin: '0 0 16px', color: 'var(--text-primary)' }}>🎯 Skills & Interests</h4>
              <div style={{ marginBottom: '16px' }}>
                <p style={{ color: 'var(--text-secondary)', margin: '0 0 8px', fontSize: '14px' }}>Skills</p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {(student.skills || 'Python, JavaScript').split(',').map((skill, i) => (
                    <span key={i} style={{
                      padding: '4px 12px',
                      background: 'var(--bg-hover)',
                      borderRadius: '16px',
                      fontSize: '14px',
                      color: 'var(--text-primary)'
                    }}>
                      {skill.trim()}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <p style={{ color: 'var(--text-secondary)', margin: '0 0 8px', fontSize: '14px' }}>Interests</p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {(student.interests || 'AI, Web Development').split(',').map((interest, i) => (
                    <span key={i} style={{
                      padding: '4px 12px',
                      background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))',
                      borderRadius: '16px',
                      fontSize: '14px',
                      color: 'var(--primary-start)'
                    }}>
                      {interest.trim()}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Account Info */}
            <div className="glass" style={{ padding: '24px', borderRadius: '16px' }}>
              <h4 style={{ margin: '0 0 16px', color: 'var(--text-primary)' }}>👤 Account Information</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>Email</span>
                  <span style={{ color: 'var(--text-primary)' }}>{user?.email || 'N/A'}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>Username</span>
                  <span style={{ color: 'var(--text-primary)' }}>{user?.username || 'N/A'}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>Role</span>
                  <span style={{
                    padding: '2px 8px',
                    background: user?.role === 'admin' ? 'rgba(255, 107, 107, 0.1)' : 'rgba(56, 239, 125, 0.1)',
                    color: user?.role === 'admin' ? '#ff6b6b' : '#38ef7d',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}>
                    {user?.role?.toUpperCase() || 'STUDENT'}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>Status</span>
                  <span style={{
                    padding: '2px 8px',
                    background: 'rgba(56, 239, 125, 0.1)',
                    color: '#38ef7d',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}>
                    ACTIVE
                  </span>
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {!student && (
        <div className="glass" style={{ padding: '48px', borderRadius: '16px', textAlign: 'center' }}>
          <p style={{ color: 'var(--text-secondary)', fontSize: '18px' }}>
            No student profile found. Please contact admin.
          </p>
        </div>
      )}
    </div>
  );
};

const InfoItem = ({ label, value, icon, highlight }) => (
  <div style={{
    padding: '16px',
    background: highlight ? 'linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))' : 'var(--bg-hover)',
    borderRadius: '12px',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
      <span>{icon}</span>
      <span style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>{label}</span>
    </div>
    <span style={{
      fontSize: highlight ? '24px' : '16px',
      fontWeight: highlight ? '600' : '500',
      color: 'var(--text-primary)'
    }}>
      {value}
    </span>
  </div>
);

export default StudentProfile;
