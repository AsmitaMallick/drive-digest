from fastapi import APIRouter
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Document, Summary

from app.services.exporter import (
    export_csv,
    export_pdf
)

router = APIRouter()


@router.get("/download/csv")
async def download_csv():

    db: Session = SessionLocal()

    summaries = db.query(
        Document.filename,
        Summary.summary_text
    ).join(
        Summary,
        Summary.document_id == Document.id
    ).all()

    data = [
        {
            "filename": s.filename,
            "summary": s.summary_text
        }
        for s in summaries
    ]

    filename = "summaries.csv"

    export_csv(data, filename)

    return FileResponse(
        filename,
        media_type="text/csv",
        filename=filename
    )


@router.get("/download/pdf")
async def download_pdf():

    db: Session = SessionLocal()

    summaries = db.query(
        Document.filename,
        Summary.summary_text
    ).join(
        Summary,
        Summary.document_id == Document.id
    ).all()

    data = [
        {
            "filename": s.filename,
            "summary": s.summary_text
        }
        for s in summaries
    ]

    filename = "summaries.pdf"

    export_pdf(data, filename)

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename
    )