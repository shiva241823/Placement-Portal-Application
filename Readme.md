# Placement Portal Application (PPA V2)

A full-stack web application built to manage campus recruitment activities efficiently.

The system supports three roles:
- Admin (Institute Placement Cell)
- Company
- Student


# TECH STACK


Backend:
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- SQLite
- Redis
- Celery

Frontend:
- Vue 3
- Vue Router 4
- Axios
- Bootstrap 5
- Vite


# PROJECT STRUCTURE


PPA/
│
├── backend/
│   ├── app/
│   ├── run.py
│   ├── celery_worker.py
│   ├── requirements.txt
│   └── instance/
│
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── README.md


# STEP 1: CLONE THE PROJECT

git clone <your-repository-url>
cd PPA


# BACKEND SETUP (FLASK)


Step 1: Navigate to backend

cd backend

Step 2: Create Virtual Environment

Windows:
python -m venv venv
.\venv\Scripts\Activate.ps1

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

If requirements.txt is missing:

pip install flask flask_sqlalchemy flask_jwt_extended flask_migrate redis celery

Step 4: Run Flask Server

python run.py

Backend runs at:
http://127.0.0.1:5000



# REDIS SETUP (Required for Caching & Celery)

cd "C:\Users\DELL\OneDrive\Documents\redis"
.\redis-server.exe redis.windows.conf

Windows:
Use Redis Desktop or WSL

Mac:
brew install redis
brew services start redis

Linux:
sudo apt install redis-server
sudo systemctl start redis

Verify Redis is running:
in a seprate terminal
cd "C:\Users\DELL\OneDrive\Documents\redis"
.\redis-cli.exe ping

Expected Output:
PONG



# CELERY SETUP (IMPORTANT: USING --pool=solo)


Open a NEW terminal.

Navigate to backend:

cd backend
venv\Scripts\activate

Start Celery Worker (MANDATORY pool=solo):

celery -A celery_worker.celery worker --loglevel=info --pool=solo

If using scheduled jobs (daily reminders / monthly reports):

celery -A celery_worker.celery beat --loglevel=info



# FRONTEND SETUP (VUE + VITE)

Open a NEW terminal.

cd frontend

Install dependencies:

npm install

Ensure correct Vue Router version:

npm uninstall vue-router
npm install vue-router@4

Install Bootstrap (if not installed):

npm install bootstrap

Start frontend:

npm run dev

Frontend runs at:
http://localhost:5173



# RUNNING COMPLETE SYSTEM (5 TERMINALS REQUIRED)


You need FIVE terminals running simultaneously:

------------------------------------------------------------
Terminal 1 – Flask Backend
------------------------------------------------------------

cd backend
venv\Scripts\activate
python run.py

------------------------------------------------------------
Terminal 2 – Redis Server
------------------------------------------------------------

redis-server

(Or start Redis service depending on OS)

------------------------------------------------------------
Terminal 3 – Celery Worker (pool=solo)
------------------------------------------------------------

cd backend
venv\Scripts\activate
celery -A celery_worker.celery worker --loglevel=info --pool=solo

------------------------------------------------------------
Terminal 4 – Celery Beat (Scheduled Jobs)
------------------------------------------------------------

cd backend
venv\Scripts\activate
celery -A celery_worker.celery beat --loglevel=info

------------------------------------------------------------
Terminal 5 – Vue Frontend
------------------------------------------------------------

cd frontend
npm run dev


1. 401 Unauthorized
- Clear browser localStorage
- Login again
- Ensure JWT token is stored

2. Navbar Missing
- Ensure App.vue renders Navbar conditionally for correct routes

3. Styling Broken
- Install Bootstrap:
  npm install bootstrap
- Import in main.js:
  import "bootstrap/dist/css/bootstrap.min.css"
  import "bootstrap/dist/js/bootstrap.bundle.min.js"
