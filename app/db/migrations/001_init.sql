-- Initial schema for ForgeAlpha Club v2
-- Run this on every fresh database

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    tier INTEGER DEFAULT 0,
    subscription_status TEXT DEFAULT 'active',
    subscribed_until TEXT,
    trial_until TEXT,
    banned_until TEXT,
    referrals INTEGER DEFAULT 0,
    referred_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tier INTEGER NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    provider TEXT DEFAULT 'manual',
    tx_hash TEXT,
    status TEXT DEFAULT 'pending',
    confirmations INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    min_tier INTEGER NOT NULL,
    source TEXT DEFAULT 'onchain',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_payments_user_status ON payments(user_id, status);
CREATE INDEX IF NOT EXISTS idx_users_tier ON users(tier);