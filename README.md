## Todo Tracker – Django + React

This project is a full‑stack todo tracker with:

- **Backend**: Django + Django REST Framework (`todo_django`)
- **Frontend**: React + Vite (`todo_react`)

---

## 1. Backend (Django API)

### Run the backend

From `todo_django`:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API is served at `http://127.0.0.1:8000/api`.

### Authentication (`/api/auth/`)
- `POST /api/auth/register/` – Register a new user account
- `POST /api/auth/login/` – Authenticate and obtain token
- `POST /api/auth/logout/` – Logout and revoke token
- `GET /api/auth/profile/` – Get current user profile
- `PATCH /api/auth/profile/` – Update user profile

### Tasks (`/api/tasks/`)
- `GET /api/tasks/` – List all tasks (supports filtering/search/order)
- `POST /api/tasks/` – Create a new task
- `GET /api/tasks/{id}/` – Get specific task details
- `PATCH /api/tasks/{id}/` – Update a task
- `DELETE /api/tasks/{id}/` – Delete a task
- `POST /api/tasks/{id}/complete/` – Toggle task completion status
- `GET /api/tasks/overdue/` – List overdue tasks
- `GET /api/tasks/today/` – List tasks due today

### API documentation

- `GET /api/schema/` – OpenAPI 3.0 specification
- `GET /api/docs/` – Swagger UI interactive docs

---

## 2. Frontend (React app)

The React app lives in `todo_react` and talks to the Django API.

### Configure API base URL

In `todo_react/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### Run the frontend

From `todo_react`:

```bash
npm install
npm run dev
```

Then open `http://localhost:5173/`.

### Main routes

- `/login` – Login with your Django user
- `/dashboard` – Shows basic user info
- `/tasks` – Task list (filter by status, mark complete, delete)
- `/tasks/create` – Create a new task

For details specific to the React project, see `todo_react/README.md`.