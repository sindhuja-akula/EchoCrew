-- Database Indexes for EchoCrew Performance Optimization

-- Users indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);

-- System logs index
CREATE INDEX IF NOT EXISTS idx_system_logs_created_at ON system_logs (created_at DESC);
