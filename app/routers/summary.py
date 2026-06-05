from fastapi import APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.services.parser import (
    parse_pdf,
    parse_docx,
    parse_txt
)

from app.services.gemini_service import summarize_text

from app.db.session import SessionLocal
from app.db.models import Document, Summary

import shutil
import os

router = APIRouter()


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/summarize")
async def summarize_document(
    file: UploadFile = File(...)
):

    filepath = f"{UPLOAD_DIR}/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ext = file.filename.split(".")[-1]

    if ext == "pdf":
        text = parse_pdf(filepath)

    elif ext == "docx":
        text = parse_docx(filepath)

    elif ext == "txt":
        text = parse_txt(filepath)

    else:
        return {"error": "Unsupported file"}

    summary = summarize_text(text)

    db: Session = SessionLocal()

    document = Document(
        filename=file.filename,
        mime_type=file.content_type,
        raw_text=text
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    db_summary = Summary(
        document_id=document.id,
        summary_text=summary
    )

    db.add(db_summary)
    db.commit()

    return RedirectResponse( url="/documents", status_code=303 )