# Task API

A CRUD REST API for managing to-do tasks, built with FastAPI (Python).  
Built as Week 2 Assignment A1 of the FlyRank AI Fluency Internship.

## Run locally (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## Endpoints

| Method | Path | Description | Status codes |
|--------|------|-------------|--------------|
| GET | `/` | API info | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{id}` | Get one task | 200, 404 |
| POST | `/tasks` | Create a task | 201, 422 |
| PUT | `/tasks/{id}` | Update a task | 200, 400, 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204, 404 |
| GET | `/stats` | Task statistics | 200 |
| POST | `/reset` | Reset to seed data | 200 |

## Testing with curl.exe on Windows

PowerShell corrupts JSON quoting when passed inline to `curl.exe`. The reliable pattern is to write the JSON body to a file first, then pass it with `-d "@file.json"`.

```powershell
# Create the body file
[System.IO.File]::WriteAllText("$PWD\create.json", '{"title":"Buy milk"}')

# Send the request
curl.exe -i -X POST http://localhost:8000/tasks `
  -H "Content-Type: application/json" `
  -d "@create.json"
```

Example response:

```
HTTP/1.1 201 Created
date: Sat, 18 Jul 2026 17:50:46 GMT
server: uvicorn
content-length: 43
content-type: application/json

{"id":4,"title":"Final check","done":false}
```

## Data model

```json
{
  "id": 1,
  "title": "Buy groceries",
  "done": false
}
```

Tasks are stored in memory only. Restarting the server resets all tasks to the three seed tasks. This is intentional for Week 2 — persistence via a database is added in Week 3.

## Swagger UI

![Swagger UI](swagger-screenshot.png)

## Mortality experiment

After creating several tasks and restarting the server, all created tasks disappeared — only the three seed tasks remained. Python lists live in RAM: when the process exits, that memory is freed. A database writes state to disk so it survives restarts — which is the entire reason Week 3 introduces one.

## AI vs Me

*(Filled in during Stage 7 bonus)*