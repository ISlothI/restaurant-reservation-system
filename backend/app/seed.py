import logging
from datetime import datetime, timedelta, timezone

import bcrypt

from app.database import get_database

logger = logging.getLogger(__name__)


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def seed_demo_data() -> None:
    db = get_database()

    if await db["users"].count_documents({}) > 0:
        logger.info("Database already seeded – skipping")
        return

    logger.info("Seeding demo data …")

    admin1 = await db["users"].insert_one(
        {
            "email": "admin@example.com",
            "password_hash": _hash("admin123"),
            "full_name": "Kovács István",
            "phone": "+36301234567",
            "role": "admin",
        }
    )
    admin2 = await db["users"].insert_one(
        {
            "email": "admin2@example.com",
            "password_hash": _hash("admin123"),
            "full_name": "Nagy Katalin",
            "phone": "+36309876543",
            "role": "admin",
        }
    )
    guest1 = await db["users"].insert_one(
        {
            "email": "guest@example.com",
            "password_hash": _hash("guest123"),
            "full_name": "Szabó Anna",
            "phone": "+36201112233",
            "role": "guest",
        }
    )
    guest2 = await db["users"].insert_one(
        {
            "email": "guest2@example.com",
            "password_hash": _hash("guest123"),
            "full_name": "Tóth Péter",
            "phone": "+36204445566",
            "role": "guest",
        }
    )

    rest1 = await db["restaurants"].insert_one(
        {
            "manager_id": str(admin1.inserted_id),
            "name": "Budapest Bisztró",
            "description": "Hagyományos magyar konyha modern köntösben, a belváros szívében.",
            "address": "Budapest, Váci utca 12.",
            "contact": "+3611234567",
            "opening_hours": "H-V: 11:00-23:00",
            "services": ["outdoor_seating", "vegan_options", "wheelchair_accessible"],
            "is_active": True,
        }
    )
    rest2 = await db["restaurants"].insert_one(
        {
            "manager_id": str(admin2.inserted_id),
            "name": "Dunakorzó Étterem",
            "description": "Panorámás étterem a Duna-parton, nemzetközi és magyar ételekkel.",
            "address": "Budapest, Belgrád rakpart 4.",
            "contact": "+3617654321",
            "opening_hours": "H-Szo: 12:00-22:00, V: 12:00-20:00",
            "services": ["outdoor_seating", "gluten_free_options", "pet_friendly"],
            "is_active": True,
        }
    )

    r1_id = str(rest1.inserted_id)
    r2_id = str(rest2.inserted_id)

    t1 = await db["tables"].insert_one(
        {"restaurant_id": r1_id, "name": "A1 - Ablak melletti", "capacity": 4, "table_type": "window", "is_active": True}
    )
    t2 = await db["tables"].insert_one(
        {"restaurant_id": r1_id, "name": "A2 - Terasz", "capacity": 6, "table_type": "outdoor", "is_active": True}
    )
    t3 = await db["tables"].insert_one(
        {"restaurant_id": r1_id, "name": "A3 - Belső terem", "capacity": 2, "table_type": "indoor", "is_active": True}
    )
    t4 = await db["tables"].insert_one(
        {"restaurant_id": r2_id, "name": "B1 - Panoráma", "capacity": 4, "table_type": "window", "is_active": True}
    )
    t5 = await db["tables"].insert_one(
        {"restaurant_id": r2_id, "name": "B2 - Kerti asztal", "capacity": 8, "table_type": "outdoor", "is_active": True}
    )

    now = datetime.now(timezone.utc)
    tomorrow = now + timedelta(days=1)
    day_after = now + timedelta(days=2)

    s1 = await db["reservation_slots"].insert_one(
        {
            "restaurant_id": r1_id,
            "table_id": str(t1.inserted_id),
            "start_at": tomorrow.replace(hour=18, minute=0, second=0, microsecond=0),
            "end_at": tomorrow.replace(hour=20, minute=0, second=0, microsecond=0),
            "max_guests": 4,
            "status": "open",
        }
    )
    s2 = await db["reservation_slots"].insert_one(
        {
            "restaurant_id": r1_id,
            "table_id": str(t2.inserted_id),
            "start_at": tomorrow.replace(hour=19, minute=0, second=0, microsecond=0),
            "end_at": tomorrow.replace(hour=21, minute=0, second=0, microsecond=0),
            "max_guests": 6,
            "status": "open",
        }
    )
    s3 = await db["reservation_slots"].insert_one(
        {
            "restaurant_id": r1_id,
            "table_id": str(t3.inserted_id),
            "start_at": day_after.replace(hour=12, minute=0, second=0, microsecond=0),
            "end_at": day_after.replace(hour=14, minute=0, second=0, microsecond=0),
            "max_guests": 2,
            "status": "open",
        }
    )
    s4 = await db["reservation_slots"].insert_one(
        {
            "restaurant_id": r2_id,
            "table_id": str(t4.inserted_id),
            "start_at": tomorrow.replace(hour=18, minute=0, second=0, microsecond=0),
            "end_at": tomorrow.replace(hour=20, minute=0, second=0, microsecond=0),
            "max_guests": 4,
            "status": "open",
        }
    )
    s5 = await db["reservation_slots"].insert_one(
        {
            "restaurant_id": r2_id,
            "table_id": str(t5.inserted_id),
            "start_at": day_after.replace(hour=19, minute=0, second=0, microsecond=0),
            "end_at": day_after.replace(hour=22, minute=0, second=0, microsecond=0),
            "max_guests": 8,
            "status": "open",
        }
    )

    await db["reservations"].insert_one(
        {
            "restaurant_id": r1_id,
            "user_id": str(guest1.inserted_id),
            "slot_id": str(s1.inserted_id),
            "party_size": 2,
            "status": "confirmed",
            "special_occasion": "date_night",
            "guest_note": "Ablak melletti asztalt kérünk, ha lehet.",
            "created_at": now,
            "updated_at": now,
        }
    )
    await db["reservations"].insert_one(
        {
            "restaurant_id": r2_id,
            "user_id": str(guest2.inserted_id),
            "slot_id": str(s4.inserted_id),
            "party_size": 3,
            "status": "pending",
            "special_occasion": "birthday",
            "guest_note": "Születésnapi torta meglepetés lehetséges?",
            "created_at": now,
            "updated_at": now,
        }
    )

    logger.info("Demo data seeded successfully")
