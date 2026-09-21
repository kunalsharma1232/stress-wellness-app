export default function About() {
  return (
    <div className="content-page">
      <h1>About This Project</h1>

      <h2>Project Objective</h2>
      <p>
        MindScope AI aims to help people better understand the factors contributing to their stress
        using an AI-driven assessment, and to translate that understanding into actionable,
        personalized wellness guidance.
      </p>

      <h2>Problem Statement</h2>
      <p>
        Stress affects people of all ages, but it is rarely measured or explained in an accessible,
        personalized way. Most people only realize the scale of their stress once it has already
        affected their health, relationships, or performance.
      </p>

      <h2>Why Stress Detection Matters</h2>
      <p>
        Early awareness of stress factors - sleep, anxiety, environment, workload, and social support -
        allows for proactive lifestyle changes before stress escalates into more serious health concerns.
      </p>

      <h2>Role of Artificial Intelligence</h2>
      <p>
        Rather than relying on fixed if/else rules, this system trains a neural network on real
        questionnaire data so it can recognize non-obvious patterns and interactions between
        anxiety, sleep, environment, and other factors.
      </p>

      <h2>Deep Learning Methodology</h2>
      <p>
        A multi-layer neural network (Dense &rarr; ReLU &rarr; Dropout &rarr; Dense &rarr; ReLU &rarr; Dropout &rarr; Output)
        is trained on a preprocessed, scaled version of the dataset, evaluated on a held-out test
        set, and the resulting metrics are shown transparently on the AI Technology page.
      </p>

      <h2>Personalized Wellness Recommendations</h2>
      <p>
        After a prediction, the system layers rule-based, explainable wellness guidance on top of the
        AI result - tailored to which specific factors (sleep, anxiety, support, workload, etc.) are
        driving your score.
      </p>

      <h2>Privacy and Responsible AI</h2>
      <p>
        Your responses and results are stored securely and are never sold or shared. Passwords are
        hashed, not stored in plain text, and API access requires authentication.
      </p>

      <p className="disclaimer-box">
        This system is an AI-based educational/wellness support system and is not a medical
        diagnosis tool. If you are experiencing a mental-health emergency, please contact a
        qualified healthcare professional or emergency service.
      </p>
    </div>
  );
}
