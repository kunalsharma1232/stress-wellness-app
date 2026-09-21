import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import type { HistoryItem } from '../types';

export default function History() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/api/predictions/history').then((res) => setItems(res.data)).catch(() => {});
  }, []);

  async function openDetail(id: string) {
    const { data } = await api.get(`/api/predictions/${id}`);
    navigate('/stress-result', {
      state: {
        result: {
          id: data.id,
          predicted_label: data.prediction,
          stress_score: data.stress_score,
          probabilities: data.probabilities,
          age_group: data.age_group,
          created_at: data.created_at,
          recommendations: [],
        },
      },
    });
  }

  if (items.length === 0) {
    return (
      <div className="content-page">
        <h1>Prediction History</h1>
        <p>No assessments yet.</p>
      </div>
    );
  }

  return (
    <div className="content-page">
      <h1>Prediction History</h1>
      <table className="data-table">
        <thead>
          <tr><th>Date</th><th>Age</th><th>Stress Score</th><th>Level</th><th>Action</th></tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{new Date(item.created_at).toLocaleDateString()}</td>
              <td>{item.age}</td>
              <td>{item.stress_score}</td>
              <td>{item.prediction}</td>
              <td><button className="btn btn-sm btn-outline" onClick={() => openDetail(item.id)}>View</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
