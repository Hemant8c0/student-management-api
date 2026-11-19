# Student Management API

A REST API built with **FastAPI**, **SQLAlchemy 2** and **SQLite**. It implements complete CRUD operations for student records.

## Features

- SQLite database; `students` table is created automatically when the app starts.
- Create, list, get-one, update and delete student records.
- Validation for name, email, age and course.
- Duplicate email protection.
- Interactive Swagger documentation at `/docs`.

## 1. Setup

Use Python 3.10 or newer.

```bash
# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Run the API

```bash
uvicorn main:app --reload
```

Open:
- API home: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs

The `students.db` SQLite file and `students` table are created automatically.

## 3. Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students/` | Create a student |
| GET | `/students/` | Get all students |
| GET | `/students/{student_id}` | Get one student |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |

## 4. Sample requests

### Create a student

```bash
curl -X POST "http://127.0.0.1:8000/students/" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Aman Sharma\",\"email\":\"aman@example.com\",\"age\":21,\"course\":\"Computer Science\"}"
```

Example response (`201 Created`):

```json
{
  "id": 1,
  "name": "Aman Sharma",
  "email": "aman@example.com",
  "age": 21,
  "course": "Computer Science"
}
```

### Read all students

```bash
curl "http://127.0.0.1:8000/students/"
```

### Read one student

```bash
curl "http://127.0.0.1:8000/students/1"
```

### Update a student

```bash
curl -X PUT "http://127.0.0.1:8000/students/1" ^
  -H "Content-Type: application/json" ^
  -d "{\"age\":22,\"course\":\"Data Science\"}"
```

### Delete a student

```bash
curl -X DELETE "http://127.0.0.1:8000/students/1"
```

> In Windows PowerShell, you can also use Swagger UI (`/docs`) to send each request. Click an endpoint, select **Try it out**, enter the JSON body or ID, and click **Execute**.

## 5. Validation examples

- Name and course must contain at least 2 characters.
- Email must be a valid email address.
- Age must be between 16 and 100.
- Email must be unique.
- An unknown student ID returns `404 Not Found`.
- Invalid request data returns `422 Unprocessable Entity`.

Example invalid body:

```json
{
  "name": "A",
  "email": "not-an-email",
  "age": 12,
  "course": "C"
}
```

## 6. Push to GitHub

Create a new empty repository on GitHub named `student-management-api`. Do not add a README on GitHub (this project already contains one). Then run these commands in this project folder:

```bash
git init
git add .
git commit -m "Build Student Management CRUD API with FastAPI and SQLite"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/student-management-api.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Your submission URL will be:

`https://github.com/YOUR-USERNAME/student-management-api`

## Submission checklist

- [ ] API starts successfully.
- [ ] Create, read, update and delete work from `/docs`.
- [ ] `students.db` is generated after startup.
- [ ] GitHub repository contains `main.py`, `requirements.txt`, `.gitignore` and `README.md`.
- [ ] README includes endpoint list, validation rules and sample requests.
