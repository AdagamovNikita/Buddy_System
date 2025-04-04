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

def initialize_db():
    conn = get_db_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'buddy')),
            is_approved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_details (
            user_id INTEGER PRIMARY KEY,
            student_id_number TEXT UNIQUE,
            age INTEGER,
            gender TEXT,
            nationality TEXT,
            major TEXT NOT NULL,
            academic_year INTEGER CHECK(academic_year BETWEEN 1 AND 5),
            languages TEXT,
            bio TEXT,
            phone_number TEXT,
            is_international BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS buddy_preferences (
            user_id INTEGER PRIMARY KEY,
            preferred_role TEXT NOT NULL CHECK(preferred_role IN ('advisor', 'mentor', 'friend')),
            preferred_gender TEXT,
            min_preferred_age INTEGER,
            max_preferred_age INTEGER,
            preferred_major TEXT,
            preferred_language TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS buddy_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buddy_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'active', 'declined', 'completed', 'paused')) DEFAULT 'pending',
            match_score INTEGER,
            matched_by_admin BOOLEAN DEFAULT FALSE,
            admin_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (buddy_id, student_id),
            CHECK (buddy_id != student_id),
            FOREIGN KEY (buddy_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS video_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            initiator_id INTEGER NOT NULL,
            recipient_id INTEGER NOT NULL,
            scheduled_time TIMESTAMP NOT NULL,
            duration_minutes INTEGER,
            call_status TEXT CHECK(call_status IN ('scheduled', 'completed', 'missed', 'canceled')),
            notes TEXT,
            FOREIGN KEY (initiator_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            interaction_type TEXT NOT NULL CHECK(interaction_type IN ('message', 'call', 'meeting', 'event')),
            points_earned INTEGER NOT NULL DEFAULT 0,
            interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duration_minutes INTEGER,
            notes TEXT,
            FOREIGN KEY (match_id) REFERENCES buddy_matches(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS leaderboard (
            user_id INTEGER PRIMARY KEY,
            total_points INTEGER DEFAULT 0,
            current_rank INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reviewer_id INTEGER NOT NULL,
            reviewed_id INTEGER NOT NULL,
            match_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            comments TEXT,
            is_anonymous BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (reviewed_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (match_id) REFERENCES buddy_matches(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            event_type TEXT CHECK(event_type IN ('mentorship', 'social', 'academic', 'workshop')),
            location TEXT,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            max_attendees INTEGER,
            organizer_id INTEGER NOT NULL,
            is_public BOOLEAN DEFAULT TRUE,
            points_value INTEGER DEFAULT 0,
            FOREIGN KEY (organizer_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS event_attendees (
            event_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            attended BOOLEAN DEFAULT FALSE,
            points_earned INTEGER DEFAULT 0,
            PRIMARY KEY (event_id, user_id),
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            day_of_week INTEGER CHECK(day_of_week BETWEEN 0 AND 6),
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            is_recurring BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS scheduled_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            scheduled_time TIMESTAMP NOT NULL,
            duration_minutes INTEGER NOT NULL,
            session_type TEXT CHECK(session_type IN ('academic', 'social', 'career', 'other')),
            status TEXT CHECK(status IN ('scheduled', 'completed', 'canceled', 'no-show')) DEFAULT 'scheduled',
            location TEXT,
            notes TEXT,
            FOREIGN KEY (match_id) REFERENCES buddy_matches(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT NOT NULL,
            target_user_id INTEGER,
            description TEXT,
            performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (target_user_id) REFERENCES users(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            target_roles TEXT,
            is_pinned BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            notification_type TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            related_entity_type TEXT,
            related_entity_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            if not user["is_approved"]:
                flash("Your account is pending approval from the administrator", "warning")
                return redirect(url_for("login"))
            
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["full_name"] = user["full_name"]
            conn = get_db_connection()
            profile_complete = conn.execute(
                "SELECT 1 FROM user_details WHERE user_id = ?", (user["id"],)
            ).fetchone()
            conn.close()

            if not profile_complete and user["role"] != "admin":
                flash("Please complete your profile information", "info")
                return redirect(url_for("complete_profile"))

            flash(f"Welcome back, {user['full_name']}!", "success")
            return redirect(url_for(f"{user['role']}_dashboard"))
        else:
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
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        
        if not all([full_name, email, password, role]):
            flash("Please fill in all required fields", "error")
            return redirect(url_for("register"))
        
        if role not in ["student", "buddy"]:
            flash("Invalid role selected", "error")
            return redirect(url_for("register"))
        
        conn = get_db_connection()
        try:
            username = email.split("@")[0]
            conn.execute(
                "INSERT INTO users (username, password_hash, email, full_name, role) VALUES (?, ?, ?, ?, ?)",
                (username, generate_password_hash(password), email, full_name, role)
            )
            conn.commit()
            flash("Registration successful! Please wait for administrator approval.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email address is already registered", "error")
        finally:
            conn.close()
    
    return render_template("register.html")

@app.route("/complete-profile", methods=["GET", "POST"])
def complete_profile():
    if "user_id" not in session:
        flash("Please log in to complete your profile.", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    print(f"User ID from session: {user_id}")  

    conn = get_db_connection()
    existing_profile = conn.execute(
        "SELECT * FROM user_details WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()

    print(f"Existing profile: {existing_profile}")  

    if request.method == "POST":
        student_id = request.form.get("student_id")
        age = request.form.get("age")
        gender = request.form.get("gender")
        nationality = request.form.get("nationality")
        major = request.form.get("major")
        academic_year = request.form.get("academic_year")
        languages = request.form.get("languages")
        bio = request.form.get("bio")
        phone = request.form.get("phone")

        print(f"Form Data Received: {student_id}, {age}, {gender}, {nationality}, {major}, {academic_year}, {languages}, {bio}, {phone}")

        conn = get_db_connection()
        try:
            if existing_profile:
                print("Updating existing profile...")  
                conn.execute(
                    """UPDATE user_details 
                    SET student_id_number = ?, age = ?, gender = ?, nationality = ?, 
                        major = ?, academic_year = ?, languages = ?, bio = ?, phone_number = ? 
                    WHERE user_id = ?""",
                    (student_id, age, gender, nationality, major, academic_year, languages, bio, phone, user_id)
                )
            else:
                print("Inserting new profile...") 
                conn.execute(
                    """INSERT INTO user_details 
                    (user_id, student_id_number, age, gender, nationality, major, academic_year, languages, bio, phone_number)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (user_id, student_id, age, gender, nationality, major, academic_year, languages, bio, phone)
                )
            conn.commit()
            print("Profile saved successfully!")  
            flash("Profile saved successfully!", "success")
            return redirect(url_for("view_profile"))
        except Exception as e:
            print(f"Error saving profile: {e}")  
            flash(f"Error saving profile: {str(e)}", "error")
        finally:
            conn.close()

    return render_template("complete_profile.html", profile=existing_profile)

@app.route("/view_profile")
def view_profile():
    user_id = session.get("user_id")
    print(f"Accessing profile for user_id: {user_id}")  

    if not user_id:
        print("User ID is missing. Redirecting to login.")
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()

    profile = conn.execute("SELECT * FROM user_details WHERE user_id = ?", (user_id,)).fetchone()

    role = conn.execute("SELECT role FROM users WHERE id = ?", (user_id,)).fetchone()

    conn.close()

    print(f"Profile data fetched: {profile}")  
    print(f"User role fetched: {role}")  

    if not profile:
        print("No profile found, redirecting to complete-profile.")  
        flash("Profile not found. Please complete your profile.", "warning")
        return redirect(url_for("complete_profile"))

    user_role = role[0] if role else None

    return render_template("view_profile.html", profile=profile, user_role=user_role)


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))
    
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
    
    conn.close()
    
    return render_template("admin_dashboard.html", 
                         pending_users=pending_users,
                         recent_matches=recent_matches)

@app.route("/admin/approve-user/<int:user_id>")
def approve_user(user_id):
    if not session.get("is_admin"):
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE users SET is_approved = 1 WHERE id = ?", (user_id,)
        )
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
        conn.execute(
            "DELETE FROM users WHERE id = ? AND is_approved = 0", (user_id,)
        )
        conn.commit()
        flash("User rejected and removed", "success")
    except Exception as e:
        flash(f"Error rejecting user: {str(e)}", "error")
    finally:
        conn.close()
    
    return redirect(url_for("admin_dashboard"))

@app.route("/student/dashboard")
def student_dashboard():
    if "user_id" not in session or session["role"] != "student":
        flash("Please login as a student to access this page", "warning")
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    profile_complete = conn.execute(
        "SELECT 1 FROM user_details WHERE user_id = ?", (session["user_id"],)
    ).fetchone()
    
    if not profile_complete:
        flash("Please complete your profile first", "info")
        return redirect(url_for("complete_profile"))
    
    matches = conn.execute(
        """SELECT bm.*, u.full_name as buddy_name 
        FROM buddy_matches bm
        JOIN users u ON bm.buddy_id = u.id
        WHERE bm.student_id = ?""", (session["user_id"],)
    ).fetchall()
    
    events = conn.execute(
        """SELECT * FROM events 
        WHERE is_public = 1 AND start_time > datetime('now')
        ORDER BY start_time LIMIT 5"""
    ).fetchall()
    
    conn.close()
    
    return render_template("student_dashboard.html",
                         full_name=session["full_name"],
                         matches=matches,
                         events=events)

@app.route("/buddy/dashboard")
def buddy_dashboard():
    if "user_id" not in session or session["role"] != "buddy":
        flash("Please login as a buddy to access this page", "warning")
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    profile_complete = conn.execute(
        "SELECT 1 FROM user_details WHERE user_id = ?", (session["user_id"],)
    ).fetchone()
    
    if not profile_complete:
        flash("Please complete your profile first", "info")
        return redirect(url_for("complete_profile"))
    
    matches = conn.execute(
        """SELECT bm.*, u.full_name as student_name 
        FROM buddy_matches bm
        JOIN users u ON bm.student_id = u.id
        WHERE bm.buddy_id = ?""", (session["user_id"],)
    ).fetchall()
    
    sessions = conn.execute(
        """SELECT ss.*, u.full_name as student_name 
        FROM scheduled_sessions ss
        JOIN buddy_matches bm ON ss.match_id = bm.id
        JOIN users u ON bm.student_id = u.id
        WHERE bm.buddy_id = ? AND ss.status = 'scheduled'
        ORDER BY ss.scheduled_time LIMIT 5""", (session["user_id"],)
    ).fetchall()
    
    conn.close()
    
    return render_template("buddy_dashboard.html",
                         full_name=session["full_name"],
                         matches=matches,
                         sessions=sessions)

if __name__ == "__main__":
    if not os.path.exists("buddy_system.db"):
        initialize_db()
    app.run(debug=True)