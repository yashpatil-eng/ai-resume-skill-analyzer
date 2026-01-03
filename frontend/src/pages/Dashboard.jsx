import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ResumeUpload from '../components/ResumeUpload';
import JobResults from '../components/JobResults';
import { authAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [userSkills, setUserSkills] = useState([]);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    console.log('Dashboard: Checking authentication...');

    // Check if user is authenticated
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');

    console.log('Dashboard: Token exists:', !!token);
    console.log('Dashboard: User data exists:', !!userData);

    if (!token || !userData) {
      console.log('Dashboard: No token or user data, redirecting to login');
      navigate('/login');
      return;
    }

    // Get user info from localStorage
    try {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      console.log('Dashboard: User loaded from localStorage:', parsedUser.email);
    } catch (error) {
      console.error('Dashboard: Error parsing user data:', error);
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      navigate('/login');
      return;
    }

    // Verify token with backend (optional - for security)
    authAPI.getCurrentUser()
      .then((data) => {
        console.log('Dashboard: Token verified with backend:', data.email);
        // Update user data if needed
        if (data.full_name && !user.full_name) {
          setUser(data);
        }
      })
      .catch((error) => {
        console.error('Dashboard: Token verification failed:', error);
        // Token invalid, redirect to login
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
      });
  }, [navigate]);

  const handleResumeProcessed = (skills) => {
    setUserSkills(skills);
    setRecommendations(null); // Clear previous recommendations
  };

  const handleGetRecommendations = async () => {
    if (userSkills.length === 0) {
      alert('Please upload a resume first to extract skills');
      return;
    }

    setLoading(true);
    try {
      // Import jobAPI dynamically to avoid circular dependency
      const { jobAPI } = await import('../services/api');
      const response = await jobAPI.recommend(userSkills, 10);
      setRecommendations(response);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      alert('Failed to get job recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  if (!user) {
    return <div className="dashboard-loading">Loading...</div>;
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Career Intelligence Dashboard</h1>
          <div className="user-info">
            <span>Welcome, {user.full_name || user.email}</span>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-section">
          <h2>Upload Resume</h2>
          <ResumeUpload onResumeProcessed={handleResumeProcessed} />
        </div>

        {userSkills.length > 0 && (
          <div className="dashboard-section">
            <h2>Your Skills</h2>
            <div className="skills-display">
              {userSkills.map((skill, index) => (
                <span key={index} className="skill-tag">
                  {skill}
                </span>
              ))}
            </div>
            <button
              onClick={handleGetRecommendations}
              className="recommend-button"
              disabled={loading}
            >
              {loading ? 'Loading Recommendations...' : 'Get Job Recommendations'}
            </button>
          </div>
        )}

        {recommendations && (
          <div className="dashboard-section">
            <h2>Job Recommendations</h2>
            <JobResults recommendations={recommendations} />
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;





