from sqlalchemy import create_engine, Column, Integer, Text, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    pdf_name = Column(String(255))
    content = Column(Text)
    embedding = Column(Vector(384))


def create_tables():
    Base.metadata.create_all(engine)
    print("Table created successfully")

def is_pdf_loaded(pdf_name: str) -> bool:
    """Check if the PDF has already been processed and loaded."""
    try:
        return session.query(Document).filter_by(pdf_name=pdf_name).first() is not None
    except Exception as e:
        print(f"Error checking DB: {e}")
        return False

def add_pdf_record(pdf_name: str):
    """Add a tracking record for the processed PDF."""
    try:
        # We just insert a tracking row so we know this pdf is loaded.
        doc = Document(pdf_name=pdf_name, content="PDF tracking record")
        session.add(doc)
        session.commit()
    except Exception as e:
        print(f"Error adding to DB: {e}")
        session.rollback()

if __name__ == "__main__":
    create_tables()