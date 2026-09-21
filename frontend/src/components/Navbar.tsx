import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/navbar.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/');
  }

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-logo">
          <span className="navbar-logo-mark">MS</span>
          <span>MindScope AI</span>
        </Link>
        <nav className="navbar-links">
          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
          <Link to="/how-it-works">How It Works</Link>
          <Link to="/ai-technology">AI Technology</Link>
          {user && <Link to="/dashboard">Dashboard</Link>}
        </nav>
        <div className="navbar-actions">
          {user ? (
            <>
              <Link to="/check-stress" className="btn btn-primary btn-sm">Check My Stress</Link>
              <button className="btn btn-ghost btn-sm" onClick={handleLogout}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-ghost btn-sm">Login</Link>
              <Link to="/register" className="btn btn-primary btn-sm">Register</Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
