# todo_tracker

## 🔧 Detailed Endpoints

### Authentication (`/api/auth/`)
- `POST /api/auth/register/` - Register a new user account
- `POST /api/auth/login/` - Authenticate and obtain tokens
- `POST /api/auth/logout/` - Logout and revoke tokens
- `GET /api/auth/profile/` - Get current user profile
- `PATCH /api/auth/profile/` - Update user profile

### Tasks (`/api/tasks/`)
- `GET /api/tasks/` - List all tasks (supports filtering)
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Get specific task details
- `PATCH /api/tasks/{id}/` - Update a task
- `DELETE /api/tasks/{id}/` - Delete a task
- `POST /api/tasks/{id}/complete/` - Toggle task completion status
- `GET /api/tasks/overdue/` - List overdue tasks
- `GET /api/tasks/today/` - List tasks due today

### Documentation (`/api/`)
- `GET /api/schema/` - OpenAPI 3.0 specification
- `GET /api/docs/` - Interactive API documentation (Swagger UI)