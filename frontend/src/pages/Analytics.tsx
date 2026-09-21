import { useEffect, useState } from 'react';
import '../styles/analytics.css';
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  BarChart, Bar, PieChart, Pie, Cell,
} from 'recharts';
import api from '../services/api';
import type { AnalyticsSummary } from '../types';

interface HistoryPoint {
  date: string;
  stress_score: number;
  level: string;
}

const PIE_COLORS: Record<string, string> = { Low: '#3fb27f', Moderate: '#e0a341', High: '#e05252' };

export default function Analytics() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [history, setHistory] = useState<HistoryPoint[]>([]);

  useEffect(() => {
    api.get('/api/analytics/summary').then((res) => setSummary(res.data)).catch(() => {});
    api.get('/api/analytics/history').then((res) => setHistory(res.data)).catch(() => {});
  }, []);

  if (!summary?.has_data) {
    return (
      <div className="content-page">
        <h1>Analytics</h1>
        <p>Take at least one assessment to see your analytics here.</p>
      </div>
    );
  }

  const factorData = Object.entries(summary.factor_averages || {}).map(([name, value]) => ({ name, value }));
  const pieData = Object.entries(summary.category_distribution || {}).map(([name, value]) => ({ name, value }));
  const lineData = history.map((h) => ({ date: new Date(h.date).toLocaleDateString(), score: h.stress_score }));

  return (
    <div className="content-page">
      <h1>Analytics</h1>

      <h2>Factor Analysis (Averages)</h2>
      <div className="chart-box">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={factorData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" tick={{ fontSize: 11 }} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#4d6bfe" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {lineData.length > 1 && (
        <>
          <h2>Stress History</h2>
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={lineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#4d6bfe" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </>
      )}

      <h2>Category Distribution</h2>
      <div className="chart-box">
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie data={pieData} dataKey="value" nameKey="name" outerRadius={100} label>
              {pieData.map((entry) => (
                <Cell key={entry.name} fill={PIE_COLORS[entry.name] || '#8884d8'} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
