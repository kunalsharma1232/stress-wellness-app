export function getAgeGroup(age: number): string {
  const bands: [number, number, string][] = [
    [10, 19, '10-19'], [20, 29, '20-29'], [30, 39, '30-39'],
    [40, 49, '40-49'], [50, 59, '50-59'], [60, 69, '60-69'],
    [70, 79, '70-79'], [80, 89, '80-89'], [90, 200, '90+'],
  ];
  const match = bands.find(([lo, hi]) => age >= lo && age <= hi);
  return match ? match[2] : 'unknown';
}

export interface CoreQuestion {
  key: string;
  label: string;
  min: number;
  max: number;
}

/** Core ML-mapped questions, reworded slightly per age group for tone/accessibility.
 * Every group still feeds the SAME backend feature keys - see section 9 of the spec. */
export function getQuestionsForAgeGroup(ageGroup: string): CoreQuestion[] {
  const isYouth = ageGroup === '10-19';
  const isYoungAdult = ageGroup === '20-29' || ageGroup === '30-39';
  const isMidLife = ageGroup === '40-49' || ageGroup === '50-59';
  const isOlder = ['60-69', '70-79', '80-89', '90+'].includes(ageGroup);

  const anxietyLabel = isYouth
    ? 'How often do you feel anxious because of school, studies, or social situations?'
    : isYoungAdult
    ? 'How often do career, financial, or relationship concerns make you feel anxious?'
    : isMidLife
    ? 'How often do work or family responsibilities make you feel anxious?'
    : 'How often do you feel anxious or on edge, day to day?';

  const stressSourceLabel = isYouth
    ? 'How heavy does your school/college workload feel lately?'
    : isYoungAdult
    ? 'How much do career or financial pressures weigh on you?'
    : isMidLife
    ? 'How much do work and family responsibilities weigh on you?'
    : isOlder
    ? 'How connected do you feel to others day to day?'
    : 'How manageable does your day-to-day load feel?';

  return [
    { key: 'anxiety_level', label: anxietyLabel, min: 0, max: 21 },
    { key: 'depression', label: 'How low or down have you generally felt recently?', min: 0, max: 27 },
    { key: 'sleep_quality', label: 'How would you describe your sleep quality?', min: 0, max: 5 },
    { key: 'headache', label: 'How often have you experienced headaches?', min: 0, max: 5 },
    { key: 'breathing_problem', label: 'How often have you noticed difficulty breathing during stressful moments?', min: 0, max: 5 },
    { key: 'mental_health_history', label: 'Have you previously experienced mental health difficulties? (0 = No, 1 = Yes)', min: 0, max: 1 },
    { key: 'living_conditions', label: 'How comfortable and safe do you feel in your living environment?', min: 0, max: 5 },
    { key: 'study_load', label: stressSourceLabel, min: 0, max: 5 },
    { key: 'social_support', label: 'How supported do you feel by people around you?', min: 0, max: 5 },
    { key: 'self_esteem', label: 'How would you rate your overall self-confidence lately?', min: 0, max: 30 },
    ...(isYouth ? [{ key: 'bullying', label: 'How often have you experienced bullying or peer pressure?', min: 0, max: 5 }] : []),
    ...(isYoungAdult || isMidLife
      ? [{ key: 'future_career_concerns', label: 'How much do future career or financial concerns weigh on you?', min: 0, max: 5 }]
      : []),
  ];
}
