import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { predictionsAPI, analyticsAPI } from '../services/api';
import { TrendingUp, Award, AlertCircle, BarChart3, Sparkles, Target, Zap, Calendar, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import './Dashboard.css';

const Dashboard = () => {
  const { user, student } = useAuth();
  const [loading, setLoading] = useState(true);
  const [riskScore, setRiskScore] = useState(null);
  const [trends, setTrends] = useState(null);
  const [comparison, setComparison] = useState(null);

  useEffect(() => {
    if (student?.id) {
      loadDashboardData();
    } else {
      setLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [student]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load risk score
      try {
        const riskResponse = await predictionsAPI.calculateRiskScore(student.id);
        setRiskScore(riskResponse.data);
      } catch (err) {
        console.log('Risk score not available yet');
        setRiskScore({ risk_score: 25, risk_level: 'Low', factors: [], recommendations: ['Add more performance data'] });
      }
      
      // Load trends
      try {
        const trendsResponse = await analyticsAPI.getTrends(student.id);
        setTrends(trendsResponse.data);
      } catch (err) {
        console.log('Trends not available yet');
        setTrends({ marks_trend: [], trend_direction: 'stable', average_marks: 0, average_attendance: 0 });
      }
      
      // Load comparison
      try {
        const comparisonResponse = await analyticsAPI.getComparison(student.id);
        setComparison(comparisonResponse.data);
      } catch (err) {
        console.log('Comparison not available yet');
        setComparison({ percentile: 75, class_average: 70 });
      }
      
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score) => {
    if (score >= 70) return '#ef4444';
    if (score >= 50) return '#f59e0b';
    if (score >= 30) return '#eab308';
    return '#10b981';
  };

  const getRiskGradient = (score) => {
    if (score >= 70) return 'linear-gradient(135deg, #ef4444, #dc2626)';
    if (score >= 50) return 'linear-gradient(135deg, #f59e0b, #d97706)';
    if (score >= 30) return 'linear-gradient(135deg, #eab308, #ca8a04)';
    return 'linear-gradient(135deg, #10b981, #059669)';
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner">
          <div className="spinner-ring"></div>
          <Sparkles className="spinner-icon" size={24} />
        </div>
        <p className="loading-text">Loading your dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-background">
          <div className="hero-gradient"></div>
          <div className="hero-pattern"></div>
        </div>
        <div className="hero-content">
          <div className="hero-text">
            <span className="hero-greeting">Welcome back</span>
            <h1 className="hero-title">
              {student?.first_name || user?.username}
              <span className="hero-wave">👋</span>
            </h1>
            <p className="hero-subtitle">
              Here's your academic performance overview for this semester
            </p>
          </div>
          <div className="hero-badges">
            <div className="hero-badge">
              <Calendar size={16} />
              <span>Semester {student?.semester || 1}</span>
            </div>
            <div className="hero-badge highlight">
              <Target size={16} />
              <span>CGPA: {student?.current_cgpa?.toFixed(2) || '0.00'}</span>
            </div>
          </div>
        </div>
        <div className="hero-illustration">
          <div className="floating-card card-1">
            <Zap size={20} />
          </div>
          <div className="floating-card card-2">
            <Award size={20} />
          </div>
          <div className="floating-card card-3">
            <TrendingUp size={20} />
          </div>
        </div>
      </div>

      {/* Quick Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-card-glow glow-purple"></div>
          <div className="stat-header">
            <div className="stat-icon purple">
              <TrendingUp size={22} />
            </div>
            <div className={`stat-trend ${trends?.marks_change >= 0 ? 'positive' : 'negative'}`}>
              {trends?.marks_change >= 0 ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
              <span>{Math.abs(trends?.marks_change || 0).toFixed(1)}%</span>
            </div>
          </div>
          <div className="stat-body">
            <h3 className="stat-title">Performance Trend</h3>
            <p className="stat-value capitalize">{trends?.trend_direction || 'Stable'}</p>
            <p className="stat-desc">from last record</p>
          </div>
          <div className="stat-sparkline">
            <div className="sparkline-bar" style={{ height: '40%' }}></div>
            <div className="sparkline-bar" style={{ height: '60%' }}></div>
            <div className="sparkline-bar" style={{ height: '45%' }}></div>
            <div className="sparkline-bar" style={{ height: '80%' }}></div>
            <div className="sparkline-bar" style={{ height: '65%' }}></div>
            <div className="sparkline-bar active" style={{ height: '90%' }}></div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card-glow glow-green"></div>
          <div className="stat-header">
            <div className="stat-icon green">
              <Award size={22} />
            </div>
            <div className="stat-trend positive">
              <ArrowUpRight size={16} />
              <span>Top {100 - (comparison?.percentile || 0)}%</span>
            </div>
          </div>
          <div className="stat-body">
            <h3 className="stat-title">Class Percentile</h3>
            <p className="stat-value">{comparison?.percentile?.toFixed(0) || '0'}%</p>
            <p className="stat-desc">
              {comparison?.performance_status === 'above_average' ? 'Above' : 'Below'} class average
            </p>
          </div>
          <div className="stat-progress">
            <div className="progress-track">
              <div className="progress-fill green" style={{ width: `${comparison?.percentile || 0}%` }}></div>
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card-glow" style={{ background: getRiskColor(riskScore?.risk_score) }}></div>
          <div className="stat-header">
            <div className="stat-icon" style={{ background: getRiskGradient(riskScore?.risk_score) }}>
              <AlertCircle size={22} />
            </div>
            <span className={`stat-badge ${riskScore?.risk_level?.toLowerCase()}`}>
              {riskScore?.risk_level || 'Unknown'}
            </span>
          </div>
          <div className="stat-body">
            <h3 className="stat-title">Risk Score</h3>
            <p className="stat-value">{riskScore?.risk_score?.toFixed(0) || '0'}</p>
            <p className="stat-desc">risk assessment level</p>
          </div>
          <div className="stat-meter">
            <div className="meter-track">
              <div 
                className="meter-fill" 
                style={{ 
                  width: `${riskScore?.risk_score || 0}%`,
                  background: getRiskGradient(riskScore?.risk_score)
                }}
              ></div>
            </div>
            <div className="meter-labels">
              <span>Low</span>
              <span>High</span>
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card-glow glow-amber"></div>
          <div className="stat-header">
            <div className="stat-icon amber">
              <BarChart3 size={22} />
            </div>
            <span className={`stat-badge ${(riskScore?.metrics?.average_attendance || 0) >= 75 ? 'good' : 'warning'}`}>
              {(riskScore?.metrics?.average_attendance || 0) >= 75 ? 'Good' : 'Low'}
            </span>
          </div>
          <div className="stat-body">
            <h3 className="stat-title">Avg. Attendance</h3>
            <p className="stat-value">{riskScore?.metrics?.average_attendance?.toFixed(1) || '0'}%</p>
            <p className="stat-desc">
              {(riskScore?.metrics?.average_attendance || 0) >= 75 ? 'Keep it up!' : 'Needs improvement'}
            </p>
          </div>
          <div className="stat-progress">
            <div className="progress-track">
              <div 
                className="progress-fill amber" 
                style={{ width: `${riskScore?.metrics?.average_attendance || 0}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-card">
          <div className="chart-header">
            <div className="chart-title-group">
              <h3 className="chart-title">Performance Trend</h3>
              <p className="chart-subtitle">Your marks over time</p>
            </div>
            <div className="chart-legend">
              <span className="legend-dot purple"></span>
              <span>Marks</span>
            </div>
          </div>
          <div className="chart-body">
            {trends && trends.marks_trend && trends.marks_trend.length > 0 ? (
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={trends.marks_trend.map((marks, index) => ({ name: `Record ${index + 1}`, marks }))}>
                  <defs>
                    <linearGradient id="marksGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                      <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" vertical={false} />
                  <XAxis 
                    dataKey="name" 
                    stroke="#64748b"
                    fontSize={12}
                    tickLine={false}
                    axisLine={{ stroke: 'rgba(148, 163, 184, 0.1)' }}
                  />
                  <YAxis 
                    stroke="#64748b"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      background: 'rgba(15, 23, 42, 0.95)', 
                      border: '1px solid rgba(148, 163, 184, 0.1)',
                      borderRadius: '12px',
                      boxShadow: '0 20px 40px rgba(0,0,0,0.3)'
                    }}
                    labelStyle={{ color: '#fff', fontWeight: 600 }}
                    itemStyle={{ color: '#8b5cf6' }}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="marks" 
                    stroke="#8b5cf6" 
                    strokeWidth={3}
                    fill="url(#marksGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-chart">
                <div className="empty-icon">
                  <TrendingUp size={32} />
                </div>
                <p>No performance data available yet</p>
                <span>Start adding records to see your trend</span>
              </div>
            )}
          </div>
        </div>

        <div className="chart-card">
          <div className="chart-header">
            <div className="chart-title-group">
              <h3 className="chart-title">Class Comparison</h3>
              <p className="chart-subtitle">How you compare to others</p>
            </div>
          </div>
          <div className="chart-body">
            {comparison && (
              <ResponsiveContainer width="100%" height={280}>
                <BarChart 
                  data={[
                    { name: 'Your CGPA', value: comparison.student_cgpa, fill: 'url(#barGradient1)' },
                    { name: 'Class Avg', value: comparison.class_average, fill: 'url(#barGradient2)' },
                    { name: 'Dept Avg', value: comparison.department_average, fill: 'url(#barGradient3)' }
                  ]}
                  barSize={40}
                >
                  <defs>
                    <linearGradient id="barGradient1" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#8b5cf6"/>
                      <stop offset="100%" stopColor="#6366f1"/>
                    </linearGradient>
                    <linearGradient id="barGradient2" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#10b981"/>
                      <stop offset="100%" stopColor="#059669"/>
                    </linearGradient>
                    <linearGradient id="barGradient3" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#f59e0b"/>
                      <stop offset="100%" stopColor="#d97706"/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" vertical={false} />
                  <XAxis 
                    dataKey="name" 
                    stroke="#64748b"
                    fontSize={12}
                    tickLine={false}
                    axisLine={{ stroke: 'rgba(148, 163, 184, 0.1)' }}
                  />
                  <YAxis 
                    stroke="#64748b"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                    domain={[0, 10]}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      background: 'rgba(15, 23, 42, 0.95)', 
                      border: '1px solid rgba(148, 163, 184, 0.1)',
                      borderRadius: '12px',
                      boxShadow: '0 20px 40px rgba(0,0,0,0.3)'
                    }}
                    labelStyle={{ color: '#fff', fontWeight: 600 }}
                    cursor={{ fill: 'rgba(148, 163, 184, 0.05)' }}
                  />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      </div>

      {/* Insights Section */}
      <div className="insights-section">
        {/* Risk Factors */}
        {riskScore && riskScore.factors && riskScore.factors.length > 0 && (
          <div className="insight-card risk">
            <div className="insight-header">
              <div className="insight-icon risk">
                <AlertCircle size={20} />
              </div>
              <h3 className="insight-title">Risk Factors</h3>
              <span className="insight-count">{riskScore.factors.length}</span>
            </div>
            <div className="insight-body">
              {riskScore.factors.map((factor, index) => (
                <div key={index} className="insight-item risk">
                  <div className="insight-bullet"></div>
                  <span>{factor}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        {riskScore && riskScore.recommendations && riskScore.recommendations.length > 0 && (
          <div className="insight-card success">
            <div className="insight-header">
              <div className="insight-icon success">
                <Sparkles size={20} />
              </div>
              <h3 className="insight-title">AI Recommendations</h3>
              <span className="insight-count">{riskScore.recommendations.length}</span>
            </div>
            <div className="insight-body">
              {riskScore.recommendations.map((rec, index) => (
                <div key={index} className="insight-item success">
                  <div className="insight-number">{index + 1}</div>
                  <span>{rec}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
