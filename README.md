# Course Compass

![Tests](https://github.com/julian17cervantes/Course-Compass/actions/workflows/tests.yml/badge.svg)

A REST API for tracking college courses and calculating GPA, built with FastAPI and PostgreSQL.

## Features

- Full CRUD for courses (create, list, fetch, update, delete)
- Unit-weighted GPA calculation, cumulative and per semester
- Automated tests run on every push and pull request with GitHub Actions

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

## Running tests

```bash
pytest
```

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST | /courses | Create a course |
| GET | /courses | List all courses |
| GET | /courses/{id} | Get one course |
| PUT | /courses/{id} | Update a course |
| DELETE | /courses/{id} | Delete a course |
| GET | /gpa | Cumulative and per-semester GPA |