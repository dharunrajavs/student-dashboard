import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { analyticsAPI } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Analytics = () => {
  const { student } = useAuth();
  const [heatmapData, setHeatmapData] = useState(null);
  const [leaderboard, setLeaderboard] = useState(null);

  // Default student ID if student data not loaded
  const studentId = student?.id || 1;

  useEffect(() => {
    loadAnalytics();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [studentId]);

  const loadAnalytics = async () => {
    try {
      const heatmap = await analyticsAPI.getHeatmap(studentId);
      setHeatmapData(heatmap.data);

      const leaders = await analyticsAPI.getLeaderboard({ limit: 10 });
      setLeaderboard(leaders.data);
    } catch (error) {
      console.error('Failed to load analytics', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Performance Analytics</h2>

      {/* Performance Heatmap */}
      <div className="glass" style={{ padding: '24px', borderRadius: '12px', marginTop: '20px' }}>
        <h3>📈 Performance Heatmap</h3>
        {heatmapData && heatmapData.subject_performance && heatmapData.subject_performance.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={heatmapData.subject_performance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="subject" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="average_marks" fill="var(--primary)" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p>No performance data available</p>
        )}
      </div>

      {/* Leaderboard */}
      <div className="glass" style={{ padding: '24px', borderRadius: '12px', marginTop: '20px' }}>
        <h3>🏆 Top Performers</h3>
        {leaderboard && leaderboard.leaderboard && leaderboard.leaderboard.length > 0 ? (
          <table style={{ width: '100%', marginTop: '16px', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--border-color)' }}>
                <th style={{ padding: '12px', textAlign: 'left' }}>Rank</th>
                <th style={{ padding: '12px', textAlign: 'left' }}>Name</th>
                <th style={{ padding: '12px', textAlign: 'left' }}>Department</th>
                <th style={{ padding: '12px', textAlign: 'left' }}>CGPA</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.leaderboard.map((entry) => (
                <tr key={entry.rank} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '12px' }}>{entry.rank}</td>
                  <td style={{ padding: '12px' }}>{entry.name}</td>
                  <td style={{ padding: '12px' }}>{entry.department}</td>
                  <td style={{ padding: '12px', fontWeight: 'bold', color: 'var(--primary)' }}>{entry.cgpa}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No leaderboard data available</p>
        )}
      </div>
    </div>
  );
};

export default Analytics;
