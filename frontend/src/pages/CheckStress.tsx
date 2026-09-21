import { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function CheckStress() {
  const [age, setAge] = useState('');
  const navigate = useNavigate();

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    navigate('/questionnaire', { state: { age: Number(age) } });
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h1>Let's understand you better</h1>
        <p className="auth-subtitle">
          We'll start with your age so the questions that follow feel relevant to you.
        </p>

        <label>What is your age?</label>
        <input
          type="number"
          min={10}
          max={110}
          required
          value={age}
          onChange={(e) => setAge(e.target.value)}
          placeholder="e.g. 24"
        />

        <button type="submit" className="btn btn-primary btn-block">Continue</button>
      </form>
    </div>
  );
}
