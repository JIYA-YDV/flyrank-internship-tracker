\# FlyRank Auth API — A4: Auth · Login \& Protect



A secure REST API built with \*\*Python + FastAPI\*\* and \*\*Supabase Auth\*\*.

Handles user sign-up, login, logout, and JWT-protected routes — guarded by

a reusable auth dependency. Built as Week 4 of the FlyRank Backend Internship.



\---



\## What it demonstrates



| Feature | Implementation |

|---------|---------------|

| Identity Provider | Supabase Auth — no DIY password hashing ever |

| JWT verification | `supabase.auth.get\_user(token)` — real network call to Supabase |

| Reusable auth guard | `require\_auth` FastAPI dependency via `Depends()` |

| Swagger UI | Built-in FastAPI at `/docs` with 🔒 padlock on protected routes |

| Correct status codes | 201 · 200 · 204 · 400 · 401 · 403 · 422 |

| Middleware reuse | Same `Depends(require\_auth)` on every protected route — zero copy-paste |



\---



\## Quick Start



\### 1. Clone the repo



```bash

git clone https://github.com/YOUR-USERNAME/flyrank-auth-api.git

cd flyrank-auth-api

```



\### 2. Create virtual environment



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```powershell

pip install -r requirements.txt

```



\### 4. Set up environment variables



```powershell

Copy-Item ".env.example" ".env"

notepad .env

```



Fill in your real Supabase values:



```env

SUPABASE\_URL=https://your-project-ref.supabase.co

SUPABASE\_KEY=your-anon-public-key-here

```



\*\*Where to find these:\*\*

1\. Go to \[supabase.com](https://supabase.com) → your project

2\. \*\*Settings → API\*\*

3\. Copy \*\*Project URL\*\* and \*\*anon / public\*\* key

4\. ⚠️ Never use the `service\_role` key — it bypasses all security



\*\*One-time Supabase setting for local testing:\*\*

```

Authentication → Providers → Email → disable "Confirm email" → Save

```



\### 5. Run the server



```powershell

uvicorn app.main:app --reload --port 8000

```



```

✅  Supabase client initialized successfully

INFO:     Uvicorn running on http://127.0.0.1:8000

INFO:     Application startup complete.

```



\- \*\*API root:\*\* http://localhost:8000

\- \*\*Swagger UI:\*\* http://localhost:8000/docs

\- \*\*ReDoc:\*\* http://localhost:8000/redoc



\---



\## API Reference



| Method | Endpoint | Auth Required | Description | Success Code |

|--------|----------|:---:|-------------|:---:|

| `GET` | `/` | ❌ | Health check | 200 |

| `GET` | `/public/info` | ❌ | Public info — open to everyone | 200 |

| `POST` | `/auth/signup` | ❌ | Register a new account | 201 |

| `POST` | `/auth/login` | ❌ | Authenticate and get a JWT | 200 |

| `POST` | `/auth/logout` | ✅ Bearer | End the session | 204 |

| `POST` | `/auth/refresh` | ❌ | Exchange refresh token for new access token | 200 |

| `GET` | `/protected/profile` | ✅ Bearer | Read your private profile | 200 |

| `GET` | `/protected/dashboard` | ✅ Bearer | Read your private dashboard | 200 |

| `GET` | `/protected/admin` | ✅ Bearer + admin role | Admin-only route (demonstrates 403) | 200 |



\---



\## Status Codes



| Code | Meaning | When it appears |

|------|---------|----------------|

| `200` | OK | Successful read, login, or refresh |

| `201` | Created | Successful signup |

| `204` | No Content | Successful logout — nothing to return |

| `400` | Bad Request | Missing fields or invalid input |

| `401` | Unauthorized | Missing, malformed, or expired token |

| `403` | Forbidden | Valid token but insufficient role/permission |

| `422` | Unprocessable Entity | Wrong data types sent in request body |



\### 401 vs 403 — the important difference



```

401 Unauthorized = "I don't know WHO you are"

&#x20;                  → No token, bad token, expired token

&#x20;                  → Fix: log in and get a fresh token



403 Forbidden    = "I know EXACTLY who you are — and still no"

&#x20;                  → Valid token, wrong role/permission

&#x20;                  → Fix: you need different privileges

```



\---



\## Auth Flow



```

Client              FastAPI Server            Supabase

&#x20; │                       │                      │

&#x20; │── POST /auth/signup ──►│── sign\_up() ────────►│

&#x20; │                        │   (Supabase hashes   │

&#x20; │◄── 201 user ───────────│    password, stores) │

&#x20; │                        │                      │

&#x20; │── POST /auth/login ───►│── sign\_in\_with\_  ───►│

&#x20; │                        │   password()         │

&#x20; │◄── 200 access\_token ───│◄── session + JWT ────│

&#x20; │                        │                      │

&#x20; │── GET /protected/   ──►│                      │

&#x20; │   profile              │── get\_user(token) ──►│

&#x20; │   Authorization:       │   (verify signature  │

&#x20; │   Bearer <JWT>         │    + expiry)         │

&#x20; │                        │◄── verified user ────│

&#x20; │◄── 200 profile ────────│                      │

&#x20; │                        │                      │

&#x20; │── POST /auth/logout ──►│── sign\_out() ───────►│

&#x20; │◄── 204 no content ─────│                      │

```



\---



\## Security Decisions



| Decision | Reason |

|----------|--------|

| Never store or hash passwords | Supabase handles bcrypt — rolling your own crypto ends careers |

| Use `anon` key only, never `service\_role` | `service\_role` bypasses Row Level Security entirely |

| `get\_user(token)` makes a real network call | Local JWT parsing cannot detect revoked sessions |

| Single `require\_auth` dependency | One bug fix protects ALL routes — no copy-paste risk |

| Generic error messages on 401 | Never reveal which field was wrong — prevents user enumeration attacks |

| `try/except` around all Supabase calls | SDK throws exceptions in newer versions instead of returning None |



\---



\## Testing with PowerShell



```powershell

\# 1. Sign up

Invoke-RestMethod -Uri "http://localhost:8000/auth/signup" `

&#x20; -Method POST -ContentType "application/json" `

&#x20; -Body '{"email":"test@example.com","password":"password123"}'



\# 2. Login + capture token

$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `

&#x20; -Method POST -ContentType "application/json" `

&#x20; -Body '{"email":"test@example.com","password":"password123"}'

$TOKEN = $response.access\_token



\# 3. Access protected profile

Invoke-RestMethod -Uri "http://localhost:8000/protected/profile" `

&#x20; -Method GET -Headers @{ Authorization = "Bearer $TOKEN" }



\# 4. Tampered token → 401

try {

&#x20; Invoke-RestMethod -Uri "http://localhost:8000/protected/profile" `

&#x20;   -Method GET -Headers @{ Authorization = "Bearer ${TOKEN}TAMPERED" }

} catch { Write-Host "Correctly rejected with 401" }



