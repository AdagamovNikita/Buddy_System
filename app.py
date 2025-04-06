from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

def get_db_connection():
    conn = sqlite3.connect("buddy_system.db")
    conn.row_factory = sqlite3.Row
    return conn

DUMMY_STUDENT_DATA = [
    {
        "full_name": "Sam Al Khoury",
        "student_id": "100000018",
        "age": 18,
        "gender": "Male",
        "major": "Bachelor of Science in Computer Science",
        "academic_year": 2,
        "email": "sja00@aubmed.ac.cy"
    },
    {
        "full_name": "Omar Kaddour",
        "student_id": "100000001",
        "age": 19,
        "gender": "Male",
        "major": "Bachelor of Science in Computer Science",
        "academic_year": 2,
        "email": "osa00@aubmed.ac.cy"
    },
    {
        "full_name": "Ryan Dibeh",
        "student_id": "100000019",
        "age": 18,
        "gender": "male",
        "major": "Bachelor of Science in Psychology",
        "academic_year": 1,
        "email": "rad00@aubmed.ac.cy"
    }
]

def initialize_db():
    conn = get_db_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            email TEXT UNIQUE,
            full_name TEXT,
            role TEXT CHECK(role IN ('student', 'buddy')),
            is_approved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_details (
            user_id INTEGER PRIMARY KEY,
            student_id_number TEXT UNIQUE,
            age INTEGER,
            gender TEXT,
            interests TEXT,
            nationality TEXT,
            major TEXT,
            academic_year INTEGER CHECK(academic_year BETWEEN 1 AND 5),
            languages TEXT,
            bio TEXT,
            phone_number TEXT,
            is_international BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS buddy_preferences (
            user_id INTEGER PRIMARY KEY,
            preferred_role TEXT CHECK(preferred_role IN ('advisor', 'mentor', 'friend')),
            preferred_gender TEXT,
            min_preferred_age INTEGER,
            max_preferred_age INTEGER,
            preferred_major TEXT,
            preferred_language TEXT
        );

        CREATE TABLE IF NOT EXISTS buddy_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buddy_id INTEGER,
            student_id INTEGER,
            status TEXT CHECK(status IN ('pending', 'active', 'declined', 'completed', 'paused')) DEFAULT 'pending',
            match_score INTEGER,
            matched_by_admin BOOLEAN DEFAULT FALSE,
            admin_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (buddy_id, student_id),
            CHECK (buddy_id != student_id)
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            content TEXT,
            is_read BOOLEAN DEFAULT FALSE,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS video_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            initiator_id INTEGER,
            recipient_id INTEGER,
            scheduled_time TIMESTAMP,
            duration_minutes INTEGER,
            call_status TEXT CHECK(call_status IN ('scheduled', 'completed', 'missed', 'canceled')),
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            interaction_type TEXT CHECK(interaction_type IN ('message', 'call', 'meeting', 'event')),
            points_earned INTEGER DEFAULT 0,
            interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duration_minutes INTEGER,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS leaderboard (
            user_id INTEGER PRIMARY KEY,
            total_points INTEGER DEFAULT 0,
            current_rank INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reviewer_id INTEGER,
            reviewed_id INTEGER,
            match_id INTEGER,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            comments TEXT,
            is_anonymous BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            event_type TEXT CHECK(event_type IN ('mentorship', 'social', 'academic', 'workshop')),
            location TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            max_attendees INTEGER,
            organizer_id INTEGER,
            is_public BOOLEAN DEFAULT TRUE,
            points_value INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS event_attendees (
            event_id INTEGER,
            user_id INTEGER,
            attended BOOLEAN DEFAULT FALSE,
            points_earned INTEGER DEFAULT 0,
            PRIMARY KEY (event_id, user_id)
        );

        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            day_of_week INTEGER CHECK(day_of_week BETWEEN 0 AND 6),
            start_time TIME,
            end_time TIME,
            is_recurring BOOLEAN DEFAULT TRUE
        );

        CREATE TABLE IF NOT EXISTS scheduled_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            scheduled_time TIMESTAMP,
            duration_minutes INTEGER,
            session_type TEXT CHECK(session_type IN ('academic', 'social', 'career', 'other')),
            status TEXT CHECK(status IN ('scheduled', 'completed', 'canceled', 'no-show')) DEFAULT 'scheduled',
            location TEXT,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT,
            target_user_id INTEGER,
            description TEXT,
            performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            target_roles TEXT,
            is_pinned BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            message TEXT,
            notification_type TEXT,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            related_entity_type TEXT,
            related_entity_id INTEGER
        );

        CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
        CREATE INDEX IF NOT EXISTS idx_buddy_matches_status ON buddy_matches(status);
        CREATE INDEX IF NOT EXISTS idx_interactions_match_id ON interactions(match_id);
        CREATE INDEX IF NOT EXISTS idx_scheduled_sessions_match_id ON scheduled_sessions(match_id);
        CREATE INDEX IF NOT EXISTS idx_events_start_time ON events(start_time);
        """
    )
    conn.commit()
    conn.close()

ADMIN_CREDENTIALS = {
    'email': 'admin@aubmed.ac.cy',
    'password': 'Admin'
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        if email == ADMIN_CREDENTIALS['email'] and password == ADMIN_CREDENTIALS['password']:
            session["user_id"] = "admin"
            session["is_admin"] = True
            session["full_name"] = "Admin"
            flash("Admin login successful!", "success")
            return redirect(url_for("admin_dashboard"))
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["full_name"] = user["full_name"]
            details = conn.execute(
                "SELECT languages, bio, phone_number, interests FROM user_details WHERE user_id = ?", 
                (user["id"],)
            ).fetchone()
            
            conn.close()
            if not details or not all([details["languages"], details["bio"], details["phone_number"], details["interests"]]):
                flash("Please complete your profile", "info")
                return redirect(url_for("complete_profile"))
            
            if not user["is_approved"]:
                flash("Your account is pending approval from the administrator", "warning")
                return redirect(url_for("login"))
            
            flash(f"Welcome back, {user['full_name']}!", "success")
            return redirect(url_for(f"{user['role']}_dashboard"))
        else:
            conn.close()
            flash("Invalid email or password", "error")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    if 'user_id' in session:
        session.clear()
        flash("You have been successfully logged out", "info")
    else:
        flash("You were not logged in", "info")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        if not email.endswith("@aubmed.ac.cy"):
            flash("Please use your university email address (@aubmed.ac.cy)", "error")
            return redirect(url_for("register"))
        dummy_match = next((s for s in DUMMY_STUDENT_DATA if s['email'].lower() == email.lower()), None)
        if not dummy_match:
            flash("Email not found in university records", "error")
            return redirect(url_for("register"))
        if role == "buddy" and dummy_match['academic_year'] < 2:
            flash("Only students in their second year or higher can register as buddies", "error")
            return redirect(url_for("register"))
        
        conn = get_db_connection()
        try:
            existing_user = conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone()
            if existing_user:
                flash("Email address is already registered", "error")
                return redirect(url_for("register"))
            username = email.split("@")[0]
            conn.execute(
                "INSERT INTO users (username, password_hash, email, full_name, role, is_approved) VALUES (?, ?, ?, ?, ?, ?)",
                (username, generate_password_hash(password), email, dummy_match['full_name'], role, False)
            )
            conn.commit()
            user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
            conn.execute(
                """INSERT INTO user_details 
                (user_id, student_id_number, age, gender, major, academic_year)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (user["id"], dummy_match['student_id'], dummy_match['age'], 
                 dummy_match['gender'], dummy_match['major'], dummy_match['academic_year'])
            )
            conn.commit()
            session["user_id"] = user["id"]
            session["role"] = role
            session["full_name"] = dummy_match['full_name']
            flash("Please complete your profile", "info")
            return redirect(url_for("complete_profile"))
            
        except Exception as e:
            flash(f"Registration error: {str(e)}", "error")
        finally:
            conn.close()
    email = request.args.get("email", "")
    show_buddy_option = False
    
    if email.endswith("@aubmed.ac.cy"):
        dummy_match = next((s for s in DUMMY_STUDENT_DATA if s['email'].lower() == email.lower()), None)
        if dummy_match and dummy_match['academic_year'] >= 2:
            show_buddy_option = True
    
    return render_template("register.html", 
                         email=email,
                         show_buddy_option=show_buddy_option)


