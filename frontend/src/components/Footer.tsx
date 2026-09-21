export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <p>
          <strong>MindScope AI</strong> - AI Based Stress Level Prediction and Wellness Recommendation System
        </p>
        <p className="footer-disclaimer">
          This application is designed for educational and wellness-support purposes.
          It does not provide medical diagnosis or replace professional medical advice.
          If you are in crisis or experiencing a mental-health emergency, please contact
          a qualified healthcare professional or emergency service immediately.
        </p>
        <p className="footer-copy">&copy; {new Date().getFullYear()} MindScope AI - B.Tech AI &amp; Data Science Project</p>
      </div>
    </footer>
  );
}
