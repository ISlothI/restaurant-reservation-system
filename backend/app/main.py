from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import close_mongo_connection, connect_to_mongo
from app.routes import auth_router, categories_router, reservations_router, restaurants_router, slots_router, tables_router
from app.seed import seed_demo_data


@asynccontextmanager
async def lifespan(application: FastAPI):
    await connect_to_mongo()
    await seed_demo_data()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="Restaurant Reservation System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(restaurants_router, prefix="/api/restaurants", tags=["Restaurants"])
app.include_router(tables_router, prefix="/api/restaurants", tags=["Tables"])
app.include_router(slots_router, prefix="/api/restaurants", tags=["Reservation Slots"])
app.include_router(reservations_router, prefix="/api/reservations", tags=["Reservations"])
app.include_router(categories_router, prefix="/api/categories", tags=["Categories"])


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
