# Buddy System: Academic Mentorship Platform

**Buddy System** is a web-based platform designed to connect junior students with experienced mentors. The application helps students integrate into university life through a smart pairing system and built-in communication tools.

---

## My Role: System Analyst & Database Designer

In this project, I focused on the technical planning and the data architecture. My goal was to transform university requirements into a solid technical structure, focusing on how the data should be organized and how the system should function.

* **Technology Stack Selection:** I evaluated and selected the project tools (Flask, SQLite, and JWT). I chose this stack to balance fast development with security and reliability.
* **Database Design & Implementation:** I designed the entire relational database from the ground up. This included all three professional phases: **Conceptual, Logical, and Physical design**. I mapped out entities for users, roles, student profiles, and scheduling. I also personally implemented the database layer using raw SQL to ensure high performance.
* **System Planning:** I defined the overall structure of the platform. I ensured a "separation of concerns" so that the business logic, database interactions, and user interface remained organized and easy to manage.

---

## Key Features

### 1. Role-Based Access Control (RBAC)
The system uses three distinct permission levels to manage access and security:
* **Administrator:** Manages the platform, approves mentor applications, and monitors matches.
* **Buddy (Mentor):** Manages student requests, hosts sessions, and tracks mentee progress.
* **Student (Mentee):** Browses for mentors based on preferences and schedules meetings.

### 2. Automated Zoom Integration
To simplify online meetings, I integrated the **Zoom API (OAuth 2.0)**. The system automatically creates a unique meeting link whenever a student and mentor schedule a session, removing the need for manual setup.

### 3. Smart Matching Logic
The platform uses a scoring system to pair students with the best possible mentors based on:
* **Major & Specialization:** Matching users within the same academic field.
* **Language:** Finding mentors who speak the same native or secondary languages.
* **Seniority:** Prioritizing experienced students as mentors for newcomers.
* **Interests:** Connecting students with shared hobbies and extracurriculars.

---

## Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python 3, Flask |
| **Database** | SQLite (Raw SQL with `sqlite3.Row` for efficiency) |
| **Frontend** | HTML5, CSS3, Jinja2 Templates |
| **Security** | JWT (JSON Web Tokens), Flask-Session, Secure Password Hashing |
| **Integrations** | Zoom API (OAuth 2.0) |
| **Forms** | WTForms / Flask-WTF |

---

## Project Structure

```text
├── app.py              # Core application logic and routing
├── config.py           # Environment and security settings
├── forms.py            # Data validation and form definitions
├── buddy_system.db     # Optimized SQLite database
├── static/             # CSS, JavaScript, and images
└── templates/          # Jinja2 HTML templates
```

---

## Local Setup Instructions

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/AdagamovNikita/Buddy_System.git
    cd BuddySystem
    ```

2.  **Initialize Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install Flask requests PyJWT python-dotenv Flask-WTF WTForms
    ```

4.  **Configure Environment**
    Create a `.env` file in the root folder:
    ```env
    FLASK_SECRET_KEY=your_secret_key
    ZOOM_API_KEY=your_zoom_client_id
    ZOOM_API_SECRET=your_zoom_client_secret
    ```

5.  **Run the Application**
    ```bash
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

**Default Admin Credentials:**
* **Email:** `admin@aubmed.ac.cy`
* **Password:** `Admin`
