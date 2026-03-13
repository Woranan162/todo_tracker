# Todo Tracker – Django + React

A full‑stack task management app with a Django REST API backend and a React (Vite) frontend. Users can authenticate, create/update/delete tasks, and view filtered task lists.

### Project structure

- `todo_django/` – Django project and REST API
- `todo_react/` – React + Vite frontend

---

## Quick start

**Backend (Django):**

```bash
cd todo_django
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend (React):**

```bash
cd todo_react
npm install
npm run dev
```

Then open `http://localhost:5173/`. The API runs at `http://127.0.0.1:8000/api`.

---

## Backend (Django API)

### Authentication (`/api/auth/`)

Endpoints for registering users, logging in, managing tokens, and viewing/updating the current user profile.

- `POST /api/auth/register/` – Register a new user account
- `POST /api/auth/login/` – Authenticate and obtain token
- `POST /api/auth/logout/` – Logout and revoke token
- `GET /api/auth/profile/` – Get current user profile
- `PATCH /api/auth/profile/` – Update user profile

### Tasks (`/api/tasks/`)

CRUD and helper endpoints for tasks belonging to the authenticated user.

- `GET /api/tasks/` – List all tasks (supports filtering, search, ordering)
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

## Frontend (React app)

The React app in `todo_react` talks to the Django API. Set the base URL in `todo_react/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### Main routes

- `/login` – Login with your Django user
- `/dashboard` – Basic user info and links
- `/tasks` – Task list (filter by status, mark complete, delete)
- `/tasks/create` – Create a new task

For more details on the React app (routing, components, styling), see [todo_react/README.md](todo_react/README.md).
