import { useMemo, useState } from 'react';
import '../styles/questionnaire.css';
import { useLocation, useNavigate } from 'react-router-dom';
import ProgressBar from '../components/ProgressBar';
import QuestionCard from '../components/QuestionCard';
import { getAgeGroup, getQuestionsForAgeGroup } from '../hooks/useAgeGroup';
import api from '../services/api';

const GROUP_SIZE = 3;

export default function Questionnaire() {
  const location = useLocation();
  const navigate = useNavigate();
  const age = (location.state as { age?: number } | null)?.age;

  const ageGroup = useMemo(() => getAgeGroup(age || 0), [age]);
  const questions = useMemo(() => getQuestionsForAgeGroup(ageGroup), [ageGroup]);

  const groups = useMemo(() => {
    const chunks: typeof questions[] = [];
    for (let i = 0; i < questions.length; i += GROUP_SIZE) {
      chunks.push(questions.slice(i, i + GROUP_SIZE));
    }
    return chunks;
  }, [questions]);

  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>(
    Object.fromEntries(questions.map((q) => [q.key, Math.floor((q.min + q.max) / 2)]))
  );
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  if (!age) {
    return (
      <div className="content-page">
        <p>Please start from the Check My Stress page.</p>
        <button className="btn btn-primary" onClick={() => navigate('/check-stress')}>Go Back</button>
      </div>
    );
  }

  function handleChange(key: string, value: number) {
    setAnswers((prev) => ({ ...prev, [key]: value }));
  }

  async function handleSubmit() {
    setSubmitting(true);
    setError('');
    try {
      const payload = { age, ...answers };
      const { data } = await api.post('/api/predictions/predict', payload);
      navigate('/stress-result', { state: { result: data } });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Something went wrong while running the assessment.');
    } finally {
      setSubmitting(false);
    }
  }

  const isLastStep = step === groups.length - 1;

  return (
    <div className="questionnaire-page">
      <ProgressBar current={step + 1} total={groups.length} />

      <div className="question-group">
        {groups[step].map((q) => (
          <QuestionCard key={q.key} question={q} value={answers[q.key]} onChange={handleChange} />
        ))}
      </div>

      {error && <div className="form-error">{error}</div>}

      <div className="questionnaire-actions">
        <button
          type="button"
          className="btn btn-outline"
          disabled={step === 0}
          onClick={() => setStep((s) => Math.max(0, s - 1))}
        >
          Previous
        </button>

        {isLastStep ? (
          <button type="button" className="btn btn-primary" onClick={handleSubmit} disabled={submitting}>
            {submitting ? 'Submitting...' : 'Submit Assessment'}
          </button>
        ) : (
          <button type="button" className="btn btn-primary" onClick={() => setStep((s) => s + 1)}>
            Next
          </button>
        )}
      </div>
    </div>
  );
}
