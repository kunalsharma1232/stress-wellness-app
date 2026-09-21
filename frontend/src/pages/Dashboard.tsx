import { useEffect, useState } from 'react';
import '../styles/dashboard.css';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import StressCard from '../components/StressCard';
import type { AnalyticsSummary, HistoryItem } from '../types';

export default function Dashboard() {
  const { user } = useAuth();
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [recent, setRecent] = useState<HistoryItem[]>([]);

  useEffect(() => {
    api.get('/api/analytics/summary').then((res) => setSummary(res.data)).catch(() => {});
    api.get('/api/predictions/history').then((res) => setRecent(res.data.slice(0, 5))).catch(() => {});
  }, []);

  return (
    <div className="dashboard-page">
      <h1>Welcome, {user?.full_name}</h1>

      {summary?.has_data ? (
        <div className="stat-grid">
          <StressCard title="Latest Stress Score" value={`${summary.latest_score}/100`} />
          <StressCard
            title="Current Stress Level"
            value={summary.latest_level || '-'}
            accent={summary.latest_level === 'High' ? 'danger' : summary.latest_level === 'Moderate' ? 'warning' : 'success'}
          />
          <StressCard title="Number of Assessments" value={summary.total_assessments || 0} />
        </div>
      ) : (
        <div className="empty-state">
          <p>You haven't taken an assessment yet.</p>
          <Link to="/check-stress" className="btn btn-primary">Check My Stress</Link>
        </div>
      )}

      <div className="quick-actions">
        <Link to="/check-stress" className="btn btn-primary">Check My Stress</Link>
        <Link to="/analytics" className="btn btn-outline">View Analytics</Link>
        <Link to="/history" className="btn btn-outline">Prediction History</Link>
        <Link to="/wellness-assistant" className="btn btn-outline">AI Wellness Assistant</Link>
      </div>

      {recent.length > 0 && (
        <div className="recent-history">
          <h2>Recent Assessments</h2>
          <table className="data-table">
            <thead>
              <tr><th>Date</th><th>Stress Score</th><th>Level</th></tr>
            </thead>
            <tbody>
              {recent.map((r) => (
                <tr key={r.id}>
                  <td>{new Date(r.created_at).toLocaleDateString()}</td>
                  <td>{r.stress_score}</td>
                  <td>{r.prediction}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