\# 5. Logout

Invoke-RestMethod -Uri "http://localhost:8000/auth/logout" `

&#x20; -Method POST -Headers @{ Authorization = "Bearer $TOKEN" }

```



\---



\## Testing with Swagger UI



```

1\. Open http://localhost:8000/docs

2\. Find POST /auth/login → click Try it out → fill email + password → Execute

3\. Copy the access\_token from the response body

4\. Click the Authorize 🔒 button (top right of the page)

5\. Paste your token → click Authorize → Close

6\. Now click GET /protected/profile → Try it out → Execute

7\. You should see 200 with your user data

```



\---



\## Project Structure



```

flyrank-auth-api/

├── app/

│   ├── \_\_init\_\_.py

│   ├── main.py                  # FastAPI app, routers, Swagger config

│   ├── config.py                # Supabase client — reads .env, fails fast

│   ├── middleware/

│   │   ├── \_\_init\_\_.py

│   │   └── auth.py              # require\_auth — the reusable JWT guard

│   └── routes/

│       ├── \_\_init\_\_.py

│       ├── auth.py              # POST /auth/signup login logout refresh

│       ├── protected.py         # GET /protected/profile dashboard admin

│       └── public.py            # GET /public/info

├── .env                         # ← git-ignored, YOUR real secrets

├── .env.example                 # ← committed, placeholder values only

├── .gitignore                   # excludes .env, venv, \_\_pycache\_\_

├── requirements.txt             # fastapi uvicorn supabase python-dotenv

└── README.md                    # this file

```



\---



\## Dependencies



```txt

fastapi==0.111.0

uvicorn\[standard]==0.29.0

supabase==2.5.0

python-dotenv==1.0.1

pydantic==2.7.1

```



Install all:

```powershell

pip install -r requirements.txt

```



\---



\## Glossary



| Term | What it means in this project |

|------|-------------------------------|

| \*\*JWT\*\* | JSON Web Token — a signed string proving who you are. The `access\_token` you get from `/login` |

| \*\*Bearer token\*\* | How the JWT travels: `Authorization: Bearer eyJ...` in the request header |

| \*\*Identity Provider\*\* | Supabase — manages accounts, hashes passwords, signs tokens so we don't have to |

| \*\*Middleware / Dependency\*\* | `require\_auth` — runs before the route handler, verifies the token, or returns 401 |

| \*\*401 vs 403\*\* | 401 = "who are you?" · 403 = "I know you, and no" |

| \*\*Refresh token\*\* | Long-lived token to get a new access token without re-logging in |

| \*\*anon key\*\* | Supabase public key — safe to use in your app. Never use `service\_role` |



\---



\## Commit History



```

Stage 0: initialize FastAPI project structure and folder layout

Stage 0: add Supabase client config with env validation and fail-fast

Stage 1: add signup and login routes with Supabase Auth and input validation

Stage 2: add public info route and protected stub returning 401 without token

Stage 3: verify JWT via supabase.auth.get\_user() with real network validation

Stage 3: update protected routes to use verified user data from middleware

Stage 4: confirm require\_auth middleware reused across all protected routes

Stage 5: configure Swagger UI with bearer auth padlock on all protected routes

Stage 6: publish to GitHub with README, env example, and gitignore

Extras: add 403 admin-only route demonstrating 401 vs 403 distinction

Extras: add refresh token endpoint with short-lived token explanation

Stage 7: AI vs me — prompt, generated code, and diff analysis

Final: complete README with deliverables, setup, and endpoint reference

```



\---



\## Deliverables Checklist



\- ✅ `POST /auth/signup` — creates account, returns 201

\- ✅ `POST /auth/login` — returns JWT access token, 200

\- ✅ `POST /auth/logout` — protected, ends session, 204

\- ✅ `GET /protected/profile` — verified user data, 401 without token

\- ✅ `GET /public/info` — open endpoint, 200

\- ✅ `GET /protected/dashboard` — second protected route, same middleware

\- ✅ `require\_auth` dependency — reusable, applied via `Depends()`

\- ✅ Swagger UI at `/docs` with 🔒 padlock on protected routes

\- ✅ Correct status codes: 201 · 200 · 204 · 400 · 401 · 403

\- ✅ `.env` git-ignored, `.env.example` committed

\- ✅ Public GitHub repo with ≥ 12 commits

\- ✅ README with setup, run command, endpoint table, auth flow

