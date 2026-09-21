import { useLocation, Navigate, Link } from 'react-router-dom';
import StressGauge from '../components/StressGauge';
import type { PredictionResult } from '../types';

export default function StressResult() {
  const location = useLocation();
  const result = (location.state as { result?: PredictionResult } | null)?.result;

  if (!result) {
    return <Navigate to="/check-stress" replace />;
  }

  return (
    <div className="result-page">
      <h1>Your Stress Assessment</h1>

      <div className="result-top">
        <StressGauge score={result.stress_score} level={result.predicted_label} />

        <div className="result-details">
          <p><strong>AI-derived stress score:</strong> {result.stress_score}/100</p>
          <p className="result-note">
            This is a normalized presentation score derived from the model's class
            probabilities - not a medical measurement.
          </p>
          <p><strong>Predicted category:</strong> {result.predicted_label}</p>
          <p><strong>Age group:</strong> {result.age_group}</p>
          <p><strong>Assessment date:</strong> {new Date(result.created_at).toLocaleString()}</p>
        </div>
      </div>

      <h2>Personalized Wellness Recommendations</h2>
      <ul className="recommendations-list">
        {result.recommendations.map((r, i) => <li key={i}>{r}</li>)}
      </ul>

      <div className="result-actions">
        <Link to="/analytics" className="btn btn-outline">View Analytics</Link>
        <Link to="/wellness-assistant" className="btn btn-outline">Talk to Wellness Assistant</Link>
        <Link to="/dashboard" className="btn btn-primary">Back to Dashboard</Link>
      </div>
    </div>
  );
}
