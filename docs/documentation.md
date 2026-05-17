# Szoftverdokumentáció – Étterem Foglalási Rendszer

## 1. Technológiai stack

### Backend
- **Python 3.12** – Választás indoka: rendszeres használat, erős típusrendszer, aszinkron támogatás.
- **FastAPI** – Modern, gyors, OpenAPI dokumentáció automatikusan generálva. Az async/await natívan támogatott.
- **Pydantic v2** – Request/response validáció és szerializáció, típusbiztos modellek.
- **Motor** – Aszinkron MongoDB driver, FastAPI-val tökéletesen integrálható.
- **python-jose** – JWT token generálás és validálás.
- **bcrypt** – Jelszó hash-elés, iparági standard.
- **uvicorn** – ASGI szerver, production-ready.

### Frontend
- **Angular 18** – Komponens-alapú SPA keretrendszer, erős routing, reaktív form-ok, dependency injection.
- **TailwindCSS 3** – Utility-first CSS, gyors prototipizálás, konzisztens design.
- **TypeScript** – Típusbiztos frontend fejlesztés.

### Adatbázis
- **MongoDB 7** – Dokumentum-alapú NoSQL adatbázis, rugalmas séma, jól illeszkedik a JSON-alapú REST API-hoz.

### Infrastruktúra
- **Docker + Docker Compose** – A teljes rendszer egyetlen paranccsal indítható (`docker compose up --build`).
- **Nginx** – A frontend kiszolgálása és API proxy a backend felé.

## 2. Architektúra

Háromrétegű architektúra a backend oldalon:
- **Presentation layer** (`routes/`) – HTTP kérések fogadása, válaszok küldése
- **Business logic layer** (`services/`) – Üzleti szabályok, validáció
- **Data access layer** (`repositories/`) – MongoDB műveletek

## 3. Funkcionális követelmények

- Felhasználói regisztráció és bejelentkezés (JWT)
- Szerepkör-alapú hozzáférés (admin / vendég)
- Éttermek listázása és részleteinek megtekintése (publikus)
- Admin: étterem létrehozása/szerkesztése, asztalok CRUD, időpontok CRUD, foglalások kezelése
- Vendég: foglalás létrehozása (időpont, létszám, alkalom, megjegyzés), foglalások megtekintése, lemondás
- Demó adatok automatikus betöltése első indításkor

## 4. Nem-funkcionális követelmények

- A rendszer Docker Compose-zal egyetlen paranccsal indítható
- Jelszavak bcrypt hash-sel tárolva, soha nem kerülnek visszaküldésre
- JWT token 24 órás lejárattal
- CORS konfigurálva a frontend origin-re
- MongoDB adat perzisztencia Docker volume-mal
- Aszinkron I/O végig (FastAPI + Motor)

## 5. Adatbázis séma

A MongoDB öt kollekcióból áll. Az `_id` mező minden dokumentumban automatikusan generált ObjectId, amelyet a kód string-ként kezel.

### `users`

| Mező | Típus | Megszorítás |
|------|-------|-------------|
| `_id` | ObjectId | automatikus |
| `email` | string | egyedi, érvényes e-mail formátum |
| `password_hash` | string | bcrypt hash, sosem kerül visszaküldésre |
| `full_name` | string | 1–100 karakter |
| `phone` | string | max. 20 karakter, nem kötelező |
| `role` | enum | `admin` \| `guest` |

### `restaurants`

| Mező | Típus | Megszorítás |
|------|-------|-------------|
| `_id` | ObjectId | automatikus |
| `manager_id` | string | → `users._id` (admin) |
| `name` | string | 1–200 karakter |
| `description` | string | max. 2000 karakter |
| `address` | string | 1–300 karakter |
| `contact` | string | max. 100 karakter |
| `opening_hours` | string | max. 200 karakter |
| `services` | string[] | `outdoor_seating`, `vegan_options`, `gluten_free_options`, `wheelchair_accessible`, `pet_friendly` |
| `is_active` | bool | alapértelmezett: `true` |

### `tables`

| Mező | Típus | Megszorítás |
|------|-------|-------------|
| `_id` | ObjectId | automatikus |
| `restaurant_id` | string | → `restaurants._id` |
| `name` | string | 1–100 karakter |
| `capacity` | int | 1–50 |
| `table_type` | enum | `indoor` \| `outdoor` \| `window` |
| `is_active` | bool | alapértelmezett: `true` |

### `reservation_slots`

| Mező | Típus | Megszorítás |
|------|-------|-------------|
| `_id` | ObjectId | automatikus |
| `restaurant_id` | string | → `restaurants._id` |
| `table_id` | string | → `tables._id` |
| `start_at` | datetime | UTC |
| `end_at` | datetime | UTC |
| `status` | enum | `open` \| `closed` — foglaláskor automatikusan `closed`, lemondáskor visszaáll `open`-re |

### `reservations`

| Mező | Típus | Megszorítás |
|------|-------|-------------|
| `_id` | ObjectId | automatikus |
| `restaurant_id` | string | → `restaurants._id` |
| `user_id` | string | → `users._id` |
| `slot_id` | string | → `reservation_slots._id` |
| `party_size` | int | 1–50, nem haladhatja meg az asztal kapacitását |
| `status` | enum | `pending` \| `confirmed` \| `cancelled` |
| `special_occasion` | enum \| null | `birthday`, `anniversary`, `date_night`, `engagement`, `business_dinner`, `family_celebration` |
| `guest_note` | string | max. 500 karakter |
| `created_at` | datetime | UTC |
| `updated_at` | datetime | UTC |

### Kapcsolatok

```
users (1) ────────── (N) restaurants   [manager_id]
restaurants (1) ───── (N) tables        [restaurant_id]
tables (1) ─────────  (N) reservation_slots [table_id]
restaurants (1) ──── (N) reservation_slots  [restaurant_id]
users (1) ──────────  (N) reservations  [user_id]
reservation_slots (1) ─ (1) reservations   [slot_id]
```
