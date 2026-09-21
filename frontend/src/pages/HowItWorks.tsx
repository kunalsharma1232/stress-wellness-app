const STEPS = [
  { title: '1. Tell us your age', text: 'We ask your age first so the questionnaire that follows uses age-appropriate wording.' },
  { title: '2. Answer a short questionnaire', text: 'A multi-step form collects your anxiety, sleep, environment, and wellbeing factors.' },
  { title: '3. Feature mapping', text: 'Your answers are mapped to the exact numeric features the trained model expects - nothing arbitrary is sent to the model.' },
  { title: '4. Deep Learning prediction', text: 'A trained neural network (not if/else rules) classifies your stress level and produces class probabilities.' },
  { title: '5. Personalized results', text: 'You get a stress score, category, contributing factors, and tailored wellness recommendations.' },
  { title: '6. Track over time', text: 'Every assessment is saved so you can see trends on the Analytics and History pages.' },
];

export default function HowItWorks() {
  return (
    <div className="content-page">
      <h1>How It Works</h1>
      <div className="steps-list">
        {STEPS.map((s) => (
          <div key={s.title} className="step-item">
            <h3>{s.title}</h3>
            <p>{s.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
