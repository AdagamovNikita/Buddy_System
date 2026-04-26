# Buddy System

Buddy System is a web-based platform designed to facilitate mentoring and peer support within educational institutions. The application connects junior students with experienced peers (buddies) to support their academic and social integration.

## My Role: System Analyst & Architect

In this project, I served primarily as the System Analyst and Core Architect. My key responsibilities and contributions included:

* Technology Stack Selection: Evaluated and selected the appropriate frameworks and libraries to ensure rapid development, maintainability, and scalability.
* Architectural Design: Engineered a monolithic backend architecture utilizing Flask, ensuring clear separation of concerns between routing, business logic, and data access layers.
* Database Architecture: Designed the complete relational database schema from scratch. I mapped out entity-relationship models for users, complex role management, student profiles, matching preferences, dynamic scheduling, and messaging. 
* Implementation: Actively participated in the backend implementation, particularly focusing on translating the designed database schema into functional SQLite structures and developing the core pairing algorithm.

## Technology Stack

* Backend: Python 3, Flask
* Database: SQLite (Raw SQL with sqlite3.Row for optimized data retrieval)
* Frontend: HTML5, CSS3, Jinja2 Templates
* Forms & Validation: WTForms, Flask-WTF
* Security & Authentication: JWT (JSON Web Tokens), Flask-Session, secure password hashing
* External Integrations: Zoom API (OAuth-based meeting generation)

## Core Architecture

The system is built on a monolithic Flask architecture:
* app.py: The core application file managing routing, business logic controllers, database interactions, and Zoom API token management.
* config.py: Centralized environment variable management.
* forms.py: Declarative form definitions and validation logic.
* templates/ & static/: Server-side rendered views and static assets.
* Database Layer: Auto-initialized SQLite database (buddy_system.db) designed to handle user relations, session tracking, and matching states without the overhead of an ORM.

## System Capabilities

### Role-Based Access Control
The application supports three distinct user scopes:
* Administrator: Manages the platform, approves buddy applications, monitors matches, and oversees the user base.
* Buddy (Mentor): Subject to admin approval. Can accept student requests, manage sessions, and communicate with mentees.
* Student (Mentee): Can configure matching preferences, browse potential mentors, schedule meetings, and participate in events.

### Advanced Matching Algorithm
A core feature of the system is the custom matching algorithm I designed. It pairs students and buddies based on a 100-point scoring system considering:
* Major and academic specialization (+30 points)
* Native and secondary language overlap (up to +25 points)
* Academic year difference (prioritizing reasonable seniority gaps)
* Shared interests and hobbies
* Mentor workload balancing (reducing visibility for overloaded buddies)

### Integrated Scheduling and Zoom API
The system provides built-in calendar functionality. I integrated the Zoom API via OAuth to automatically generate meeting links when a student and a buddy schedule a session, completely abstracting the manual meeting creation process.

## Local Setup Instructions

1. Clone the repository
git clone https://github.com/AdagamovNikita/Buddy_System.git
cd BuddySystem

2. Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install dependencies
pip install Flask requests PyJWT python-dotenv Flask-WTF WTForms

4. Configure environment variables
Create a .env file in the root directory and define the following variables:
FLASK_SECRET_KEY=your_secret_key
ZOOM_API_KEY=your_zoom_client_id
ZOOM_API_SECRET=your_zoom_client_secret

5. Run the application
python app.py

The application will start at http://127.0.0.1:5000. The database (buddy_system.db) is automatically initialized on the first run.

Default Administrator Credentials:
Email: admin@aubmed.ac.cy
Password: Admin