from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"


def get_db_connection():
    conn = sqlite3.connect("buddy_system.db")
    conn.row_factory = sqlite3.Row
    return conn


# ignore the majors for now. all of them say bachelor of science regardless of the major, this is just from the dummy data and is not an error with the database or
DUMMY_STUDENT_DATA = [
    {
        "full_name": "Sam Al Khoury",
        "student_id": "100000018",
        "age": 18,
        "gender": "male",
        "major": "Computer Science",
        "academic_year": 2,
        "email": "sja00@aubmed.ac.cy",
    },
    {
        "full_name": "Omar Kaddour",
        "student_id": "100000001",
        "age": 19,
        "gender": "male",
        "major": "Computer Science",
        "academic_year": 2,
        "email": "osa00@aubmed.ac.cy",
    },
    {
        "full_name": "Ryan Dibeh",
        "student_id": "100000019",
        "age": 18,
        "gender": "male",
        "major": "Psychology",
        "academic_year": 1,
        "email": "rad00@aubmed.ac.cy",
    },
    {
        "full_name": "Layla Hammoud",
        "student_id": "100000020",
        "age": 20,
        "gender": "female",
        "major": "Business",
        "academic_year": 3,
        "email": "lha00@aubmed.ac.cy",
    },
    {
        "full_name": "Karim Nasser",
        "student_id": "100000021",
        "age": 19,
        "gender": "male",
        "major": "PPE",
        "academic_year": 2,
        "email": "kna00@aubmed.ac.cy",
    },
    {
        "full_name": "Maya Farah",
        "student_id": "100000022",
        "age": 18,
        "gender": "female",
        "major": "Industrial Engineering",
        "academic_year": 1,
        "email": "mfa00@aubmed.ac.cy",
    },
    {
        "full_name": "Ziad Abadi",
        "student_id": "100000023",
        "age": 21,
        "gender": "male",
        "major": "Computer Science",
        "academic_year": 4,
        "email": "zab00@aubmed.ac.cy",
    },
    {
        "full_name": "Nour El Din",
        "student_id": "100000024",
        "age": 20,
        "gender": "female",
        "major": "Psychology",
        "academic_year": 3,
        "email": "nel00@aubmed.ac.cy",
    },
    {
        "full_name": "Tarek Mansour",
        "student_id": "100000025",
        "age": 19,
        "gender": "male",
        "major": "Business",
        "academic_year": 2,
        "email": "tma00@aubmed.ac.cy",
    },
    {
        "full_name": "Hala Zaytoun",
        "student_id": "100000026",
        "age": 18,
        "gender": "female",
        "major": "PPE",
        "academic_year": 1,
        "email": "hza00@aubmed.ac.cy",
    },
    {
        "full_name": "Fadi Jaber",
        "student_id": "100000027",
        "age": 22,
        "gender": "male",
        "major": "Industrial Engineering",
        "academic_year": 4,
        "email": "fja00@aubmed.ac.cy",
    },
    {
        "full_name": "Rima Chahine",
        "student_id": "100000028",
        "age": 20,
        "gender": "female",
        "major": "Computer Science",
        "academic_year": 3,
        "email": "rch00@aubmed.ac.cy",
    },
    {
        "full_name": "Ali Saad",
        "student_id": "100000029",
        "age": 19,
        "gender": "male",
        "major": "Psychology",
        "academic_year": 2,
        "email": "asa00@aubmed.ac.cy",
    },
    {
        "full_name": "Yara Haddad",
        "student_id": "100000030",
        "age": 18,
        "gender": "female",
        "major": "Business",
        "academic_year": 1,
        "email": "yha00@aubmed.ac.cy",
    },
    {
        "full_name": "Bassel Maroun",
        "student_id": "100000031",
        "age": 21,
        "gender": "male",
        "major": "PPE",
        "academic_year": 4,
        "email": "bma00@aubmed.ac.cy",
    },
    {
        "full_name": "Dana Halabi",
        "student_id": "100000032",
        "age": 20,
        "gender": "female",
        "major": "Industrial Engineering",
        "academic_year": 3,
        "email": "dha00@aubmed.ac.cy",
    },
    {
        "full_name": "Wissam Tannous",
        "student_id": "100000033",
        "age": 19,
        "gender": "male",
        "major": "Computer Science",
        "academic_year": 2,
        "email": "wta00@aubmed.ac.cy",
    },
    {
        "full_name": "Leila Asmar",
        "student_id": "100000034",
        "age": 18,
        "gender": "female",
        "major": "Psychology",
        "academic_year": 1,
        "email": "las00@aubmed.ac.cy",
    },
    {
        "full_name": "Jad Younes",
        "student_id": "100000035",
        "age": 22,
        "gender": "male",
        "major": "Business",
        "academic_year": 4,
        "email": "jyo00@aubmed.ac.cy",
    },
    {
        "full_name": "Sara Makdisi",
        "student_id": "100000036",
        "age": 20,
        "gender": "female",
        "major": "PPE",
        "academic_year": 3,
        "email": "sma00@aubmed.ac.cy",
    },
    {
        "full_name": "Rami Itani",
        "student_id": "100000037",
        "age": 19,
        "gender": "male",
        "major": "Industrial Engineering",
        "academic_year": 2,
        "email": "rit00@aubmed.ac.cy",
    },
    {
        "full_name": "Lina Daher",
        "student_id": "100000038",
        "age": 18,
        "gender": "female",
        "major": "Computer Science",
        "academic_year": 1,
        "email": "lda00@aubmed.ac.cy",
    },
    {
        "full_name": "Hadi Fakhry",
        "student_id": "100000039",
        "age": 21,
        "gender": "male",
        "major": "Psychology",
        "academic_year": 4,
        "email": "hfa00@aubmed.ac.cy",
    },
    {
        "full_name": "Nadia Saliba",
        "student_id": "100000040",
        "age": 20,
        "gender": "female",
        "major": "Business",
        "academic_year": 3,
        "email": "nsa00@aubmed.ac.cy",
    },
    {
        "full_name": "Sam Dibeh",
        "student_id": "100000041",
        "age": 20,
        "gender": "male",
        "major": "Computer Science",
        "academic_year": 2,
        "email": "sdi00@aubmed.ac.cy",
    },
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
            admin_approved BOOLEAN DEFAULT FALSE,  -- Make sure this is included
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


ADMIN_CREDENTIALS = {"email": "admin@aubmed.ac.cy", "password": "Admin"}


def get_potential_buddies(
    student_id,
    major_filter=None,
    language_filter=None,
    year_filter=None,
    gender_filter=None,
):
    conn = get_db_connection()
    try:
        student_details = conn.execute(
            """SELECT ud.*, bp.preferred_gender, bp.min_preferred_age, 
                  bp.max_preferred_age, bp.preferred_major, bp.preferred_language
               FROM user_details ud
               LEFT JOIN buddy_preferences bp ON ud.user_id = bp.user_id
               WHERE ud.user_id = ?""",
            (student_id,),
        ).fetchone()
        if not student_details:
            return []
        query = """SELECT u.id, u.full_name, ud.*, 
                  (SELECT COUNT(*) FROM buddy_matches 
                   WHERE buddy_id = u.id AND status = 'active') as active_matches
               FROM users u
               JOIN user_details ud ON u.id = ud.user_id
               WHERE u.role = 'buddy' 
               AND u.is_approved = 1
               AND u.id NOT IN (
                   SELECT buddy_id FROM buddy_matches 
                   WHERE student_id = ? AND status IN ('active', 'pending')
               )
               AND u.id != ?"""
        params = [student_id, student_id]
        if gender_filter:
            query += " AND LOWER(ud.gender) = LOWER(?)"
            params.append(gender_filter)
        if major_filter:
            query += " AND ud.major = ?"
            params.append(major_filter)
        if language_filter:
            query += " AND ud.languages LIKE ?"
            params.append(f"%{language_filter}%")
        if year_filter:
            query += " AND ud.academic_year = ?"
            params.append(int(year_filter))
        potential_buddies = conn.execute(query, params).fetchall()
        if not potential_buddies:
            return []
        scored_buddies = []
        for buddy in potential_buddies:
            score = 0
            if student_details["major"] and buddy["major"]:
                if student_details["major"] == buddy["major"]:
                    score += 30
            if student_details["languages"] and buddy["languages"]:
                student_langs = [
                    lang.strip().lower()
                    for lang in student_details["languages"].split(",")
                ]
                buddy_langs = [
                    lang.strip().lower() for lang in buddy["languages"].split(",")
                ]
                if student_langs[0] == buddy_langs[0]:
                    score += 15
                common_langs = set(student_langs).intersection(buddy_langs)
                if common_langs:
                    score += min(10, len(common_langs) * 2)
            if student_details["academic_year"] and buddy["academic_year"]:
                year_diff = abs(
                    student_details["academic_year"] - buddy["academic_year"]
                )
                if year_diff == 0:
                    score += 20
                elif year_diff == 1:
                    score += 15
                elif year_diff == 2:
                    score += 5
            if student_details["interests"] and buddy["interests"]:
                student_interests = set(
                    i.strip().lower() for i in student_details["interests"].split(",")
                )
                buddy_interests = set(
                    i.strip().lower() for i in buddy["interests"].split(",")
                )
                common_interests = student_interests.intersection(buddy_interests)
                if common_interests:
                    score += min(20, len(common_interests) * 5)
            if buddy["active_matches"] < 2:
                score += 10 - (buddy["active_matches"] * 5)
            score = max(0, min(100, score))

            scored_buddies.append(
                {
                    "buddy_id": buddy["id"],
                    "name": buddy["full_name"],
                    "score": score,
                    "major": buddy["major"],
                    "languages": buddy["languages"],
                    "interests": buddy["interests"],
                    "academic_year": buddy["academic_year"],
                    "gender": buddy["gender"],
                    "age": buddy["age"],
                    "nationality": buddy["nationality"],
                    "active_matches": buddy["active_matches"],
                }
            )
        scored_buddies.sort(key=lambda x: (-x["score"], x["active_matches"]))
        return scored_buddies

    except Exception as e:
        print(f"Error finding potential buddies: {str(e)}")
        return []
    finally:
        conn.close()


def add_admin_approved_column():
    conn = get_db_connection()
    try:
        conn.execute("PRAGMA table_info(buddy_matches);")
        columns = [column[1] for column in conn.fetchall()]
        if "admin_approved" not in columns:
            conn.execute(
                """
                ALTER TABLE buddy_matches
                ADD COLUMN admin_approved BOOLEAN DEFAULT FALSE;
            """
            )
            conn.commit()
            print("Column 'admin_approved' added successfully.")
        else:
            print("Column 'admin_approved' already exists.")

    except Exception as e:
        print(f"Error adding column: {e}")

    finally:
        conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if (
            email == ADMIN_CREDENTIALS["email"]
            and password == ADMIN_CREDENTIALS["password"]
        ):
            session["user_id"] = "admin"
            session["is_admin"] = True
            session["full_name"] = "Admin"
            flash("Admin login successful!", "success")
            return redirect(url_for("admin_dashboard"))

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user and password:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["full_name"] = user["full_name"]
            details = conn.execute(
                "SELECT languages, bio, phone_number, interests FROM user_details WHERE user_id = ?",
                (user["id"],),
            ).fetchone()

            conn.close()
            if not details or not all(
                [
                    details["languages"],
                    details["bio"],
                    details["phone_number"],
                    details["interests"],
                ]
            ):
                flash("Please complete your profile", "info")
                return redirect(url_for("complete_profile"))

            if not user["is_approved"]:
                flash(
                    "Your account is pending approval from the administrator", "warning"
                )
                return redirect(url_for("login"))
            return redirect(url_for(f"{user['role']}_dashboard"))
        else:
            conn.close()
            flash("Invalid email or password", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    if "user_id" in session:
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
        dummy_match = next(
            (s for s in DUMMY_STUDENT_DATA if s["email"].lower() == email.lower()), None
        )
        if not dummy_match:
            flash("Email not found in university records", "error")
            return redirect(url_for("register"))
        if role == "buddy" and dummy_match["academic_year"] < 2:
            flash(
                "Only students in their second year or higher can register as buddies",
                "error",
            )
            return redirect(url_for("register"))

        conn = get_db_connection()
        try:
            existing_user = conn.execute(
                "SELECT 1 FROM users WHERE email = ?", (email,)
            ).fetchone()
            if existing_user:
                flash("Email address is already registered", "error")
                return redirect(url_for("register"))
            username = email.split("@")[0]
            conn.execute(
                "INSERT INTO users (username, password_hash, email, full_name, role, is_approved) VALUES (?, ?, ?, ?, ?, ?)",
                (username, password, email, dummy_match["full_name"], role, False),
            )
            conn.commit()
            user = conn.execute(
                "SELECT id FROM users WHERE email = ?", (email,)
            ).fetchone()
            conn.execute(
                """INSERT INTO user_details 
                (user_id, student_id_number, age, gender, major, academic_year)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    user["id"],
                    dummy_match["student_id"],
                    dummy_match["age"],
                    dummy_match["gender"],
                    dummy_match["major"],
                    dummy_match["academic_year"],
                ),
            )
            conn.commit()
            session["user_id"] = user["id"]
            session["role"] = role
            session["full_name"] = dummy_match["full_name"]
            flash("Please complete your profile", "info")
            return redirect(url_for("complete_profile"))

        except Exception as e:
            flash(f"Registration error: {str(e)}", "error")
        finally:
            conn.close()
    email = request.args.get("email", "")
    show_buddy_option = False

    if email.endswith("@aubmed.ac.cy"):
        dummy_match = next(
            (s for s in DUMMY_STUDENT_DATA if s["email"].lower() == email.lower()), None
        )
        if dummy_match and dummy_match["academic_year"] >= 2:
            show_buddy_option = True

    return render_template(
        "register.html", email=email, show_buddy_option=show_buddy_option
    )


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
        "Programming",
        "Sports",
        "Music",
        "Reading",
        "Traveling",
        "Photography",
        "Cooking",
        "Gaming",
        "Art",
        "Movies",
        "Hiking",
        "Dancing",
        "Languages",
        "Volunteering",
        "Entrepreneurship",
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
                (
                    languages,
                    nationality,
                    bio,
                    full_phone,
                    interests_str,
                    session["user_id"],
                ),
            )
            conn.commit()
            flash(
                "Profile completed successfully! Please wait for administrator approval.",
                "success",
            )
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error saving profile: {str(e)}", "error")
        finally:
            if conn:
                conn.close()

    return render_template(
        "complete_profile.html", interests=interests, country_codes=country_codes
    )


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

        pending_matches = conn.execute(
            """SELECT bm.*, u1.full_name as buddy_name, u2.full_name as student_name 
            FROM buddy_matches bm
            JOIN users u1 ON bm.buddy_id = u1.id
            JOIN users u2 ON bm.student_id = u2.id
            WHERE bm.status = 'pending'"""
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

        return render_template(
            "admin_dashboard.html",
            pending_users=pending_users,
            pending_matches=pending_matches,
            recent_matches=recent_matches,
            stats={"total_users": total_users, "active_matches": active_matches},
        )

    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        return redirect(url_for("index"))
    finally:
        if "conn" in locals():
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
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user:
            flash("User not found", "error")
            return redirect(url_for("admin_dashboard"))
        details = conn.execute(
            "SELECT * FROM user_details WHERE user_id = ?", (user_id,)
        ).fetchone()
        return render_template("user_details.html", user=user, details=details)
    finally:
        conn.close()


@app.route("/student/dashboard")
def student_dashboard():
    if "user_id" not in session or session["role"] != "student":
        flash("Please login as a student to access this page", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT is_approved FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()

        if not user["is_approved"]:
            flash("Your account is pending approval from the administrator", "warning")
            return redirect(url_for("login"))

        user_details = conn.execute(
            "SELECT * FROM user_details WHERE user_id = ?", (session["user_id"],)
        ).fetchone()

        if not user_details:
            flash("Please complete your profile first", "info")
            return redirect(url_for("complete_profile"))

        matches = conn.execute(
            """SELECT bm.*, u.full_name as buddy_name, 
               datetime(bm.created_at) as formatted_created_at
               FROM buddy_matches bm
               JOIN users u ON bm.buddy_id = u.id
               WHERE bm.student_id = ?""",
            (session["user_id"],),
        ).fetchall()

        approved_matches = [m for m in matches if m["status"] in ("approved", "active")]

        pending_matches = conn.execute(
            """SELECT bm.*, u.full_name as buddy_name, 
               datetime(bm.created_at) as formatted_created_at
               FROM buddy_matches bm
               JOIN users u ON bm.buddy_id = u.id
               WHERE bm.student_id = ? AND bm.status = 'pending'""",
            (session["user_id"],),
        ).fetchall()

        events = conn.execute(
            """SELECT *, datetime(start_time) as formatted_start_time 
               FROM events 
               WHERE is_public = 1 AND start_time > datetime('now')
               ORDER BY start_time LIMIT 5"""
        ).fetchall()

        pending_request = conn.execute(
            "SELECT 1 FROM buddy_matches WHERE student_id = ?",
            (session["user_id"],)
        ).fetchone()

        return render_template(
            "student_dashboard.html",
            full_name=session["full_name"],
            user_details=user_details,
            matches=matches,
            pending_matches=pending_matches,
            events=events,
            approved_matches=approved_matches,
            pending_request=pending_request,
        )
    finally:
        conn.close()


@app.route("/buddy/dashboard")
def buddy_dashboard():
    if "user_id" not in session or session["role"] != "buddy":
        flash("Please login as a buddy to access this page", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT is_approved FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()

        if not user["is_approved"]:
            flash("Your account is pending approval from the administrator", "warning")
            return redirect(url_for("login"))

        user_details = conn.execute(
            "SELECT * FROM user_details WHERE user_id = ?", (session["user_id"],)
        ).fetchone()

        if not user_details:
            flash("Please complete your profile first", "info")
            return redirect(url_for("complete_profile"))

        matches = conn.execute(
            """SELECT bm.*, u.full_name as student_name, 
               datetime(bm.created_at) as formatted_created_at
               FROM buddy_matches bm
               JOIN users u ON bm.student_id = u.id
               WHERE bm.buddy_id = ?""",
            (session["user_id"],),
        ).fetchall()

        approved_matches = [
            m for m in matches if m["status"].lower() in ("approved", "active")
        ]

        pending_matches = conn.execute(
            """SELECT bm.*, u.full_name as student_name, 
               datetime(bm.created_at) as formatted_created_at
               FROM buddy_matches bm
               JOIN users u ON bm.student_id = u.id
               WHERE bm.buddy_id = ? AND bm.status = 'pending'""",
            (session["user_id"],),
        ).fetchall()

        sessions = conn.execute(
            """SELECT ss.*, u.full_name as student_name, 
               datetime(ss.scheduled_time) as formatted_scheduled_time
               FROM scheduled_sessions ss
               JOIN buddy_matches bm ON ss.match_id = bm.id
               JOIN users u ON bm.student_id = u.id
               WHERE bm.buddy_id = ? AND ss.status = 'scheduled'
               ORDER BY ss.scheduled_time LIMIT 5""",
            (session["user_id"],),
        ).fetchall()

        events = conn.execute(
            """SELECT *, datetime(start_time) as formatted_start_time 
               FROM events 
               WHERE is_public = 1 AND start_time > datetime('now')
               ORDER BY start_time LIMIT 5"""
        ).fetchall()

        return render_template(
            "buddy_dashboard.html",
            full_name=session["full_name"],
            user_details=user_details,
            matches=matches,
            approved_matches=approved_matches,
            pending_matches=pending_matches,
            sessions=sessions,
            events=events,
        )
    finally:
        conn.close()


@app.route("/potential-matches")
def view_potential_matches():
    if "user_id" not in session or session["role"] != "student":
        flash("Please login as a student to view matches", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    try:
        major_filter = request.args.get("major", "")
        language_filter = request.args.get("language", "")
        year_filter = request.args.get("year", "")
        gender_filter = request.args.get("gender", "")
        matches = get_potential_buddies(
            session["user_id"],
            major_filter=major_filter if major_filter else None,
            language_filter=language_filter if language_filter else None,
            year_filter=year_filter if year_filter else None,
            gender_filter=gender_filter if gender_filter else None,
        )

        return render_template(
            "potential_matches.html", matches=matches, full_name=session["full_name"]
        )
    finally:
        conn.close()

@app.route("/buddy-details/<int:buddy_id>")
def buddy_details(buddy_id):
    if "user_id" not in session or session["role"] != "student":
        flash("Please login as a student to view buddy details", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    try:
        buddy = conn.execute(
            """SELECT u.id as buddy_id, u.full_name as name, ud.* 
            FROM users u
            JOIN user_details ud ON u.id = ud.user_id
            WHERE u.id = ? AND u.role = 'buddy' AND u.is_approved = 1""",
            (buddy_id,),
        ).fetchone()

        if not buddy:
            flash("Buddy not found", "error")
            return redirect(url_for("view_potential_matches"))

        student_details = conn.execute(
            "SELECT * FROM user_details WHERE user_id = ?", (session["user_id"],)
        ).fetchone()

        match_score = 0
        if student_details:
            if student_details["major"] and buddy["major"]:
                if student_details["major"] == buddy["major"]:
                    match_score += 30
            if student_details["languages"] and buddy["languages"]:
                student_langs = [
                    lang.strip().lower()
                    for lang in student_details["languages"].split(",")
                ]
                buddy_langs = [
                    lang.strip().lower() for lang in buddy["languages"].split(",")
                ]
                if student_langs[0] == buddy_langs[0]:
                    match_score += 15
                common_langs = set(student_langs).intersection(buddy_langs)
                if common_langs:
                    match_score += min(10, len(common_langs) * 2)
            if student_details["academic_year"] and buddy["academic_year"]:
                year_diff = abs(
                    student_details["academic_year"] - buddy["academic_year"]
                )
                if year_diff == 0:
                    match_score += 20
                elif year_diff == 1:
                    match_score += 15
                elif year_diff == 2:
                    match_score += 5
            if student_details["interests"] and buddy["interests"]:
                student_interests = set(
                    i.strip().lower() for i in student_details["interests"].split(",")
                )
                buddy_interests = set(
                    i.strip().lower() for i in buddy["interests"].split(",")
                )
                common_interests = student_interests.intersection(buddy_interests)
                if common_interests:
                    match_score += min(20, len(common_interests) * 5)
            active_matches = conn.execute(
                "SELECT COUNT(*) FROM buddy_matches WHERE buddy_id = ? AND status = 'active'",
                (buddy_id,)
            ).fetchone()[0]
            if active_matches < 2:
                match_score += 10 - (active_matches * 5)
            
            match_score = max(0, min(100, match_score))

        return render_template(
            "buddy_details.html",
            buddy=buddy,
            full_name=session["full_name"],
            match_score=match_score,
        )
    finally:
        conn.close()

@app.route("/request-match/<int:buddy_id>", methods=["POST"])
def request_match(buddy_id):
    if "user_id" not in session or session["role"] != "student":
        flash("Unauthorized", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    try:
        existing_match = conn.execute(
            """SELECT 1 FROM buddy_matches 
            WHERE student_id = ? AND status IN ('pending', 'active')""",
            (session["user_id"],),
        ).fetchone()

        if existing_match:
            flash("You can only have one active or pending buddy request at a time", "error")
            return redirect(url_for("view_potential_matches"))

        buddy_active_matches = conn.execute(
            "SELECT COUNT(*) FROM buddy_matches WHERE buddy_id = ? AND status = 'active'",
            (buddy_id,),
        ).fetchone()[0]

        if buddy_active_matches >= 3:
            flash("This buddy has reached the maximum number of students", "info")
            return redirect(url_for("view_potential_matches"))

        student_details = conn.execute(
            "SELECT * FROM user_details WHERE user_id = ?", (session["user_id"],)
        ).fetchone()
        buddy_details = conn.execute(
            "SELECT * FROM user_details WHERE user_id = ?", (buddy_id,)
        ).fetchone()

        match_score = 0
        if student_details and buddy_details:
            if student_details["major"] and buddy_details["major"]:
                if student_details["major"] == buddy_details["major"]:
                    match_score += 30
            if student_details["languages"] and buddy_details["languages"]:
                student_langs = [
                    lang.strip().lower()
                    for lang in student_details["languages"].split(",")
                ]
                buddy_langs = [
                    lang.strip().lower() for lang in buddy_details["languages"].split(",")
                ]
                if student_langs[0] == buddy_langs[0]:
                    match_score += 15
                common_langs = set(student_langs).intersection(buddy_langs)
                if common_langs:
                    match_score += min(10, len(common_langs) * 2)
            if student_details["academic_year"] and buddy_details["academic_year"]:
                year_diff = abs(
                    student_details["academic_year"] - buddy_details["academic_year"]
                )
                if year_diff == 0:
                    match_score += 20
                elif year_diff == 1:
                    match_score += 15
                elif year_diff == 2:
                    match_score += 5
            if student_details["interests"] and buddy_details["interests"]:
                student_interests = set(
                    i.strip().lower() for i in student_details["interests"].split(",")
                )
                buddy_interests = set(
                    i.strip().lower() for i in buddy_details["interests"].split(",")
                )
                common_interests = student_interests.intersection(buddy_interests)
                if common_interests:
                    match_score += min(20, len(common_interests) * 5)
            
            if buddy_active_matches < 2:
                match_score += 10 - (buddy_active_matches * 5)
            
            match_score = max(0, min(100, match_score))

        conn.execute(
            """INSERT INTO buddy_matches 
            (buddy_id, student_id, status, match_score, created_at) 
            VALUES (?, ?, 'pending', ?, datetime('now'))""",
            (buddy_id, session["user_id"], match_score),
        )
        conn.commit()

        buddy = conn.execute(
            "SELECT full_name FROM users WHERE id = ?", (buddy_id,)
        ).fetchone()

        conn.execute(
            """INSERT INTO notifications 
            (user_id, title, message, notification_type, related_entity_type, related_entity_id) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                buddy_id,
                "New Match Request",
                f"{session['full_name']} wants to connect with you!",
                "match_request",
                "buddy_match",
                conn.execute("SELECT last_insert_rowid()").fetchone()[0],
            ),
        )

        conn.execute(
            """INSERT INTO notifications 
            (user_id, title, message, notification_type, related_entity_type, related_entity_id) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                "admin",
                "New Match Request",
                f"{session['full_name']} wants to connect with buddy {buddy['full_name']}",
                "match_request",
                "buddy_match",
                conn.execute("SELECT last_insert_rowid()").fetchone()[0],
            ),
        )

        conn.commit()

        flash(f"Match request sent to {buddy['full_name']}!", "success")
        return redirect(url_for("student_dashboard"))

    except Exception as e:
        conn.rollback()
        flash(f"Error requesting match: {str(e)}", "error")
        return redirect(url_for("view_potential_matches"))
    finally:
        conn.close()


@app.route("/approve-match/<int:match_id>", methods=["POST"])
def approve_match(match_id):
    if "user_id" not in session or session["role"] != "buddy":
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    try:
        match = conn.execute(
            "SELECT buddy_id, student_id, status FROM buddy_matches WHERE id = ?",
            (match_id,),
        ).fetchone()

        if not match:
            flash("Match not found", "error")
            return redirect(url_for("buddy_dashboard"))

        if match["status"] != "pending":
            flash("Match has already been approved or declined", "error")
            return redirect(url_for("buddy_dashboard"))

        active_matches = conn.execute(
            "SELECT COUNT(*) FROM buddy_matches WHERE buddy_id = ? AND status = 'active'",
            (match["buddy_id"],),
        ).fetchone()[0]

        if active_matches >= 3:
            flash("You already have 3 active students. Cannot accept more.", "error")
            return redirect(url_for("buddy_dashboard"))

        conn.execute(
            "UPDATE buddy_matches SET status = 'active', updated_at = datetime('now') WHERE id = ?",
            (match_id,),
        )

        conn.execute(
            "UPDATE buddy_matches SET admin_approved = 1 WHERE id = ?", (match_id,)
        )

        student = conn.execute(
            "SELECT full_name FROM users WHERE id = ?", (match["student_id"],)
        ).fetchone()

        conn.execute(
            """INSERT INTO notifications 
            (user_id, title, message, notification_type, related_entity_type, related_entity_id) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                match["student_id"],
                "Match Approved",
                f"Your match request with {session['full_name']} has been approved!",
                "match_approved",
                "buddy_match",
                match_id,
            ),
        )

        conn.commit()

        flash("Match approved successfully", "success")
        return redirect(url_for("buddy_dashboard"))

    except Exception as e:
        conn.rollback()
        flash(f"Error approving match: {str(e)}", "error")
        return redirect(url_for("buddy_dashboard"))
    finally:
        conn.close()


