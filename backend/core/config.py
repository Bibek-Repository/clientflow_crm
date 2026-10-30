import os
from dotenv import load_dotenv

# Load environment variables from the project's .env file
load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")


settings = Settings()