import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { adminAPI } from '../services/api';
import toast from 'react-hot-toast';

const AdminDashboard = () => {
  const [dashboard, setDashboard] = useState(null);
  const [atRiskStudents, setAtRiskStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    try {
      setLoading(true);
      const dashResponse = await adminAPI.getDashboard();
      setDashboard(dashResponse.data);

      const riskResponse = await adminAPI.getAtRiskStudents(70);
      setAtRiskStudents(riskResponse.data.at_risk_students);
    } catch (error) {
      toast.error('Failed to load admin data');
    } finally {
      setLoading(false);
    }
  };

  const exportEligible = async () => {
    try {
      const response = await adminAPI.exportEligible();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'scholarship_eligible.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('Export successful!');
    } catch (error) {
      toast.error('Failed to export');
    }
  };

  if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2>Admin Dashboard</h2>
        <Link to="/students" className="btn btn-primary">
          👥 View All Students
        </Link>
      </div>

      {/* Statistics */}
      {dashboard && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginTop: '20px' }}>
          <div className="glass" style={{ padding: '20px', borderRadius: '12px', textAlign: 'center' }}>
            <h3 style={{ fontSize: '32px', color: 'var(--primary)' }}>{dashboard.total_students}</h3>
            <p>Total Students</p>
          </div>
          <div className="glass" style={{ padding: '20px', borderRadius: '12px', textAlign: 'center' }}>
            <h3 style={{ fontSize: '32px', color: 'var(--danger)' }}>{dashboard.at_risk_students}</h3>
            <p>At-Risk Students</p>
          </div>
          <div className="glass" style={{ padding: '20px', borderRadius: '12px', textAlign: 'center' }}>
            <h3 style={{ fontSize: '32px', color: 'var(--success)' }}>{dashboard.excellent_students}</h3>
            <p>Excellent Performers</p>
          </div>
          <div className="glass" style={{ padding: '20px', borderRadius: '12px', textAlign: 'center' }}>
            <h3 style={{ fontSize: '32px', color: 'var(--info)' }}>{dashboard.average_cgpa}</h3>
            <p>Average CGPA</p>
          </div>
        </div>
      )}

      {/* At-Risk Students */}
      <div className="glass" style={{ padding: '24px', borderRadius: '12px', marginTop: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3>⚠️ At-Risk Students</h3>
          <button onClick={exportEligible} className="btn btn-primary">
            Export Eligible Students
          </button>
        </div>
        {atRiskStudents && atRiskStudents.length > 0 ? (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--border-color)' }}>
                <th style={{ padding: '12px', textAlign: 'left' }}>Name</th>
                <th style={{ padding: '12px', textAlign: 'left' }}>Department</th>
                <th style={{ padding: '12px', textAlign: 'left' }}>Risk Score</th>
                <th style={{ padding: '12px', textAlign: 'left' }}>Risk Level</th>
              </tr>
            </thead>
            <tbody>
              {atRiskStudents.map((item, index) => (
                <tr key={index} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '12px' }}>{item.student.full_name}</td>
                  <td style={{ padding: '12px' }}>{item.student.department}</td>
                  <td style={{ padding: '12px', fontWeight: 'bold', color: 'var(--danger)' }}>
                    {item.risk_data.risk_score.toFixed(0)}
                  </td>
                  <td style={{ padding: '12px' }}>{item.risk_data.risk_level}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No at-risk students found</p>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
