import os
from dotenv import load_dotenv


os.environ.pop('DB_NAME', None)
os.environ.pop('DB_USER', None)
os.environ.pop('DB_PASS', None)
os.environ.pop('DATABASE_URL', None)
os.environ.pop('SECRET_KEY', None)

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost:5432/{DB_NAME}"
SECRET_KEY = os.getenv("SECRET_KEY")