import { Link } from 'react-router-dom';
import '../styles/home.css';

const FEATURES = [
  { title: 'AI Stress Prediction', text: 'A trained Deep Learning model analyzes your questionnaire responses to estimate your stress level.' },
  { title: 'Personalized Assessment', text: 'Questions are dynamically selected and worded according to your age group.' },
  { title: 'Wellness Recommendations', text: 'Get personalized lifestyle and wellness suggestions based on your specific factors.' },
  { title: 'Visual Analytics', text: 'Understand your stress factors and trends over time through clear graphs.' },
  { title: 'Secure Data', text: 'Your information and prediction history are stored securely in MongoDB.' },
];

export default function Home() {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <h1>AI Based Stress Level Prediction and Wellness Recommendation System</h1>
          <p className="hero-subtitle">
            Understand your stress level using Artificial Intelligence and receive personalized
            wellness recommendations based on your responses.
          </p>
          <div className="hero-actions">
            <Link to="/check-stress" className="btn btn-primary btn-lg">Check My Stress</Link>
            <Link to="/how-it-works" className="btn btn-outline btn-lg">Learn More</Link>
          </div>
        </div>
        <div className="hero-visual" aria-hidden="true">
          <div className="hero-visual-ring ring-1" />
          <div className="hero-visual-ring ring-2" />
          <div className="hero-visual-core">AI</div>
        </div>
      </section>

      <section className="features">
        <h2>What MindScope AI Offers</h2>
        <div className="feature-grid">
          {FEATURES.map((f) => (
            <div key={f.title} className="feature-card">
              <h3>{f.title}</h3>
              <p>{f.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="cta-band">
        <h2>Ready to understand your stress?</h2>
        <p>It takes a few minutes and gives you a personalized, AI-derived picture of your wellbeing.</p>
        <Link to="/check-stress" className="btn btn-primary btn-lg">Check My Stress</Link>
      </section>
    </div>
  );
}
