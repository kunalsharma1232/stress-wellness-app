import type { CoreQuestion } from '../hooks/useAgeGroup';

interface QuestionCardProps {
  question: CoreQuestion;
  value: number;
  onChange: (key: string, value: number) => void;
}

export default function QuestionCard({ question, value, onChange }: QuestionCardProps) {
  const isBinary = question.max === 1;

  return (
    <div className="question-card">
      <label className="question-label">{question.label}</label>
      {isBinary ? (
        <div className="question-binary">
          <button
            type="button"
            className={`btn btn-toggle ${value === 0 ? 'active' : ''}`}
            onClick={() => onChange(question.key, 0)}
          >
            No
          </button>
          <button
            type="button"
            className={`btn btn-toggle ${value === 1 ? 'active' : ''}`}
            onClick={() => onChange(question.key, 1)}
          >
            Yes
          </button>
        </div>
      ) : (
        <div className="question-slider">
          <input
            type="range"
            min={question.min}
            max={question.max}
            value={value}
            onChange={(e) => onChange(question.key, Number(e.target.value))}
          />
          <div className="question-slider-scale">
            <span>Low</span>
            <span className="question-slider-value">{value}</span>
            <span>High</span>
          </div>
        </div>
      )}
    </div>
  );
}
