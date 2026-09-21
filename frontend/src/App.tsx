import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ProtectedRoute from './components/ProtectedRoute';

import Home from './pages/Home';
import About from './pages/About';
import HowItWorks from './pages/HowItWorks';
import AiTechnology from './pages/AiTechnology';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CheckStress from './pages/CheckStress';
import Questionnaire from './pages/Questionnaire';
import StressResult from './pages/StressResult';
import Analytics from './pages/Analytics';
import History from './pages/History';
import Recommendations from './pages/Recommendations';
import WellnessAssistant from './pages/WellnessAssistant';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <AuthProvider>
      <div className="app-shell">
        <Navbar />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/how-it-works" element={<HowItWorks />} />
            <Route path="/ai-technology" element={<AiTechnology />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/check-stress" element={<ProtectedRoute><CheckStress /></ProtectedRoute>} />
            <Route path="/questionnaire" element={<ProtectedRoute><Questionnaire /></ProtectedRoute>} />
            <Route path="/stress-result" element={<ProtectedRoute><StressResult /></ProtectedRoute>} />
            <Route path="/analytics" element={<ProtectedRoute><Analytics /></ProtectedRoute>} />
            <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />
            <Route path="/recommendations/:assessmentId" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />
            <Route path="/wellness-assistant" element={<ProtectedRoute><WellnessAssistant /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />

            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </AuthProvider>
  );
}
