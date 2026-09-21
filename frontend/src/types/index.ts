export interface User {
  id: string;
  full_name: string;
  email: string;
  age: number;
}

export interface QuestionnaireAnswers {
  age: number;
  anxiety_level: number;
  self_esteem: number;
  mental_health_history: number;
  depression: number;
  headache: number;
  blood_pressure: number;
  sleep_quality: number;
  breathing_problem: number;
  noise_level: number;
  living_conditions: number;
  safety: number;
  basic_needs: number;
  academic_performance: number;
  study_load: number;
  teacher_student_relationship: number;
  future_career_concerns: number;
  social_support: number;
  peer_pressure: number;
  extracurricular_activities: number;
  bullying: number;
}

export interface PredictionResult {
  id: string;
  predicted_label: string;
  stress_score: number;
  probabilities: Record<string, number>;
  age_group: string;
  created_at: string;
  recommendations: string[];
}

export interface HistoryItem {
  id: string;
  age: number;
  age_group: string;
  prediction: string;
  stress_score: number;
  created_at: string;
}

export interface AnalyticsSummary {
  has_data: boolean;
  latest_score?: number;
  latest_level?: string;
  total_assessments?: number;
  category_distribution?: Record<string, number>;
  factor_averages?: Record<string, number>;
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  confusion_matrix: number[][];
  num_classes: number;
  test_set_size: number;
}
