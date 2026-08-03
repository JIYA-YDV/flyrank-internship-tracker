# 🗄️ Task Management API — SQLite Persistence

**Week 3 · Assignment A2 (BE-02)**  
**FlyRank AI — Backend Engineering Track**  
**Phase:** Foundations | **Workload:** 4h

---

## 📌 What This Project Does

A RESTful CRUD API for managing tasks, built with **FastAPI** and backed by a **SQLite database**.

This is a direct continuation of the Week 2 in-memory API. The API endpoints are **completely identical** — only the storage layer changed. Tasks now survive server restarts because they are stored in a real database file instead of a Python list in memory.

### The Core Idea

```
Before (Week 2):   Client → API → Python List (lost on restart)
After  (Week 3):   Client → API → SQLite Database (persists forever)
```

The client never notices the difference. The same URLs, the same request bodies, the same responses. Only the implementation changed.

---

## 🛠️ Why SQLite?

| Reason | Explanation |
|:-------|:------------|
| **Zero installation** | No separate database server to install or configure |
| **Single file** | The entire database lives in one file called `tasks.db` |
| **Built into Python** | The `sqlite3` module comes with Python — no extra packages needed |
| **Standard SQL** | Skills transfer directly to PostgreSQL, MySQL, and other databases |
| **Easy to inspect** | You can open `tasks.db` in DB Browser for SQLite and see the data visually |

SQLite is the right choice for learning, prototyping, and small applications. When the project grows, switching to PostgreSQL requires changing only the database connection — the SQL queries and API stay the same.

---

## 📁 Where the Database File Is Stored

```text
task-api-db/
├── database.py       ← Connection, table creation, seeding logic
├── models.py         ← Pydantic request and response schemas
├── crud.py           ← All SQL query functions
├── routes.py         ← FastAPI endpoint definitions
├── main.py           ← Application entry point
├── requirements.txt  ← Python dependencies
├── tasks.db          ← SQLite database file (auto-created on first run)
├── screenshot.png    ← DB Browser screenshot
└── README.md
```

The `tasks.db` file is created **automatically** the first time you start the server.  
You do not need to create it manually.

> ⚠️ `tasks.db` is listed in `.gitignore` and is not committed to the repository.  
> Every person who clones this project gets a fresh database on first run.

---

## 🚀 How to Start the Project

### Prerequisites

- Python 3.10 or higher
- pip

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-username/task-api-db.git
cd task-api-db
```

### Step 2 — Create and activate a virtual environment

```bash
python -m venv venv

# Windows PowerShell
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Start the server

```bash
uvicorn main:app --reload --port 8000
```

### Step 5 — Confirm it works

Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

You will see the interactive Swagger UI where you can test every endpoint.

On first startup you will see:

```text
🚀 Starting Task API...
✅ Table 'tasks' is ready.
🌱 Seeded 3 example tasks.
INFO:     Application startup complete.
```

On every restart after that:

```text
🚀 Starting Task API...
✅ Table 'tasks' is ready.
📦 Database already has 3 task(s). Skipping seed.
INFO:     Application startup complete.
```

---

## 📮 API Endpoints

### Base URL
```
http://localhost:8000
```

### Endpoint Reference

| Method | Endpoint | Description | Success | Error |
|:-------|:---------|:------------|:--------|:------|
| `GET` | `/tasks` | List all tasks | 200 | — |
| `GET` | `/tasks/{id}` | Get one task by ID | 200 | 404 |
| `POST` | `/tasks` | Create a new task | 201 | 400 |
| `PUT` | `/tasks/{id}` | Update title and/or status | 200 | 404 |
| `DELETE` | `/tasks/{id}` | Delete a task | 200 | 404 |
| `GET` | `/stats` | Task count statistics | 200 | — |

### Optional Query Parameters for `GET /tasks`

| Parameter | Type | Example | Description |
|:----------|:-----|:--------|:------------|
| `search` | string | `?search=sql` | Filter tasks whose title contains keyword |
| `done` | boolean | `?done=false` | Filter by completion status |
| `sort_alpha` | boolean | `?sort_alpha=true` | Sort results alphabetically by title |

---

## 📋 Request & Response Examples

### GET /tasks
```json
[
  { "id": 1, "title": "Learn SQL fundamentals", "done": false, "created_at": "2026-08-03 20:16:59", "updated_at": "2026-08-03 20:16:59" },
  { "id": 2, "title": "Connect SQLite to FastAPI", "done": true,  "created_at": "2026-08-03 20:16:59", "updated_at": "2026-08-03 20:16:59" },
  { "id": 3, "title": "Build an AI feature with Claude", "done": false, "created_at": "2026-08-03 20:16:59", "updated_at": "2026-08-03 20:16:59" }
]
```

