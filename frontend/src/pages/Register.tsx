import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    if (password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }

    setLoading(true);
    try {
      await register(fullName, email, password, confirmPassword, Number(age));
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h1>Create Your Account</h1>
        <p className="auth-subtitle">Start understanding your stress with AI-powered insights.</p>

        {error && <div className="form-error">{error}</div>}

        <label>Full Name</label>
        <input required value={fullName} onChange={(e) => setFullName(e.target.value)} />

        <label>Email</label>
        <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />

        <label>Age</label>
        <input type="number" min={5} max={120} required value={age} onChange={(e) => setAge(e.target.value)} />

        <label>Password</label>
        <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />

        <label>Confirm Password</label>
        <input type="password" required value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />

        <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
          {loading ? 'Creating account...' : 'Register'}
        </button>

        <p className="auth-switch">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}
