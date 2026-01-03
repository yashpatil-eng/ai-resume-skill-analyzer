import { useState } from 'react';
import { resumeAPI } from '../services/api';
import './ResumeUpload.css';

const ResumeUpload = ({ onResumeProcessed }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [extractedSkills, setExtractedSkills] = useState([]);
  const [extractedText, setExtractedText] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type !== 'application/pdf') {
        setError('Please upload a PDF file');
        return;
      }
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }
      setFile(selectedFile);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError('');
    setExtractedSkills([]);
    setExtractedText('');

    try {
      const response = await resumeAPI.upload(file);
      
      setExtractedSkills(response.extracted_skills);
      setExtractedText(response.extracted_text);
      
      // Notify parent component
      if (onResumeProcessed) {
        onResumeProcessed(response.extracted_skills);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Failed to upload resume. Please try again.'
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="resume-upload">
      <div className="upload-section">
        <div className="file-input-wrapper">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            id="resume-file"
            className="file-input"
            disabled={uploading}
          />
          <label htmlFor="resume-file" className="file-label">
            {file ? file.name : 'Choose PDF Resume'}
          </label>
        </div>

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="upload-button"
        >
          {uploading ? 'Processing...' : 'Upload & Extract Skills'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {extractedSkills.length > 0 && (
        <div className="extraction-results">
          <h3>Extraction Results</h3>
          <div className="skills-preview">
            <strong>Extracted Skills ({extractedSkills.length}):</strong>
            <div className="skills-list">
              {extractedSkills.map((skill, index) => (
                <span key={index} className="skill-badge">
                  {skill}
                </span>
              ))}
            </div>
          </div>
          {extractedText && (
            <div className="text-preview">
              <strong>Resume Text Preview:</strong>
              <p>{extractedText}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;






