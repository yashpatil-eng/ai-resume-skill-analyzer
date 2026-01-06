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
    console.log('Dashboard: Current URL:', window.location.pathname);

    // Small delay to ensure login data is stored
    const checkAuth = () => {
      // Check if user is authenticated
      const token = localStorage.getItem('token');
      const userData = localStorage.getItem('user');

      console.log('Dashboard: Token exists:', !!token);
      console.log('Dashboard: User data exists:', !!userData);
      console.log('Dashboard: Token value:', token ? token.substring(0, 20) + '...' : 'null');
      console.log('Dashboard: User data value:', userData ? userData.substring(0, 50) + '...' : 'null');

      if (!token || !userData) {
        console.log('Dashboard: No token or user data, redirecting to login');
        navigate('/login');
        return;
      }

      let parsedUser;
      // Get user info from localStorage
      try {
        parsedUser = JSON.parse(userData);
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
          if (data.full_name && parsedUser && !parsedUser.full_name) {
            const updatedUser = { ...parsedUser, full_name: data.full_name };
            setUser(updatedUser);
            localStorage.setItem('user', JSON.stringify(updatedUser));
          }
        })
        .catch((error) => {
          console.error('Dashboard: Token verification failed:', error);
          console.error('Error details:', error.response?.data || error.message);
          // Only redirect if it's a real auth failure, not a network issue
          if (error.response?.status === 401) {
            console.log('Dashboard: 401 error - token invalid, redirecting to login');
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            navigate('/login');
          } else {
            console.log('Dashboard: Non-auth error, staying on dashboard (might be network issue)');
          }
        });
    };

    // Check auth immediately, but also after a short delay in case of timing issues
    checkAuth();
    const timeoutId = setTimeout(checkAuth, 500);

    return () => clearTimeout(timeoutId);
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





