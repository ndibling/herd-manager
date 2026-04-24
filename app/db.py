from sqlmodel import SQLModel, create_engine
import os

DB_PATH = os.environ.get("HERD_DB_PATH", "data/herd.db")
os.makedirs("data/uploads/photos", exist_ok=True)
os.makedirs("data/uploads/docs", exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

def init_db():
    from .models import Animal, Treatment, Organization, Document  # noqa
    SQLModel.metadata.create_all(engine)
