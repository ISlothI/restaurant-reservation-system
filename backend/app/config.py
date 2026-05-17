from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://rrs_admin:rrs_secret@localhost:27017/restaurant_reservation?authSource=admin"
    database_name: str = "restaurant_reservation"
    jwt_secret: str = "super-secret-jwt-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440

    model_config = {"env_prefix": "", "case_sensitive": False}


settings = Settings()
