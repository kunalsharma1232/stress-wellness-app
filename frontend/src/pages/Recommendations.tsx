import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useEffect } from 'react';
import api from '../services/api';

export default function Recommendations() {
  const { assessmentId } = useParams();
  const [recs, setRecs] = useState<string[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!assessmentId) return;
    api.get(`/api/recommendations/${assessmentId}`)
      .then((res) => setRecs(res.data.recommendations))
      .catch(() => setError('No recommendations found for this assessment.'));
  }, [assessmentId]);

  return (
    <div className="content-page">
      <h1>Wellness Recommendations</h1>
      {error && <p>{error}</p>}
      <ul className="recommendations-list">
        {recs.map((r, i) => <li key={i}>{r}</li>)}
      </ul>
    </div>
  );
}
