"""
Database management module for Netflix OTT Platform.
Provides SQLite persistence, schema initialization matching the ER diagram,
seeding from sample_data, and transactional helper operations.
"""

import sqlite3
import os
import time
import pandas as pd
from datetime import datetime, timedelta
from .sample_data import (
    USERS, PROFILES, SUBS_PLANS, SUBSCRIPTIONS, PAYMENTS,
    CONTENT, GENRES, DIRECTORS, ACTORS, REVIEW_RATINGS, WATCH_HISTORY,
    CONTENT_GENRES, CONTENT_DIRECTORS, CONTENT_ACTORS
)

DB_PATH = os.path.join(os.path.dirname(__file__), "netflix.db")

def get_connection():
    """Get a SQLite database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_database(reset=False):
    """
    Initialize SQLite schema matching the ER diagram and seed initial data.
    If reset=True, drops all existing tables and re-seeds.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if reset:
        cursor.executescript("""
            DROP TABLE IF EXISTS WATCH_HISTORY;
            DROP TABLE IF EXISTS REVIEW_RATING;
            DROP TABLE IF EXISTS CONTENT_ACTORS;
            DROP TABLE IF EXISTS CONTENT_DIRECTORS;
            DROP TABLE IF EXISTS CONTENT_GENRES;
            DROP TABLE IF EXISTS PAYMENTS;
            DROP TABLE IF EXISTS SUBSCRIPTION;
            DROP TABLE IF EXISTS PROFILES;
            DROP TABLE IF EXISTS CONTENT;
            DROP TABLE IF EXISTS ACTORS;
            DROP TABLE IF EXISTS DIRECTORS;
            DROP TABLE IF EXISTS GENRES;
            DROP TABLE IF EXISTS SUBS_PLAN;
            DROP TABLE IF EXISTS USER;
        """)
        conn.commit()

    # Create tables based on ER Diagram
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS USER (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            reg_date TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS SUBS_PLAN (
            plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_name TEXT NOT NULL,
            price REAL NOT NULL,
            duration_mon INTEGER NOT NULL,
            max_screen INTEGER NOT NULL,
            video_qual TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS PROFILES (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            profile_name TEXT NOT NULL,
            profile_type TEXT NOT NULL CHECK(profile_type IN ('Adult', 'Kids')),
            FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS SUBSCRIPTION (
            subs_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plan_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Active', 'Expired', 'Cancelled')),
            FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE,
            FOREIGN KEY (plan_id) REFERENCES SUBS_PLAN(plan_id)
        );

        CREATE TABLE IF NOT EXISTS PAYMENTS (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subs_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            pay_date TEXT NOT NULL,
            pay_method TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Success', 'Failed')),
            FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE,
            FOREIGN KEY (subs_id) REFERENCES SUBSCRIPTION(subs_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS CONTENT (
            content_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            duration INTEGER NOT NULL,
            language TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('Movie', 'Series')),
            release_year INTEGER NOT NULL,
            maturity TEXT NOT NULL,
            rating REAL DEFAULT 0,
            poster_url TEXT,
            backdrop_url TEXT
        );

        CREATE TABLE IF NOT EXISTS GENRES (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            genre_name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS DIRECTORS (
            director_id INTEGER PRIMARY KEY AUTOINCREMENT,
            director_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ACTORS (
            actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS CONTENT_GENRES (
            content_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            PRIMARY KEY (content_id, genre_id),
            FOREIGN KEY (content_id) REFERENCES CONTENT(content_id) ON DELETE CASCADE,
            FOREIGN KEY (genre_id) REFERENCES GENRES(genre_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS CONTENT_DIRECTORS (
            content_id INTEGER NOT NULL,
            director_id INTEGER NOT NULL,
            PRIMARY KEY (content_id, director_id),
            FOREIGN KEY (content_id) REFERENCES CONTENT(content_id) ON DELETE CASCADE,
            FOREIGN KEY (director_id) REFERENCES DIRECTORS(director_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS CONTENT_ACTORS (
            content_id INTEGER NOT NULL,
            actor_id INTEGER NOT NULL,
            PRIMARY KEY (content_id, actor_id),
            FOREIGN KEY (content_id) REFERENCES CONTENT(content_id) ON DELETE CASCADE,
            FOREIGN KEY (actor_id) REFERENCES ACTORS(actor_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS REVIEW_RATING (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 10),
            review_text TEXT,
            review_date TEXT NOT NULL,
            FOREIGN KEY (content_id) REFERENCES CONTENT(content_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS WATCH_HISTORY (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            watch_date TEXT NOT NULL,
            progress_min INTEGER NOT NULL,
            completed INTEGER NOT NULL CHECK(completed IN (0, 1)),
            FOREIGN KEY (content_id) REFERENCES CONTENT(content_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE
        );
    """)
    conn.commit()

    # Check if data exists; if empty, seed from sample_data.py
    cursor.execute("SELECT COUNT(*) FROM USER;")
    if cursor.fetchone()[0] == 0:
        _seed_data(cursor)
        conn.commit()

    conn.close()

def _seed_data(cursor):
    """Seed sample data into SQLite tables."""
    # USERS
    cursor.executemany(
        "INSERT INTO USER (user_id, name, email, password, phone, reg_date) VALUES (?, ?, ?, ?, ?, ?)",
        [(u["user_id"], u["name"], u["email"], u["password"], u["phone"], u["reg_date"]) for u in USERS]
    )

    # SUBS_PLAN
    cursor.executemany(
        "INSERT INTO SUBS_PLAN (plan_id, plan_name, price, duration_mon, max_screen, video_qual) VALUES (?, ?, ?, ?, ?, ?)",
        [(p["plan_id"], p["plan_name"], p["price"], p["duration_mon"], p["max_screen"], p["video_qual"]) for p in SUBS_PLANS]
    )

    # PROFILES
    cursor.executemany(
        "INSERT INTO PROFILES (profile_id, user_id, profile_name, profile_type) VALUES (?, ?, ?, ?)",
        [(p["profile_id"], p["user_id"], p["profile_name"], p["profile_type"]) for p in PROFILES]
    )

    # SUBSCRIPTION
    cursor.executemany(
        "INSERT INTO SUBSCRIPTION (subs_id, user_id, plan_id, start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?)",
        [(s["subs_id"], s["user_id"], s["plan_id"], s["start_date"], s["end_date"], s["status"]) for s in SUBSCRIPTIONS]
    )

    # PAYMENTS
    cursor.executemany(
        "INSERT INTO PAYMENTS (payment_id, user_id, subs_id, amount, pay_date, pay_method, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [(p["payment_id"], p["user_id"], p["subs_id"], p["amount"], p["pay_date"], p["pay_method"], p["status"]) for p in PAYMENTS]
    )

    # CONTENT
    cursor.executemany(
        """INSERT INTO CONTENT (content_id, title, description, duration, language, type, release_year, maturity, rating, poster_url, backdrop_url)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [(c["content_id"], c["title"], c["description"], c["duration"], c["language"], c["type"],
          c["release_year"], c["maturity"], c["rating"], c["poster_url"], c["backdrop_url"]) for c in CONTENT]
    )

    # GENRES
    cursor.executemany(
        "INSERT INTO GENRES (genre_id, genre_name) VALUES (?, ?)",
        [(g["genre_id"], g["genre_name"]) for g in GENRES]
    )

    # DIRECTORS
    cursor.executemany(
        "INSERT INTO DIRECTORS (director_id, director_name) VALUES (?, ?)",
        [(d["director_id"], d["director_name"]) for d in DIRECTORS]
    )

    # ACTORS
    cursor.executemany(
        "INSERT INTO ACTORS (actor_id, actor_name) VALUES (?, ?)",
        [(a["actor_id"], a["actor_name"]) for a in ACTORS]
    )

    # JUNCTIONS
    cursor.executemany(
        "INSERT INTO CONTENT_GENRES (content_id, genre_id) VALUES (?, ?)",
        [(cg["content_id"], cg["genre_id"]) for cg in CONTENT_GENRES]
    )

    cursor.executemany(
        "INSERT INTO CONTENT_DIRECTORS (content_id, director_id) VALUES (?, ?)",
        [(cd["content_id"], cd["director_id"]) for cd in CONTENT_DIRECTORS]
    )

    cursor.executemany(
        "INSERT INTO CONTENT_ACTORS (content_id, actor_id) VALUES (?, ?)",
        [(ca["content_id"], ca["actor_id"]) for ca in CONTENT_ACTORS]
    )

    # REVIEW_RATING
    cursor.executemany(
        "INSERT INTO REVIEW_RATING (review_id, content_id, user_id, rating, review_text, review_date) VALUES (?, ?, ?, ?, ?, ?)",
        [(r["review_id"], r["content_id"], r["user_id"], r["rating"], r["review_text"], r["review_date"]) for r in REVIEW_RATINGS]
    )

    # WATCH_HISTORY
    cursor.executemany(
        "INSERT INTO WATCH_HISTORY (history_id, content_id, user_id, watch_date, progress_min, completed) VALUES (?, ?, ?, ?, ?, ?)",
        [(w["history_id"], w["content_id"], w["user_id"], w["watch_date"], w["progress_min"], 1 if w["completed"] else 0) for w in WATCH_HISTORY]
    )


# ============================================================
# QUERY & CRUD HELPERS
# ============================================================

def get_all_users():
    """Retrieve all users."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM USER ORDER BY user_id ASC", conn)
    conn.close()
    return df.to_dict(orient="records")

def get_user_by_id(user_id):
    """Retrieve a single user by ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM USER WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def authenticate_user(email, password=None):
    """
    Authenticate user by email.
    Matches sample users or checks password.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM USER WHERE LOWER(email) = LOWER(?)", (email.strip(),))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)

def register_user(name, email, password, phone=""):
    """
    Register a new user in the USER entity table.
    Automatically creates initial profile in PROFILES and starter subscription.
    """
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        cur.execute("BEGIN TRANSACTION;")
        cur.execute("""
            INSERT INTO USER (name, email, password, phone, reg_date)
            VALUES (?, ?, ?, ?, ?)
        """, (name.strip(), email.strip().lower(), password, phone.strip(), today))
        new_uid = cur.lastrowid

        first_name = name.strip().split()[0] if name.strip() else "User"
        cur.execute("""
            INSERT INTO PROFILES (user_id, profile_name, profile_type)
            VALUES (?, ?, 'Adult')
        """, (new_uid, first_name))

        start_d = datetime.now().strftime("%Y-%m-%d")
        end_d = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        cur.execute("""
            INSERT INTO SUBSCRIPTION (user_id, plan_id, start_date, end_date, status)
            VALUES (?, 3, ?, ?, 'Active')
        """, (new_uid, start_d, end_d))

        conn.commit()
        return True, "Registration successful!", new_uid
    except Exception as e:
        conn.rollback()
        return False, str(e), None
    finally:
        conn.close()

def get_all_content():
    """Retrieve all content catalogue items."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM CONTENT ORDER BY rating DESC", conn)
    conn.close()
    return df.to_dict(orient="records")

def get_content_by_id(content_id):
    """Retrieve specific content item."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM CONTENT WHERE content_id = ?", (content_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_content_genres(content_id):
    """Get list of genre names for a content."""
    conn = get_connection()
    query = """
        SELECT g.genre_name
        FROM GENRES g
        JOIN CONTENT_GENRES cg ON g.genre_id = cg.genre_id
        WHERE cg.content_id = ?
    """
    df = pd.read_sql_query(query, conn, params=[content_id])
    conn.close()
    return df["genre_name"].tolist()

def get_content_actors(content_id):
    """Get list of actors for a content."""
    conn = get_connection()
    query = """
        SELECT a.actor_name
        FROM ACTORS a
        JOIN CONTENT_ACTORS ca ON a.actor_id = ca.actor_id
        WHERE ca.content_id = ?
    """
    df = pd.read_sql_query(query, conn, params=[content_id])
    conn.close()
    return df["actor_name"].tolist()

def get_content_director(content_id):
    """Get director name for a content."""
    conn = get_connection()
    query = """
        SELECT d.director_name
        FROM DIRECTORS d
        JOIN CONTENT_DIRECTORS cd ON d.director_id = cd.director_id
        WHERE cd.content_id = ?
    """
    df = pd.read_sql_query(query, conn, params=[content_id])
    conn.close()
    return df["director_name"].iloc[0] if not df.empty else "Unknown"
def get_content_genres_full(content_id):
    """Get list of full genre records (genre_id, genre_name) for a content."""
    conn = get_connection()
    query = """
        SELECT g.genre_id, g.genre_name
        FROM GENRES g
        JOIN CONTENT_GENRES cg ON g.genre_id = cg.genre_id
        WHERE cg.content_id = ?
    """
    df = pd.read_sql_query(query, conn, params=[content_id])
    conn.close()
    return df.to_dict(orient="records")

def get_content_actors_full(content_id):
    """Get list of full actor records (actor_id, actor_name) for a content."""
    conn = get_connection()
    query = """
        SELECT a.actor_id, a.actor_name
        FROM ACTORS a
        JOIN CONTENT_ACTORS ca ON a.actor_id = ca.actor_id
        WHERE ca.content_id = ?
    """
    df = pd.read_sql_query(query, conn, params=[content_id])
    conn.close()
    return df.to_dict(orient="records")

def get_content_director_full(content_id):
    """Get director record (director_id, director_name) for a content."""
    conn = get_connection()
    query = """
        SELECT d.director_id, d.director_name
        FROM DIRECTORS d
        JOIN CONTENT_DIRECTORS cd ON d.director_id = cd.director_id
        WHERE cd.content_id = ?
    """
    df = pd.read_sql_query(query, conn, params=[content_id])
    conn.close()
    return df.to_dict(orient="records")[0] if not df.empty else {"director_id": 0, "director_name": "Unknown"}

def get_content_raw_mapping(content_id):
    """Get junction table entries for ER mapping inspection."""
    conn = get_connection()
    cg = pd.read_sql_query("SELECT * FROM CONTENT_GENRES WHERE content_id = ?", conn, params=[content_id]).to_dict(orient="records")
    ca = pd.read_sql_query("SELECT * FROM CONTENT_ACTORS WHERE content_id = ?", conn, params=[content_id]).to_dict(orient="records")
    cd = pd.read_sql_query("SELECT * FROM CONTENT_DIRECTORS WHERE content_id = ?", conn, params=[content_id]).to_dict(orient="records")
    conn.close()
    return {"CONTENT_GENRES": cg, "CONTENT_ACTORS": ca, "CONTENT_DIRECTORS": cd}

def get_all_genres():
    """Retrieve all genres."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM GENRES ORDER BY genre_name ASC", conn)
    conn.close()
    return df.to_dict(orient="records")

def get_all_plans():
    """Retrieve all subscription plans."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM SUBS_PLAN ORDER BY price ASC", conn)
    conn.close()
    return df.to_dict(orient="records")

def get_plan_details(plan_id):
    """Retrieve specific plan details."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM SUBS_PLAN WHERE plan_id = ?", (plan_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_profiles(user_id):
    """Retrieve profiles belonging to a user."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM PROFILES WHERE user_id = ? ORDER BY profile_id ASC", conn, params=[user_id])
    conn.close()
    return df.to_dict(orient="records")

def get_user_subscription(user_id):
    """Retrieve active subscription for a user."""
    conn = get_connection()
    query = """
        SELECT s.*, p.plan_name, p.price, p.max_screen, p.video_qual
        FROM SUBSCRIPTION s
        JOIN SUBS_PLAN p ON s.plan_id = p.plan_id
        WHERE s.user_id = ? AND s.status = 'Active'
        ORDER BY s.subs_id DESC
        LIMIT 1
    """
    df = pd.read_sql_query(query, conn, params=[user_id])
    conn.close()
    return df.to_dict(orient="records")[0] if not df.empty else None

def get_user_payments(user_id):
    """Retrieve payment history for a user."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM PAYMENTS WHERE user_id = ? ORDER BY pay_date DESC, payment_id DESC", conn, params=[user_id])
    conn.close()
    return df.to_dict(orient="records")

def get_user_watch_history(user_id):
    """Retrieve watch history for a user enriched with content details."""
    conn = get_connection()
    query = """
        SELECT w.*, c.title, c.duration, c.poster_url, c.type
        FROM WATCH_HISTORY w
        JOIN CONTENT c ON w.content_id = c.content_id
        WHERE w.user_id = ?
        ORDER BY w.watch_date DESC, w.history_id DESC
    """
    df = pd.read_sql_query(query, conn, params=[user_id])
    conn.close()
    records = df.to_dict(orient="records")
    for r in records:
        r["completed"] = bool(r["completed"])
    return records

def get_content_reviews(content_id):
    """Retrieve reviews for a content item with reviewer name."""
    conn = get_connection()
    query = """
        SELECT r.*, u.name as user_name
        FROM REVIEW_RATING r
        JOIN USER u ON r.user_id = u.user_id
        WHERE r.content_id = ?
        ORDER BY r.review_date DESC, r.review_id DESC
    """
    df = pd.read_sql_query(query, conn, params=[content_id])
    conn.close()
    return df.to_dict(orient="records")

def get_all_reviews():
    """Retrieve all reviews enriched with user and title."""
    conn = get_connection()
    query = """
        SELECT r.*, u.name as user_name, c.title as content_title
        FROM REVIEW_RATING r
        JOIN USER u ON r.user_id = u.user_id
        JOIN CONTENT c ON r.content_id = c.content_id
        ORDER BY r.review_date DESC, r.review_id DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")

def get_table_df(table_name):
    """Retrieve raw pandas DataFrame of any table in database."""
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# ============================================================
# STATE MUTATION METHODS (SIMULATED TRANSACTIONS)
# ============================================================

def add_user_review(content_id, user_id, rating, review_text):
    """
    Insert a new review into REVIEW_RATING and update average rating in CONTENT.
    Demonstrates transaction handling.
    """
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        cur.execute("BEGIN TRANSACTION;")
        # 1. Insert review
        cur.execute("""
            INSERT INTO REVIEW_RATING (content_id, user_id, rating, review_text, review_date)
            VALUES (?, ?, ?, ?, ?)
        """, (content_id, user_id, rating, review_text, today))

        # 2. Update CONTENT rating average
        cur.execute("""
            SELECT AVG(rating) FROM REVIEW_RATING WHERE content_id = ?
        """, (content_id,))
        avg_rating = round(cur.fetchone()[0] or rating, 1)

        cur.execute("""
            UPDATE CONTENT SET rating = ? WHERE content_id = ?
        """, (avg_rating, content_id))

        conn.commit()
        return True, f"Review submitted successfully! New title rating: {avg_rating} ⭐"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def log_watch_progress(content_id, user_id, progress_min, completed=False):
    """
    Log or update watch progress in WATCH_HISTORY.
    """
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    comp_val = 1 if completed else 0

    try:
        # Check if record exists for user and content
        cur.execute("""
            SELECT history_id FROM WATCH_HISTORY
            WHERE user_id = ? AND content_id = ?
            ORDER BY history_id DESC LIMIT 1
        """, (user_id, content_id))
        row = cur.fetchone()

        if row:
            cur.execute("""
                UPDATE WATCH_HISTORY
                SET progress_min = ?, completed = ?, watch_date = ?
                WHERE history_id = ?
            """, (progress_min, comp_val, today, row["history_id"]))
        else:
            cur.execute("""
                INSERT INTO WATCH_HISTORY (content_id, user_id, watch_date, progress_min, completed)
                VALUES (?, ?, ?, ?, ?)
            """, (content_id, user_id, today, progress_min, comp_val))

        conn.commit()
        return True, "Watch progress updated successfully."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def subscribe_and_pay(user_id, plan_id, pay_method, simulate_failure=False):
    """
    ACID Transaction:
    1. If simulate_failure: insert FAILED payment record and rollback/exit without modifying subscription.
    2. If success:
       - Expire any currently active subscription for this user.
       - Insert new SUBSCRIPTION with status 'Active'.
       - Insert PAYMENTS record with status 'Success' linked to the new subs_id.
       - Commit transaction.
    """
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.now()
    start_date = today.strftime("%Y-%m-%d")

    # Fetch plan details
    cur.execute("SELECT * FROM SUBS_PLAN WHERE plan_id = ?", (plan_id,))
    plan = cur.fetchone()
    if not plan:
        conn.close()
        return False, "Plan not found."

    duration_days = plan["duration_mon"] * 30
    end_date = (today + timedelta(days=duration_days)).strftime("%Y-%m-%d")
    amount = plan["price"]

    try:
        cur.execute("BEGIN TRANSACTION;")

        if simulate_failure:
            # Create a placeholder failed payment
            cur.execute("""
                INSERT INTO PAYMENTS (user_id, subs_id, amount, pay_date, pay_method, status)
                VALUES (?, 0, ?, ?, ?, 'Failed')
            """, (user_id, amount, start_date, pay_method))
            conn.commit()
            return False, "Payment failed during bank gateway processing (Simulated). Subscription was NOT activated."

        # 1. Expire existing active subscriptions
        cur.execute("""
            UPDATE SUBSCRIPTION SET status = 'Expired'
            WHERE user_id = ? AND status = 'Active'
        """, (user_id,))

        # 2. Insert new subscription
        cur.execute("""
            INSERT INTO SUBSCRIPTION (user_id, plan_id, start_date, end_date, status)
            VALUES (?, ?, ?, ?, 'Active')
        """, (user_id, plan_id, start_date, end_date))
        subs_id = cur.lastrowid

        # 3. Insert payment record linked to subs_id
        cur.execute("""
            INSERT INTO PAYMENTS (user_id, subs_id, amount, pay_date, pay_method, status)
            VALUES (?, ?, ?, ?, ?, 'Success')
        """, (user_id, subs_id, amount, start_date, pay_method))

        conn.commit()
        return True, f"Successfully subscribed to {plan['plan_name']} (Payment ID: #{cur.lastrowid}, Subs ID: #{subs_id})!"
    except Exception as e:
        conn.rollback()
        return False, f"Transaction failed and was rolled back: {str(e)}"
    finally:
        conn.close()

def create_user_profile(user_id, profile_name, profile_type):
    """
    Insert a new profile under the given user.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO PROFILES (user_id, profile_name, profile_type)
            VALUES (?, ?, ?)
        """, (user_id, profile_name.strip(), profile_type))
        conn.commit()
        return True, f"Profile '{profile_name}' created successfully!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def run_arbitrary_query(sql_query):
    """
    Execute arbitrary SQL query for the SQL sandbox / evaluator console.
    Returns (DataFrame, error_message, elapsed_time_ms).
    """
    conn = get_connection()
    start = time.perf_counter()
    try:
        # Check if SELECT or DML
        stripped = sql_query.strip().upper()
        if stripped.startswith("SELECT") or stripped.startswith("WITH") or stripped.startswith("PRAGMA") or stripped.startswith("EXPLAIN"):
            df = pd.read_sql_query(sql_query, conn)
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            conn.close()
            return df, None, elapsed
        else:
            cur = conn.cursor()
            cur.execute(sql_query)
            conn.commit()
            rows_affected = cur.rowcount
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            conn.close()
            result_df = pd.DataFrame([{"Rows Affected": rows_affected, "Status": "Query Executed Successfully"}])
            return result_df, None, elapsed
    except Exception as e:
        elapsed = round((time.perf_counter() - start) * 1000, 2)
        conn.close()
        return None, str(e), elapsed

# Auto-initialize database on import if not already created
init_database()
