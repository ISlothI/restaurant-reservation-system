# Restaurant Reservation System

A restaurant reservation web application for restaurant managers (admins) and guests.
Admins can manage their restaurant, tables, bookable time slots, and incoming reservations.
Guests can create accounts, reserve tables, specify their preferences, and view their reservation history.

## Technology Stack

- **Backend:** Python 3.12, FastAPI, Pydantic, Motor (async MongoDB), JWT, bcrypt
- **Frontend:** Angular 18, TailwindCSS 3, TypeScript
- **Database:** MongoDB 7
- **Infrastructure:** Docker Compose

## Getting Started

### Prerequisites
- Docker installed

### Running the Application

```bash
docker compose up --build
```

The system will then be available at:
- **Frontend:** http://localhost:4200
- **Backend API:** http://localhost:8000
- **API docs (Swagger):** http://localhost:8000/docs

### Demo Users

Demo data is created automatically on first startup:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | admin123 |
| Guest | guest2@example.com | guest123 |

## Project Structure

```
├── docker-compose.yml          # Full system orchestration
├── backend/                    # FastAPI backend
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── app/
│       ├── main.py             # Application entry point
│       ├── config.py           # Environment variables
│       ├── database.py         # MongoDB connection
│       ├── seed.py             # Demo data
│       ├── models/             # Pydantic schemas
│       ├── routes/             # REST endpoints
│       ├── services/           # Business logic
│       ├── repositories/       # Data access layer
│       └── middleware/         # JWT auth, role check
├── frontend/                   # Angular frontend
│   ├── Dockerfile
│   └── src/app/
│       ├── core/               # Auth service, interceptor, guards
│       ├── shared/models/      # TypeScript interfaces
│       └── features/           # Components (auth, restaurants, admin, reservations)
├── docs/                       # Software documentation
└── prompts/                    # AI usage documentation
```

## REST API Endpoints

### Auth
- `POST /api/auth/register` – Registration
- `POST /api/auth/login` – Login (JWT)
- `GET /api/auth/me` – Current user

### Restaurants
- `GET /api/restaurants` – List (public)
- `GET /api/restaurants/:id` – Details (public)
- `POST /api/restaurants` – Create (admin)
- `PUT /api/restaurants/:id` – Update (admin, own)
- `DELETE /api/restaurants/:id` – Delete (admin, own)

### Tables
- `GET /api/restaurants/:id/tables` – List (public)
- `POST /api/restaurants/:id/tables` – Create (admin)
- `PUT /api/restaurants/:id/tables/:tid` – Update (admin)
- `DELETE /api/restaurants/:id/tables/:tid` – Delete (admin)

### Time Slots
- `GET /api/restaurants/:id/slots` – List (public)
- `POST /api/restaurants/:id/slots` – Create (admin)
- `PUT /api/restaurants/:id/slots/:sid` – Update (admin)
- `DELETE /api/restaurants/:id/slots/:sid` – Delete (admin)

### Reservations
- `GET /api/reservations/my` – My reservations (auth)
- `GET /api/reservations/restaurant/:id` – Restaurant reservations (admin)
- `POST /api/reservations` – New reservation (auth)
- `PATCH /api/reservations/:id` – Update status (auth)
- `DELETE /api/reservations/:id` – Delete (auth)
