import sqlite3

DB_NAME = 'bot_database.db'


def init_db():
    """Initialize the database and create tables if they don't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            profile TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            event TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        conn.commit()
        print('Database initialized successfully.')
    except sqlite3.Error as e:
        print(f'Error initializing database: {e}')
    finally:
        if conn:
            conn.close()


def upsert_user(username, profile):
    """Insert a new user or update existing user profile."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (username, profile) VALUES (?, ?) 
                          ON CONFLICT(username) DO UPDATE SET profile = excluded.profile;''', (username, profile))
        conn.commit()
        print('User upserted successfully.')
    except sqlite3.Error as e:
        print(f'Error upserting user: {e}')
    finally:
        if conn:
            conn.close()


def set_profile(username, profile):
    """Set user profile by username."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET profile = ? WHERE username = ?', (profile, username))
        conn.commit()
        if cursor.rowcount == 0:
            print('No user found with that username.')
        else:
            print('Profile updated successfully.')
    except sqlite3.Error as e:
        print(f'Error setting profile: {e}')
    finally:
        if conn:
            conn.close()


def get_user(username):
    """Get user information by username."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            return user
        else:
            print('User not found.')
            return None
    except sqlite3.Error as e:
        print(f'Error getting user: {e}')
    finally:
        if conn:
            conn.close()


def log_event(username, event):
    """Log an event for a user."""
    try:
        user = get_user(username)
        if user:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO events (user_id, event) VALUES (?, ?)', (user[0], event))
            conn.commit()
            print('Event logged successfully.')
        else:
            print('Cannot log event. User not found.')
    except sqlite3.Error as e:
        print(f'Error logging event: {e}')
    finally:
        if conn:
            conn.close()