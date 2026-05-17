from app.routes.auth_routes import router as auth_router
from app.routes.restaurant_routes import router as restaurants_router
from app.routes.table_routes import router as tables_router
from app.routes.slot_routes import router as slots_router
from app.routes.reservation_routes import router as reservations_router
from app.routes.category_routes import router as categories_router

__all__ = [
    "auth_router",
    "restaurants_router",
    "tables_router",
    "slots_router",
    "reservations_router",
    "categories_router",
]
