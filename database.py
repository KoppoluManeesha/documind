from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load your .env file — reads DATABASE_URL into environment
load_dotenv()

# Get the database URL from .env file
# Never hardcode this — always read from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# ============================================
# ENGINE — the actual connection to PostgreSQL
# Think of it like the phone line between
# your Python code and PostgreSQL database
# ============================================
engine = create_engine(DATABASE_URL)

# ============================================
# SESSION — how your code talks to database
# Every database operation happens inside a session
# Think of it like opening a notebook to write in
# When done you close it (commit or rollback)
# ============================================
SessionLocal = sessionmaker(
    autocommit=False,  # don't save automatically — we control when to save
    autoflush=False,   # don't send queries automatically
    bind=engine        # use our engine (our phone line)
)

# ============================================
# BASE — the parent class for all your models
# Every SQLAlchemy model inherits from this
# Think of it like Django's models.Model
# ============================================
Base = declarative_base()

# ============================================
# DEPENDENCY — gives a database session to each route
# Opens session → gives to route → closes when done
# This is called for every single API request
# ============================================
def get_db():
    db = SessionLocal()  # open the notebook
    try:
        yield db         # give it to the route
    finally:
        db.close()       # always close it — even if error occurs