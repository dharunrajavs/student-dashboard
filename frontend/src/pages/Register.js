import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import './Auth.css';

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    // Account Info
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    role: 'student',
    // Personal Info
    first_name: '',
    last_name: '',
    gender: '',
    phone: '',
    // Academic Info
    roll_number: '',
    department: '',
    semester: '1',
    batch: '',
    // Additional Info
    coding_ability: 'intermediate',
    interests: '',
    skills: '',
    family_income: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }

    if (formData.password.length < 6) {
      toast.error('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      const userData = {
        email: formData.email,
        username: formData.username,
        password: formData.password,
        role: formData.role
      };

      if (formData.role === 'student') {
        userData.student_data = {
          first_name: formData.first_name,
          last_name: formData.last_name,
          roll_number: formData.roll_number,
          department: formData.department,
          semester: parseInt(formData.semester),
          batch: formData.batch,
          gender: formData.gender,
          phone: formData.phone,
          coding_ability: formData.coding_ability,
          interests: formData.interests,
          skills: formData.skills,
          family_income: formData.family_income ? parseFloat(formData.family_income) : null
        };
      }

      const result = await register(userData);
      
      if (result.success) {
        toast.success('Registration successful! Please login.');
        navigate('/login');
      } else {
        toast.error(result.error || 'Registration failed');
      }
    } catch (error) {
      toast.error('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-background">
        <div className="gradient-blob blob-1"></div>
        <div className="gradient-blob blob-2"></div>
        <div className="gradient-blob blob-3"></div>
      </div>
      
      <div className="auth-card glass animate-fade-in" style={{ maxWidth: '500px' }}>
        <div className="auth-header">
          <h1 className="auth-logo">🎓</h1>
          <h2 className="auth-title">Create Account</h2>
          <p className="auth-subtitle">Join AI Academic Intelligence Platform</p>
          
          {/* Step Indicator */}
          <div className="step-indicator" style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '12px' }}>
            {[1, 2, 3].map(s => (
              <div key={s} style={{
                width: '32px', height: '32px', borderRadius: '50%',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: step >= s ? 'var(--primary)' : 'var(--bg-secondary)',
                color: step >= s ? '#fff' : 'var(--text-secondary)',
                fontWeight: 'bold', fontSize: '14px'
              }}>{s}</div>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          
          {/* Step 1: Personal Info */}
          {step === 1 && (
            <>
              <h3 style={{ marginBottom: '16px', color: 'var(--text-primary)' }}>Personal Information</h3>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="first_name">First Name *</label>
                  <input type="text" id="first_name" name="first_name" value={formData.first_name} onChange={handleChange} required className="form-input" />
                </div>
                <div className="form-group">
                  <label htmlFor="last_name">Last Name *</label>
                  <input type="text" id="last_name" name="last_name" value={formData.last_name} onChange={handleChange} required className="form-input" />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="gender">Gender</label>
                  <select id="gender" name="gender" value={formData.gender} onChange={handleChange} className="form-select">
                    <option value="">Select...</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="phone">Phone Number</label>
                  <input type="tel" id="phone" name="phone" value={formData.phone} onChange={handleChange} className="form-input" placeholder="+91 XXXXX XXXXX" />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="email">Email *</label>
                <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} required className="form-input" />
              </div>

              <button type="button" className="btn btn-primary btn-full" onClick={() => {
                if (formData.first_name && formData.last_name && formData.email) {
                  setStep(2);
                } else {
                  toast.error('Please fill required fields');
                }
              }}>Next: Academic Info</button>
            </>
          )}

          {/* Step 2: Academic Info */}
          {step === 2 && (
            <>
              <h3 style={{ marginBottom: '16px', color: 'var(--text-primary)' }}>Academic Information</h3>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="roll_number">Roll Number *</label>
                  <input type="text" id="roll_number" name="roll_number" value={formData.roll_number} onChange={handleChange} required className="form-input" placeholder="e.g., CS2024001" />
                </div>
                <div className="form-group">
                  <label htmlFor="batch">Batch/Year *</label>
                  <input type="text" id="batch" name="batch" value={formData.batch} onChange={handleChange} required className="form-input" placeholder="e.g., 2024-2028" />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="department">Department *</label>
                  <select id="department" name="department" value={formData.department} onChange={handleChange} required className="form-select">
                    <option value="">Select...</option>
                    <option value="Computer Science">Computer Science</option>
                    <option value="Information Technology">Information Technology</option>
                    <option value="Electronics">Electronics</option>
                    <option value="Mechanical">Mechanical</option>
                    <option value="Civil">Civil</option>
                    <option value="Electrical">Electrical</option>
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="semester">Semester *</label>
                  <select id="semester" name="semester" value={formData.semester} onChange={handleChange} required className="form-select">
                    {[1, 2, 3, 4, 5, 6, 7, 8].map(sem => (
                      <option key={sem} value={sem}>Semester {sem}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="coding_ability">Coding Ability</label>
                  <select id="coding_ability" name="coding_ability" value={formData.coding_ability} onChange={handleChange} className="form-select">
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="family_income">Family Income (₹/year)</label>
                  <input type="number" id="family_income" name="family_income" value={formData.family_income} onChange={handleChange} className="form-input" placeholder="Annual income" />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="interests">Interests</label>
                <input type="text" id="interests" name="interests" value={formData.interests} onChange={handleChange} className="form-input" placeholder="e.g., AI, Web Development, Robotics" />
              </div>

              <div className="form-group">
                <label htmlFor="skills">Skills</label>
                <input type="text" id="skills" name="skills" value={formData.skills} onChange={handleChange} className="form-input" placeholder="e.g., Python, JavaScript, Data Analysis" />
              </div>

              <div style={{ display: 'flex', gap: '12px' }}>
                <button type="button" className="btn btn-secondary btn-full" onClick={() => setStep(1)}>Back</button>
                <button type="button" className="btn btn-primary btn-full" onClick={() => {
                  if (formData.roll_number && formData.department && formData.batch) {
                    setStep(3);
                  } else {
                    toast.error('Please fill required fields');
                  }
                }}>Next: Account Setup</button>
              </div>
            </>
          )}

          {/* Step 3: Account Setup */}
          {step === 3 && (
            <>
              <h3 style={{ marginBottom: '16px', color: 'var(--text-primary)' }}>Account Setup</h3>
              
              <div className="form-group">
                <label htmlFor="username">Username *</label>
                <input type="text" id="username" name="username" value={formData.username} onChange={handleChange} required className="form-input" />
              </div>

              <div className="form-group">
                <label htmlFor="password">Password *</label>
                <input type="password" id="password" name="password" value={formData.password} onChange={handleChange} required className="form-input" />
                <small style={{ color: 'var(--text-secondary)' }}>Minimum 6 characters</small>
              </div>

              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password *</label>
                <input type="password" id="confirmPassword" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} required className="form-input" />
              </div>

              <div style={{ display: 'flex', gap: '12px' }}>
                <button type="button" className="btn btn-secondary btn-full" onClick={() => setStep(2)}>Back</button>
                <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
                  {loading ? 'Creating Account...' : 'Register'}
                </button>
              </div>
            </>
          )}
        </form>

        <div className="auth-footer">
          <p>
            Already have an account? <Link to="/login" className="auth-link">Login</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
