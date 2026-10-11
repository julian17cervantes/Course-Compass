# Course Compass


A REST API for tracking college courses and calculating GPA, built with FastAPI and PostgreSQL.

**Live demo:** https://your-app.up.railway.app/docs

## Features

- Full CRUD for courses (create, list, fetch, update, delete)
- Unit-weighted GPA calculation, cumulative and per semester
- Automated tests run on every push and pull request with GitHub Actions
- JWT authentication with bcrypt password hashing, and per-user data isolation
- Goal GPA planner that calculates the average grade needed on upcoming courses

## Tech stack

Python, FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Pytest, GitHub Actions

## Getting started

```bash
git clone https://github.com/julian17cervantes/Course-Compass.git
cd YOUR_REPO
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
createdb course_compass
echo "DATABASE_URL=postgresql+psycopg2://localhost/course_compass" > .env
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/docs for the interactive API docs.

## Run with Docker

```bash
docker compose up --build
```

Then open http://127.0.0.1:8000/docs.

## Running tests

```bash
pytest
```

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST | /signup | Create an account |
| POST | /login | Log in and receive a JWT |
| POST | /courses | Create a course |
| GET | /courses | List your courses |
| GET | /courses/{id} | Get one course |
| PUT | /courses/{id} | Update a course |
| DELETE | /courses/{id} | Delete a course |
| GET | /gpa | Cumulative and per-semester GPA |
| PUT | /goal | Set your goal GPA |
| GET | /goal | See the grades you need on upcoming courses |