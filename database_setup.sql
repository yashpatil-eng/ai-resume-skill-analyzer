-- ============================================
-- AI Career Intelligence Platform - Database Setup
-- ============================================
-- Run these queries in your Supabase SQL Editor
-- Go to: https://supabase.com/dashboard/project/YOUR_PROJECT/sql

-- ============================================
-- 1. Create Users Table
-- ============================================
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 2. Create Resumes Table
-- ============================================
CREATE TABLE resumes (
    resume_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    filename VARCHAR(255),
    extracted_text TEXT,
    extracted_skills JSONB,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 3. Create Job Recommendations Table (Optional - for caching)
-- ============================================
CREATE TABLE job_recommendations (
    recommendation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    user_skills JSONB,
    recommendations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 4. Create User Sessions Table (Optional - for session management)
-- ============================================
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 5. Enable Row Level Security (RLS)
-- ============================================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;

-- ============================================
-- 6. Create RLS Policies
-- ============================================

-- Users table policies
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid()::text = user_id::text OR auth.jwt() ->> 'user_id' = user_id::text);

CREATE POLICY "Users can insert own data" ON users
    FOR INSERT WITH CHECK (true);  -- Allow registration without auth

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid()::text = user_id::text OR auth.jwt() ->> 'user_id' = user_id::text);

-- Resumes table policies
CREATE POLICY "Users can view own resumes" ON resumes
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own resumes" ON resumes
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own resumes" ON resumes
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own resumes" ON resumes
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Job recommendations table policies
CREATE POLICY "Users can view own recommendations" ON job_recommendations
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own recommendations" ON job_recommendations
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

-- User sessions table policies
CREATE POLICY "Users can view own sessions" ON user_sessions
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own sessions" ON user_sessions
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own sessions" ON user_sessions
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- ============================================
-- 7. Create Indexes for Performance
-- ============================================

-- Users table indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Resumes table indexes
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_uploaded_at ON resumes(uploaded_at);

-- Job recommendations table indexes
CREATE INDEX idx_recommendations_user_id ON job_recommendations(user_id);
CREATE INDEX idx_recommendations_created_at ON job_recommendations(created_at);

-- User sessions table indexes
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON user_sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);

-- ============================================
-- 8. Create Functions (Optional - for cleanup)
-- ============================================

-- Function to clean up expired sessions
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM user_sessions
    WHERE expires_at < NOW();

    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function to get user resume count
CREATE OR REPLACE FUNCTION get_user_resume_count(user_uuid UUID)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(*)
        FROM resumes
        WHERE user_id = user_uuid
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 9. Create Triggers (Optional - for auto-updates)
-- ============================================

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 10. Insert Sample Data (Optional - for testing)
-- ============================================

-- Insert a test user (password: 'test123' hashed)
-- Note: In production, use proper password hashing
INSERT INTO users (email, full_name, password_hash) VALUES
('test@example.com', 'Test User', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Le0KdJcQzYFJ8SfO');

-- ============================================
-- 11. Grant Permissions (if needed)
-- ============================================

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT USAGE ON SCHEMA public TO anon;

-- Grant permissions on tables
GRANT ALL ON users TO authenticated;
GRANT ALL ON resumes TO authenticated;
GRANT ALL ON job_recommendations TO authenticated;
GRANT ALL ON user_sessions TO authenticated;

-- Grant permissions for anon users (for registration)
GRANT INSERT ON users TO anon;

-- ============================================
-- 12. Verification Queries
-- ============================================

-- Check if tables were created
SELECT
    schemaname,
    tablename,
    tableowner
FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('users', 'resumes', 'job_recommendations', 'user_sessions');

-- Check if RLS is enabled
SELECT
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('users', 'resumes', 'job_recommendations', 'user_sessions');

-- Check policies
SELECT
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies
WHERE schemaname = 'public';

-- ============================================
-- 13. Backup and Recovery (Important!)
-- ============================================

-- Enable point-in-time recovery (already enabled in Supabase)
-- Regular backups are automatic in Supabase

-- To export data (run in SQL Editor):
-- SELECT * FROM users;
-- SELECT * FROM resumes;
-- SELECT * FROM job_recommendations;

-- ============================================
-- SETUP COMPLETE!
-- ============================================

-- Your database is now ready for the AI Career Intelligence Platform!
-- Next steps:
-- 1. Update your .env file with Supabase credentials
-- 2. Install supabase-py: pip install supabase
-- 3. Update your backend code to use the database
-- 4. Test the integration
