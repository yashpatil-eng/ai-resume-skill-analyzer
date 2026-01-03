import './JobResults.css';

const JobResults = ({ recommendations }) => {
  if (!recommendations || !recommendations.recommendations) {
    return <div>No recommendations available</div>;
  }

  const { user_skills, total_jobs_found, recommendations: jobs } = recommendations;

  return (
    <div className="job-results">
      <div className="results-header">
        <p>
          Found <strong>{total_jobs_found}</strong> job recommendations based on your skills
        </p>
      </div>

      <div className="jobs-list">
        {jobs.map((job) => (
          <div key={job.job_id} className="job-card">
            <div className="job-header">
              <h3 className="job-title">{job.job_title}</h3>
              <div className="match-score">
                <span className="match-percentage">
                  {job.match_percentage.toFixed(1)}% Match
                </span>
                <div className="match-bar">
                  <div
                    className="match-fill"
                    style={{ width: `${job.match_percentage}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="job-details">
              <div className="detail-section">
                <h4>Required Skills</h4>
                <div className="skills-tags">
                  {job.required_skills.map((skill, index) => (
                    <span
                      key={index}
                      className={`skill-tag ${
                        job.user_skills.includes(skill) ? 'skill-match' : 'skill-missing'
                      }`}
                    >
                      {skill}
                      {job.user_skills.includes(skill) && ' ✓'}
                    </span>
                  ))}
                </div>
              </div>

              {job.missing_skills.length > 0 && (
                <div className="detail-section">
                  <h4>Missing Skills ({job.skill_gap_count})</h4>
                  <div className="skills-tags">
                    {job.missing_skills.map((skill, index) => (
                      <span key={index} className="skill-tag skill-missing">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {job.missing_skills.length === 0 && (
                <div className="perfect-match">
                  ✓ You have all the required skills for this position!
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {jobs.length === 0 && (
        <div className="no-results">
          No job recommendations found. Try uploading a resume with more skills.
        </div>
      )}
    </div>
  );
};

export default JobResults;






