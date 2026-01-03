-- Update RLS policies to allow registration
-- Run these commands in your Supabase SQL Editor

-- Drop existing restrictive policies
DROP POLICY IF EXISTS "Users can insert own data" ON users;

-- Create new policy that allows registration
CREATE POLICY "Allow user registration" ON users
    FOR INSERT WITH CHECK (true);

-- Update SELECT policy to work with JWT tokens
DROP POLICY IF EXISTS "Users can view own data" ON users;
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (
        auth.uid()::text = user_id::text
        OR
        auth.jwt() ->> 'user_id' = user_id::text
    );

-- Update UPDATE policy
DROP POLICY IF EXISTS "Users can update own data" ON users;
CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (
        auth.uid()::text = user_id::text
        OR
        auth.jwt() ->> 'user_id' = user_id::text
    );

-- Keep DELETE policy (users should be able to delete their own data)
-- This one should work fine as is



