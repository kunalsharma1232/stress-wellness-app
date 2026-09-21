interface StressGaugeProps {
  score: number; // 0-100
  level: string;
}

export default function StressGauge({ score, level }: StressGaugeProps) {
  const radius = 80;
  const stroke = 14;
  const normalizedRadius = radius - stroke / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const offset = circumference - (score / 100) * circumference;

  const color = score >= 70 ? '#e05252' : score >= 40 ? '#e0a341' : '#3fb27f';

  return (
    <div className="stress-gauge">
      <svg height={radius * 2} width={radius * 2}>
        <circle
          stroke="#e9edf2"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke={color}
          fill="transparent"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${circumference} ${circumference}`}
          style={{ strokeDashoffset: offset, transition: 'stroke-dashoffset 0.6s ease' }}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
          transform={`rotate(-90 ${radius} ${radius})`}
        />
        <text x="50%" y="46%" textAnchor="middle" className="gauge-score">{score}</text>
        <text x="50%" y="62%" textAnchor="middle" className="gauge-label">/ 100</text>
      </svg>
      <div className="gauge-level" style={{ color }}>{level} Stress</div>
    </div>
  );
}
