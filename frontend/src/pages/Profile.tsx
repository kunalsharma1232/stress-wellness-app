import { useAuth } from '../context/AuthContext';

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="content-page">
      <h1>Profile</h1>
      <div className="profile-card">
        <p><strong>Full Name:</strong> {user?.full_name}</p>
        <p><strong>Email:</strong> {user?.email}</p>
        <p><strong>Age:</strong> {user?.age}</p>
      </div>
    </div>
  );
}
