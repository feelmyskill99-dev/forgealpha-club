import aiosqlite
import asyncio
from datetime import datetime, timedelta
from config import TIERS

DB_PATH = "alpha_club.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                tier INTEGER DEFAULT 0,
                subscribed_until TEXT,
                referrals INTEGER DEFAULT 0,
                referred_by INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                min_tier INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                source TEXT DEFAULT 'onchain'
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                tier INTEGER,
                amount REAL,
                tx_hash TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row:
            return {
                "user_id": row[0], "username": row[1], "tier": row[2],
                "subscribed_until": row[3], "referrals": row[4], "referred_by": row[5]
            }
        return None

async def create_or_update_user(user_id: int, username: str = None, referred_by: int = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, username, referred_by) 
            VALUES (?, ?, ?)
        """, (user_id, username, referred_by))
        if username:
            await db.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
        await db.commit()

async def upgrade_user_tier(user_id: int, new_tier: int, months: int = 1):
    until = (datetime.now() + timedelta(days=30 * months)).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users SET tier = ?, subscribed_until = ? 
            WHERE user_id = ?
        """, (new_tier, until, user_id))
        await db.commit()

async def add_signal(text: str, min_tier: int, source: str = "manual"):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO signals (text, min_tier, source) VALUES (?, ?, ?)
        """, (text, min_tier, source))
        await db.commit()
        cursor = await db.execute("SELECT last_insert_rowid()")
        return (await cursor.fetchone())[0]

async def get_active_users_by_tier(min_tier: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT user_id FROM users 
            WHERE tier >= ? AND (subscribed_until IS NULL OR subscribed_until > datetime('now'))
        """, (min_tier,))
        rows = await cursor.fetchall()
        return [row[0] for row in rows]

async def add_payment(user_id: int, tier: int, amount: float, tx_hash: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO payments (user_id, tier, amount, tx_hash) VALUES (?, ?, ?, ?)
        """, (user_id, tier, amount, tx_hash))
        await db.commit()

async def get_pending_payments():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM payments WHERE status = 'pending'")
        return await cursor.fetchall()