@app.route("/complete-profile", methods=["GET", "POST"])
def complete_profile():
    if "user_id" not in session:
        flash("Please login to access this page", "warning")
        return redirect(url_for("login"))
    country_codes = [
        ("+961", "Lebanon (+961)"),
        ("+357", "Cyprus (+357)"),
        ("+971", "United Arab Emirates (+971)"),
        ("+1", "USA (+1)"),
        ("+44", "UK (+44)"),
    ]
    
    interests = [
        "Programming", "Sports", "Music", "Reading", "Traveling",
        "Photography", "Cooking", "Gaming", "Art", "Movies",
        "Hiking", "Dancing", "Languages", "Volunteering", "Entrepreneurship"
    ]
    
    if request.method == "POST":
        languages = request.form.get("languages")
        nationality = request.form.get("nationality")
        bio = request.form.get("bio")
        phone_country_code = request.form.get("phone_country_code")
        phone_number = request.form.get("phone_number")
        selected_interests = request.form.getlist("interests")
        interests_str = ",".join(selected_interests)
        if phone_number and not phone_number.isdigit():
            flash("Phone number should contain only digits", "error")
            return redirect(url_for("complete_profile"))
        full_phone = f"{phone_country_code}{phone_number}" if phone_number else None
        
        conn = None
        try:
            conn = get_db_connection()
            conn.execute(
                """UPDATE user_details 
                SET languages = ?, nationality = ?, bio = ?, phone_number = ?, interests = ?
                WHERE user_id = ?""",
                (languages, nationality, bio, full_phone, interests_str, session["user_id"])
            )
            conn.commit()
            flash("Profile completed successfully! Please wait for administrator approval.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error saving profile: {str(e)}", "error")
        finally:
            if conn:
                conn.close()
    
    return render_template("complete_profile.html", 
                         interests=interests,
                         country_codes=country_codes)

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))
    
    try:
        conn = get_db_connection()
        pending_users = conn.execute(
            "SELECT * FROM users WHERE is_approved = 0"
        ).fetchall()
        
        recent_matches = conn.execute(
            """SELECT bm.*, u1.full_name as buddy_name, u2.full_name as student_name 
            FROM buddy_matches bm
            JOIN users u1 ON bm.buddy_id = u1.id
            JOIN users u2 ON bm.student_id = u2.id
            ORDER BY bm.created_at DESC LIMIT 5"""
        ).fetchall()
        
        total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active_matches = conn.execute(
            "SELECT COUNT(*) FROM buddy_matches WHERE status = 'active'"
        ).fetchone()[0]
        
        return render_template("admin_dashboard.html", 
                             pending_users=pending_users,
                             recent_matches=recent_matches,
                             stats={'total_users': total_users, 
                                   'active_matches': active_matches})
    
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        return redirect(url_for("index"))
    finally:
        if 'conn' in locals():
            conn.close()

@app.route("/admin/approve-user/<int:user_id>")
def approve_user(user_id):
    if not session.get("is_admin"):
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    try:
        conn.execute("UPDATE users SET is_approved = 1 WHERE id = ?", (user_id,))
        conn.commit()
        flash("User approved successfully", "success")
    except Exception as e:
        flash(f"Error approving user: {str(e)}", "error")
    finally:
        conn.close()
    
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/reject-user/<int:user_id>")
def reject_user(user_id):
    if not session.get("is_admin"):
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM user_details WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        
        flash("User registration has been rejected and all data removed", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error rejecting user: {str(e)}", "error")
    finally:
        conn.close()
    
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/user-details/<int:user_id>")
def user_details(user_id):
    if not session.get("is_admin"):
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))
    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            flash("User not found", "error")
            return redirect(url_for("admin_dashboard"))
        details = conn.execute(
            "SELECT * FROM user_details WHERE user_id = ?", (user_id,)
        ).fetchone()
        return render_template("user_details.html", user=user, details=details)
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists("buddy_system.db"):
        initialize_db()
    app.run(debug=True)