from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload

from app.core.templates import templates
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db.models import Document, Summary

from app.services.parser import (
    parse_pdf,
    parse_docx,
    parse_txt
)

from app.services.gemini_service import summarize_text

import io
import os
import time

DOWNLOAD_DIR = "drive_downloads"

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


router = APIRouter()


@router.get("/documents", response_class=HTMLResponse)
async def documents(request: Request):
    

    db: Session = SessionLocal()

    results = db.query(
        Document.id,
        Document.filename,
        Document.mime_type,
        Summary.summary_text
    ).join(
        Summary,
        Summary.document_id == Document.id
    ).all()

    summaries = [ { "id": r.id, "filename": r.filename, "mime_type": r.mime_type, "summary_text": r.summary_text } for r in results ]

    user = request.session.get("user")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user,
            "summaries": summaries
        }
    )

@router.post("/process-drive-folder")
async def process_drive_folder(
    request: Request,
    folder_id: str = Form(...)
):

    user = request.session.get("user")

    if not user:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    token = request.session.get("token")

    if not token:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    access_token = token.get("access_token")
    refresh_token = token.get("refresh_token")
    scopes = [
        "openid",
        "email",
        "profile",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    if not access_token:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    if refresh_token:

        token_data = {
            "token": access_token,
            "refresh_token": refresh_token,
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "scopes": scopes
        }

        creds = Credentials.from_authorized_user_info(token_data)

    else:

        expires_at = token.get("expires_at")

        if expires_at and expires_at <= time.time():

            return RedirectResponse(
                url="/login",
                status_code=303
            )

        creds = Credentials(token=access_token, scopes=scopes)

    drive_service = build(
        "drive",
        "v3",
        credentials=creds
    )

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)"
    ).execute()

    files = results.get("files", [])

    db: Session = SessionLocal()

    for file in files:

        file_id = file["id"]

        filename = file["name"]

        mime_type = file["mimeType"]

        print("PROCESSING:", filename)

        request_file = drive_service.files().get_media(
            fileId=file_id
        )

        downloaded_file = io.BytesIO()

        downloader = MediaIoBaseDownload(
            downloaded_file,
            request_file
        )

        done = False

        while done is False:

            status, done = downloader.next_chunk()

        filepath = f"{DOWNLOAD_DIR}/{filename}"

        with open(filepath, "wb") as f:

            f.write(downloaded_file.getvalue())

        ext = filename.split(".")[-1].lower()

        try:

            if ext == "pdf":

                text = parse_pdf(filepath)

            elif ext == "docx":

                text = parse_docx(filepath)

            elif ext == "txt":

                text = parse_txt(filepath)

            else:

                print("Unsupported:", filename)

                continue

            summary = summarize_text(text)

            document = Document(
                filename=filename,
                mime_type=mime_type,
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

            print("DONE:", filename)

        except Exception as e:

            print("ERROR:", e)

    return RedirectResponse(
        url="/documents",
        status_code=303
    )    