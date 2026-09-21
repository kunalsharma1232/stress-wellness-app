interface StressCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  accent?: 'default' | 'warning' | 'danger' | 'success';
}

export default function StressCard({ title, value, subtitle, accent = 'default' }: StressCardProps) {
  return (
    <div className={`stat-card stat-card-${accent}`}>
      <div className="stat-card-title">{title}</div>
      <div className="stat-card-value">{value}</div>
      {subtitle && <div className="stat-card-subtitle">{subtitle}</div>}
    </div>
  );
}