@app.route("/reject-match/<int:match_id>", methods=["POST"])
def reject_match(match_id):
    if "user_id" not in session or session["role"] != "buddy":
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE buddy_matches SET status = 'declined', updated_at = datetime('now') WHERE id = ?",
            (match_id,),
        )

        student = conn.execute(
            "SELECT student_id FROM buddy_matches WHERE id = ?", (match_id,)
        ).fetchone()

        conn.execute(
            """INSERT INTO notifications 
            (user_id, title, message, notification_type, related_entity_type, related_entity_id) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                student["student_id"],
                "Match Declined",
                "Your match request has been declined",
                "match_declined",
                "buddy_match",
                match_id,
            ),
        )

        conn.commit()

        flash("Match declined successfully", "success")
        return redirect(url_for("buddy_dashboard"))

    except Exception as e:
        conn.rollback()
        flash(f"Error declining match: {str(e)}", "error")
        return redirect(url_for("buddy_dashboard"))
    finally:
        conn.close()


@app.route("/admin/approve-match/<int:match_id>", methods=["POST"])
def admin_approve_match(match_id):
    print("Session:", dict(session))  # DEBUG HERE

    if "user_id" not in session or not session.get("is_admin"):
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    try:
        print(
            f"Attempting to approve match with ID: {match_id}"
        )  # Debugging the match ID

        conn.execute(
            "UPDATE buddy_matches SET admin_approved = 1, updated_at = datetime('now') WHERE id = ?",
            (match_id,),
        )
        conn.commit()

        print(
            f"Successfully approved match with ID: {match_id}"
        )  # Success message in debug

        flash("Match approved by admin successfully", "success")
        return redirect(url_for("admin_dashboard"))

    except Exception as e:
        conn.rollback()
        print(f"Error occurred while approving match: {str(e)}")  # Debugging the error
        flash(f"Error approving match as admin: {str(e)}", "error")
        return redirect(url_for("admin_dashboard"))

    finally:
        conn.close()


@app.route("/messages/<int:match_id>", methods=["GET", "POST"])
def chat(match_id):
    conn = get_db_connection()
    match = conn.execute(
        "SELECT * FROM buddy_matches WHERE id = ?", (match_id,)
    ).fetchone()

    if not match or match["status"] != "active":
        flash("You can only message active matches.", "error")
        return redirect(url_for("buddy_dashboard"))

    if request.method == "POST":
        content = request.form["content"]
        sender_id = session["user_id"]
        receiver_id = (
            match["student_id"] if sender_id == match["buddy_id"] else match["buddy_id"]
        )

        conn.execute(
            "INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
            (sender_id, receiver_id, content),
        )
        conn.commit()
        flash("Message sent!", "success")

    sender_id = session["user_id"]
    receiver_id = (
        match["student_id"] if sender_id == match["buddy_id"] else match["buddy_id"]
    )
    messages = conn.execute(
        """
        SELECT * FROM messages
        WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
        ORDER BY sent_at
    """,
        (sender_id, receiver_id, receiver_id, sender_id),
    ).fetchall()

    conn.close()
    return render_template("chat.html", match=match, messages=messages)


messages = {}


@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()

    if not all(key in data for key in ["sender_id", "receiver_id", "content"]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = {
        "sender_id": data["sender_id"],
        "content": data["content"],
        "timestamp": datetime.now().isoformat(),
    }

    chat_key = tuple(sorted([data["sender_id"], data["receiver_id"]]))

    if chat_key not in messages:
        messages[chat_key] = []

    messages[chat_key].append(message)

    return jsonify({"status": "success", "message": "Message sent"})


@app.route("/get_messages", methods=["GET"])
def get_messages():
    user_id = request.args.get("user_id")
    other_id = request.args.get("buddy_id") or request.args.get("student_id")

    if not user_id or not other_id:
        return (
            jsonify({"status": "error", "message": "Missing user or chat partner ID"}),
            400,
        )

    chat_key = tuple(sorted([user_id, other_id]))

    if chat_key not in messages:
        return jsonify({"messages": []})

    conversation_messages = messages[chat_key]

    return jsonify({"messages": conversation_messages, "status": "success"})


if __name__ == "__main__":
    if not os.path.exists("buddy_system.db"):
        initialize_db()
    app.run(debug=True)
