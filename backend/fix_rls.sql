-- Emergency RLS Fix for Supabase
-- Run these commands in Supabase SQL Editor in order

-- Step 1: Temporarily disable RLS to allow registration
ALTER TABLE users DISABLE ROW LEVEL SECURITY;

-- Step 2: Drop all existing policies that might be causing issues
DROP POLICY IF EXISTS "Users can view own data" ON users;
DROP POLICY IF EXISTS "Users can insert own data" ON users;
DROP POLICY IF EXISTS "Users can update own data" ON users;
DROP POLICY IF EXISTS "Users can delete own data" ON users;
DROP POLICY IF EXISTS "Allow user registration" ON users;

-- Step 3: Re-enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Step 4: Create working policies
-- Allow anyone to register (insert)
CREATE POLICY "allow_registration" ON users
    FOR INSERT
    WITH CHECK (true);

-- Allow users to view their own data
CREATE POLICY "users_select_own" ON users
    FOR SELECT
    USING (auth.uid()::text = user_id::text);

-- Allow users to update their own data
CREATE POLICY "users_update_own" ON users
    FOR UPDATE
    USING (auth.uid()::text = user_id::text);

-- Allow users to delete their own data
CREATE POLICY "users_delete_own" ON users
    FOR DELETE
    USING (auth.uid()::text = user_id::text);

-- Step 5: Test the setup
-- Try inserting a test user
-- INSERT INTO users (email, password_hash, full_name) VALUES ('test@example.com', 'hash', 'Test User');

-- Step 6: Check if policies are working
-- SELECT * FROM users WHERE email = 'test@example.com';



