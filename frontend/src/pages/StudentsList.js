import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { studentsAPI } from '../services/api';
import toast from 'react-hot-toast';
import './Dashboard.css';

const StudentsList = () => {
  const navigate = useNavigate();
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({ page: 1, pages: 1, total: 0 });
  const [filters, setFilters] = useState({
    department: '',
    semester: ''
  });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchStudents();
  }, [pagination.page, filters]);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      const params = {
        page: pagination.page,
        per_page: 15,
        ...filters
      };
      
      // Remove empty filters
      Object.keys(params).forEach(key => {
        if (params[key] === '') delete params[key];
      });

      const response = await studentsAPI.listStudents(params);
      setStudents(response.data.students || []);
      setPagination({
        page: response.data.page,
        pages: response.data.pages,
        total: response.data.total
      });
    } catch (error) {
      console.error('Error fetching students:', error);
      toast.error('Failed to load students list');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const filteredStudents = students.filter(student => {
    if (!searchTerm) return true;
    const search = searchTerm.toLowerCase();
    return (
      student.first_name?.toLowerCase().includes(search) ||
      student.last_name?.toLowerCase().includes(search) ||
      student.roll_number?.toLowerCase().includes(search) ||
      student.department?.toLowerCase().includes(search)
    );
  });

  const handleViewStudent = (studentId) => {
    navigate(`/students/${studentId}`);
  };

  const handleExportCSV = () => {
    const headers = ['Roll Number', 'Name', 'Department', 'Semester', 'CGPA', 'Coding Ability'];
    const rows = filteredStudents.map(s => [
      s.roll_number,
      `${s.first_name} ${s.last_name}`,
      s.department,
      s.semester,
      s.current_cgpa?.toFixed(2) || '0.00',
      s.coding_ability || 'N/A'
    ]);
    
    const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'students_list.csv';
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Exported to CSV');
  };

  return (
    <div className="dashboard-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">All Students</h1>
          <p className="page-subtitle">Manage and view all registered students</p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <Link to="/admin" className="btn btn-secondary">
            ← Back to Admin
          </Link>
          <button className="btn btn-primary" onClick={handleExportCSV}>
            📥 Export CSV
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-body">
          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'flex-end' }}>
            <div className="form-group" style={{ margin: 0, flex: 1, minWidth: '200px' }}>
              <label>Search</label>
              <input
                type="text"
                className="form-input"
                placeholder="Search by name, roll number..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            
            <div className="form-group" style={{ margin: 0 }}>
              <label>Department</label>
              <select
                name="department"
                className="form-select"
                value={filters.department}
                onChange={handleFilterChange}
              >
                <option value="">All Departments</option>
                <option value="Computer Science">Computer Science</option>
                <option value="Information Technology">Information Technology</option>
                <option value="Electronics">Electronics</option>
                <option value="Mechanical">Mechanical</option>
                <option value="Civil">Civil</option>
                <option value="Electrical">Electrical</option>
              </select>
            </div>
            
            <div className="form-group" style={{ margin: 0 }}>
              <label>Semester</label>
              <select
                name="semester"
                className="form-select"
                value={filters.semester}
                onChange={handleFilterChange}
              >
                <option value="">All Semesters</option>
                {[1, 2, 3, 4, 5, 6, 7, 8].map(sem => (
                  <option key={sem} value={sem}>Semester {sem}</option>
                ))}
              </select>
            </div>
            
            <button 
              className="btn btn-secondary" 
              onClick={() => {
                setFilters({ department: '', semester: '' });
                setSearchTerm('');
              }}
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* Students Table */}
      <div className="card">
        <div className="card-header">
          <h3>Students ({pagination.total} total)</h3>
        </div>
        <div className="card-body" style={{ padding: 0 }}>
          {loading ? (
            <div className="loading-state" style={{ padding: '40px', textAlign: 'center' }}>
              <div className="spinner"></div>
              <p>Loading students...</p>
            </div>
          ) : filteredStudents.length === 0 ? (
            <div className="empty-state" style={{ padding: '40px', textAlign: 'center' }}>
              <p>No students found</p>
              <Link to="/register" className="btn btn-primary" style={{ marginTop: '16px' }}>
                + Add First Student
              </Link>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table className="data-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: 'var(--bg-secondary)' }}>
                    <th style={{ padding: '12px 16px', textAlign: 'left', borderBottom: '1px solid var(--border-color)' }}>Roll No</th>
                    <th style={{ padding: '12px 16px', textAlign: 'left', borderBottom: '1px solid var(--border-color)' }}>Name</th>
                    <th style={{ padding: '12px 16px', textAlign: 'left', borderBottom: '1px solid var(--border-color)' }}>Department</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>Semester</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>CGPA</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>Skills</th>
                    <th style={{ padding: '12px 16px', textAlign: 'center', borderBottom: '1px solid var(--border-color)' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredStudents.map((student) => (
                    <tr key={student.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                      <td style={{ padding: '12px 16px' }}>
                        <code style={{ background: 'var(--bg-secondary)', padding: '4px 8px', borderRadius: '4px' }}>
                          {student.roll_number}
                        </code>
                      </td>
                      <td style={{ padding: '12px 16px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <div style={{
                            width: '36px', height: '36px', borderRadius: '50%',
                            background: 'var(--primary-gradient)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            color: '#fff', fontWeight: 'bold'
                          }}>
                            {student.first_name?.[0]}{student.last_name?.[0]}
                          </div>
                          <div>
                            <div style={{ fontWeight: '500' }}>{student.first_name} {student.last_name}</div>
                            <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                              {student.batch || 'N/A'}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td style={{ padding: '12px 16px' }}>{student.department}</td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                        <span className="badge badge-info">Sem {student.semester}</span>
                      </td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                        <span style={{
                          fontWeight: 'bold',
                          color: student.current_cgpa >= 8 ? 'var(--success)' : 
                                 student.current_cgpa >= 6 ? 'var(--warning)' : 'var(--danger)'
                        }}>
                          {student.current_cgpa?.toFixed(2) || '0.00'}
                        </span>
                      </td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                        <span className={`badge ${
                          student.coding_ability === 'advanced' ? 'badge-success' :
                          student.coding_ability === 'intermediate' ? 'badge-warning' : 'badge-secondary'
                        }`}>
                          {student.coding_ability || 'N/A'}
                        </span>
                      </td>
                      <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                        <button
                          className="btn btn-sm btn-primary"
                          onClick={() => handleViewStudent(student.id)}
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Pagination */}
        {pagination.pages > 1 && (
          <div className="card-footer" style={{ 
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '16px', borderTop: '1px solid var(--border-color)'
          }}>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>
              Page {pagination.page} of {pagination.pages}
            </p>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                className="btn btn-secondary btn-sm"
                disabled={pagination.page === 1}
                onClick={() => setPagination(prev => ({ ...prev, page: prev.page - 1 }))}
              >
                Previous
              </button>
              <button
                className="btn btn-secondary btn-sm"
                disabled={pagination.page === pagination.pages}
                onClick={() => setPagination(prev => ({ ...prev, page: prev.page + 1 }))}
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StudentsList;
