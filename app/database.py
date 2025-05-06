from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./simple_task_manager.db"

# create an SQLAlchemy engine,
# which is the starting point for any SQLAlchemy application
engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# create a factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a base class that the model classes will inherit from
Base = declarative_base()

# dependency for routes to open and close a DB session
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()