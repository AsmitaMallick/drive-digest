from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    google_id = Column(String, unique=True)
    email = Column(String, unique=True)
    name = Column(String)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    filename = Column(String)
    mime_type = Column(String)

    raw_text = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True)

    document_id = Column(Integer, ForeignKey("documents.id"))

    summary_text = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())