import { useEffect, useState } from 'react';
import api from '../services/api';
import type { ModelMetrics } from '../types';

export default function AiTechnology() {
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/api/model/metrics')
      .then((res) => setMetrics(res.data))
      .catch(() => setError('Model metrics are not available yet - the model may not be trained in this environment.'));
  }, []);

  return (
    <div className="content-page">
      <h1>AI Technology</h1>

      <h2>Dataset</h2>
      <p>
        The model is trained on a stress-factor questionnaire dataset covering psychological
        (anxiety, depression, self-esteem), physiological (headache, sleep quality, breathing
        problems), environmental (living conditions, noise, safety), academic/work, and social
        support factors.
      </p>

      <h2>Deep Learning Architecture</h2>
      <pre className="arch-block">
Input Layer
  {'->'} Dense(64, ReLU)
  {'->'} Dropout(0.3)
  {'->'} Dense(32, ReLU)
  {'->'} Dropout(0.2)
  {'->'} Output Layer (Softmax / Sigmoid, chosen from the actual number of classes)
      </pre>

      <h2>Training Process</h2>
      <p>
        Data is cleaned (duplicates/missing values removed), features are scaled with
        StandardScaler, and the dataset is split into training, validation, and test sets.
        The network trains with the Adam optimizer and early stopping on validation loss.
      </p>

      <h2>Evaluation Metrics</h2>
      {error && <p className="error-text">{error}</p>}
      {metrics && (
        <div className="metrics-grid">
          <div className="metric-box"><span>Accuracy</span><strong>{(metrics.accuracy * 100).toFixed(1)}%</strong></div>
          <div className="metric-box"><span>Precision</span><strong>{(metrics.precision * 100).toFixed(1)}%</strong></div>
          <div className="metric-box"><span>Recall</span><strong>{(metrics.recall * 100).toFixed(1)}%</strong></div>
          <div className="metric-box"><span>F1-Score</span><strong>{(metrics.f1_score * 100).toFixed(1)}%</strong></div>
        </div>
      )}
      {metrics && (
        <>
          <h3>Confusion Matrix</h3>
          <table className="confusion-table">
            <tbody>
              {metrics.confusion_matrix.map((row, i) => (
                <tr key={i}>
                  {row.map((cell, j) => <td key={j}>{cell}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
          <p className="metric-caption">Evaluated on a held-out test set of {metrics.test_set_size} samples, {metrics.num_classes} classes.</p>
        </>
      )}

      <h2>Model Limitations</h2>
      <ul>
        <li>Trained on self-reported questionnaire data, which can be subjective.</li>
        <li>Not validated against clinical diagnostic criteria - it is a wellness-support tool, not a diagnostic one.</li>
        <li>Performance depends on how representative the training dataset is of the user base.</li>
      </ul>
    </div>
  );
}