### POST /tasks — Request Body
```json
{ "title": "Write unit tests", "done": false }
```

### POST /tasks — 201 Response
```json
{ "id": 4, "title": "Write unit tests", "done": false, "created_at": "2026-08-03 20:25:00", "updated_at": "2026-08-03 20:25:00" }
```

### POST /tasks — 400 Error (missing title)
```json
{ "detail": "Title is required" }
```

### GET /tasks/999 — 404 Error
```json
{ "detail": "Task not found" }
```

### GET /stats
```json
{ "total_tasks": 4, "completed_tasks": 1, "pending_tasks": 3 }
```

---

## 🗃️ Database Schema

```sql
CREATE TABLE tasks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT    NOT NULL,
    done       INTEGER NOT NULL DEFAULT 0,
    created_at TEXT    DEFAULT (datetime('now')),
    updated_at TEXT    DEFAULT (datetime('now'))
);
```

| Column | Type | Description |
|:-------|:-----|:------------|
| `id` | INTEGER | Auto-incrementing primary key |
| `title` | TEXT | Task description, cannot be empty |
| `done` | INTEGER | 0 = pending, 1 = completed |
| `created_at` | TEXT | Set once when task is created |
| `updated_at` | TEXT | Updated every time task is modified |

> SQLite does not have a native boolean type.  
> It stores `done` as `0` (false) or `1` (true).  
> FastAPI and Pydantic convert these automatically to JSON `true`/`false`.

---

## 🔍 SQL Queries Explored in Stage 4

These queries were run manually inside **DB Browser for SQLite**:

```sql
-- List every task in the table
SELECT * FROM tasks;

-- Show only completed tasks
SELECT * FROM tasks WHERE done = 1;

-- Count all tasks
SELECT COUNT(*) FROM tasks;

-- Mark every task as completed
UPDATE tasks SET done = 1;

-- Delete all completed tasks
DELETE FROM tasks WHERE done = 1;

-- Search for tasks containing a keyword
SELECT * FROM tasks WHERE title LIKE '%sql%';

-- Sort tasks alphabetically
SELECT * FROM tasks ORDER BY title ASC;

-- Count pending vs completed in one query
SELECT
    SUM(CASE WHEN done = 0 THEN 1 ELSE 0 END) AS pending,
    SUM(CASE WHEN done = 1 THEN 1 ELSE 0 END) AS completed
FROM tasks;
```

After running each query, visiting `GET /tasks` in the browser confirmed the API immediately reflected the manual database changes.

---

## 🖼️ Database Screenshot

The screenshot below shows `tasks.db` open in **DB Browser for SQLite**, displaying the Browse Data tab with the tasks table and all columns visible.

![DB Browser for SQLite — tasks table](./screenshot.png)

---

## ✅ Requirements Checklist

- [x] API exposes the same CRUD endpoints as Assignment 1
- [x] Tasks are stored in SQLite instead of memory
- [x] Data survives server restarts
- [x] Database is automatically created if missing
- [x] Tasks table is automatically created if missing
- [x] Three example tasks are inserted only on the first run
- [x] All CRUD operations use SQL queries
- [x] Unknown ids return 404
- [x] Invalid requests return 400
- [x] Public GitHub repository updated with README and database screenshot

### Optional Extras Completed

- [x] Search with `?search=` using SQL `LIKE`
- [x] Filter with `?done=` using SQL `WHERE`
- [x] Sort alphabetically with `?sort_alpha=`
- [x] Statistics endpoint `GET /stats` using SQL `COUNT()`
- [x] Timestamps `created_at` and `updated_at` on every task

---

## 💡 Key Lesson From This Assignment

> **APIs describe what your application does.**  
> **Databases describe where your application stores its data.**

The separation between these two layers is one of the most important ideas in backend engineering.

By the end of this assignment, every endpoint URL, request body, and response format stayed **exactly the same** as Week 2. Only the storage implementation changed.

This means that in the future, switching from SQLite to PostgreSQL or MySQL requires changing only the database connection and queries — the API layer stays untouched.

---

## 📦 Dependencies

```text
fastapi==0.111.0
uvicorn==0.29.0
pydantic==2.7.1
```

The `sqlite3` module is built into Python and requires no installation.
