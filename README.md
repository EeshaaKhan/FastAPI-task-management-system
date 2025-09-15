# 🗂️ Task Management System

A professional task management system built with FastAPI, SQLAlchemy, and Docker. This system allows multiple users to manage their tasks with full CRUD operations and status tracking.

## ✨ Features

- 👥 **Multi-user Support**: Each user can manage their own tasks
- 📝 **Task Management**: Create, read, update, and delete tasks
- 📊 **Status Tracking**: Track task progress (TODO, IN_PROGRESS, DONE)
- 🌐 **RESTful API**: Clean REST API design with proper HTTP status codes
- 🛡️ **Data Validation**: Comprehensive input validation using Pydantic
- 🗄️ **Database Management**: SQLAlchemy ORM with SQLite database
- 🧪 **Testing**: Full test suite with pytest
- 🐳 **Containerization**: Docker and Docker Compose support
- 📃 **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI 0.104+ 
- **Database**: SQLite with SQLAlchemy ORM 
- **Validation**: Pydantic v2 
- **Testing**: pytest, httpx 
- **Containerization**: Docker & Docker Compose 
- **Database Migrations**: Alembic 
- **Code Quality**: Black, isort, flake8, mypy 

## 📁 Project Structure

```
task-management-system/
├── app/
│   ├── api/v1/           # API endpoints
│   ├── core/             # Core configuration
│   ├── crud/             # CRUD operations
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── utils/            # Utility functions
│   └── main.py           # FastAPI application
├── tests/                # Test suite
├── alembic/              # Database migrations
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # Project documentation
```

## ⚡ Quick Start

### 📋 Prerequisites

-  Python 3.11+
-  Docker (optional)
-  Git

### 🏗️ Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task-management-system
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Initialize database**
   ```bash
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API documentation**
   - 🧭 Swagger UI: http://localhost:8000/api/v1/docs
   - 📘 ReDoc: http://localhost:8000/api/v1/redoc

### 🐳 Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   # Production mode
   docker-compose up --build

   # Development mode with hot reload
   docker-compose --profile dev up --build
   ```

2. **Access the application**
   - 🚀 Production: http://localhost:8000
   - 🛠️ Development: http://localhost:8001

## 📚 API Endpoints

### 👤 Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/{user_id}/with-tasks` - Get user with tasks
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### ✅ Tasks
- `POST /api/v1/users/{user_id}/tasks/` - Create task for user
- `GET /api/v1/users/{user_id}/tasks/` - Get user's tasks
- `GET /api/v1/tasks/{task_id}` - Get task by ID
- `PUT /api/v1/tasks/{task_id}` - Update task
- `PATCH /api/v1/tasks/{task_id}/status` - Update task status
- `DELETE /api/v1/tasks/{task_id}` - Delete task
- `GET /api/v1/users/{user_id}/tasks/stats` - Get task statistics

### ❤️ Health Check
- `GET /health` - Application health status

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_users.py

# Run tests in verbose mode
pytest -v
```

## 🧹 Code Quality

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

## 🔄 Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Task Management System |
| `APP_VERSION` | Application version | 1.0.0 |
| `DEBUG` | Debug mode | True |
| `ENVIRONMENT` | Environment (dev/prod) | development |
| `DATABASE_URL` | Database connection URL | sqlite:///./task_management.db |
| `API_V1_STR` | API version prefix | /api/v1 |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |

## 🛠️ API Usage Examples

### 👤 Create a User
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john.doe@example.com"
     }'
```

### 📝 Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/users/1/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Complete project documentation",
       "description": "Write comprehensive API documentation"
     }'
```

### 🔄 Update Task Status
```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/1/status" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "IN_PROGRESS"
     }'
```

## 🏛️ Architecture & Design Patterns

This project implements several software engineering best practices:

- 🧩 **Clean Architecture**: Separation of concerns with distinct layers
- 🗃️ **Repository Pattern**: CRUD operations abstracted from business logic
- 🧰 **Dependency Injection**: Database sessions and services injected via FastAPI
- 🏭 **Factory Pattern**: CRUD factory functions for consistent instantiation
- 🚨 **Exception Handling**: Custom exceptions with proper HTTP status codes
- 🛡️ **Data Validation**: Pydantic schemas for request/response validation
- 🧪 **Testing Strategy**: Comprehensive unit and integration tests

## ⚡ Performance Considerations

- 🔗 **Connection Pooling**: SQLAlchemy connection pooling for database efficiency
- ⚡ **Query Optimization**: Proper indexing and relationship loading
- 📄 **Pagination**: Built-in pagination for large result sets
- 🗂️ **Caching Headers**: Appropriate HTTP headers for caching strategies
- 🐳 **Container Optimization**: Multi-stage Docker builds for smaller images

## 🔒 Security Features

- 🛡️ **Input Validation**: Comprehensive data validation with Pydantic
- 🛑 **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
- 🌍 **CORS Configuration**: Configurable Cross-Origin Resource Sharing
- 👤 **Non-root Container**: Docker container runs as non-root user
- ❤️ **Health Checks**: Container health monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Project Link: [https://github.com/EeshaaKhan/task-management-system.git](https://github.com/EeshaaKhan/task-management-system.git)