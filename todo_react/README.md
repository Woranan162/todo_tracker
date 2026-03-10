## Todo React Frontend

This is the React + Vite frontend for your Django todo tracker.  
It talks to the Django API for authentication and task management.

### Tech stack

- React + Vite
- React Router (`react-router-dom`)
- Axios for API calls (`src/api`)
- Tailwind CSS for styling

### Prerequisites

- Node.js (LTS, e.g. 18+)
- Django backend running on `http://127.0.0.1:8000/api`

In the Django project (`todo_django`) you should already have:

- `path('api/auth/', include('user_account.urls'))`
- `path('api/tasks/', include('tasks.urls'))`

### Environment variables

Create `todo_react/.env` (already present) with:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

If you change the backend URL or port, update this value.

### How to run (frontend)

From the `todo_react` folder:

```bash
npm install
npm run dev
```

Then open:

- `http://localhost:5173/` for the React app

### How to run (backend, reference)

From the `todo_django` folder:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The frontend expects the API to be available at `http://127.0.0.1:8000/api`.

### Main routes (frontend)

- `/login` – login page (uses `/api/auth/login/`)
- `/dashboard` – user info and link to tasks
- `/tasks` – task list (uses `/api/tasks/`)
- `/tasks/create` – create task form (uses `POST /api/tasks/`)

### Folder overview

- `src/api/` – axios instance + auth/tasks API helpers
- `src/pages/` – React pages (`LoginPage`, `DashboardPage`, `TaskListPage`, `CreateTaskPage`)
- `src/store/` – Redux Toolkit store and slices (if you connect them)

This README describes the current setup of **this React project only**.  
The main project README in `todo_tracker/README.md` can describe the full Django + React stack.
