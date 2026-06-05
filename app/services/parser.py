import fitz
import re

from docx import Document


def clean_text(text: str):

    # Replace multiple whitespace/newlines with single space
    text = re.sub(r"\s+", " ", text)

    # Remove only problematic control characters
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)

    return text.strip()


def parse_pdf(path: str):

    doc = fitz.open(path)

    pages = []

    # Read first 4 pages
    max_pages = min(4, len(doc))

    for page_num in range(max_pages):

        page = doc[page_num]

        page_text = page.get_text()

        if page_text.strip():

            pages.append(page_text)

    text = " ".join(pages)

    text = clean_text(text)

    # IMPORTANT DEBUG
    print("\nPDF EXTRACTED TEXT:\n")
    print(text[:2000])

    # Better limit
    text = text[:7000]

    return text


def parse_docx(path: str):

    doc = Document(path)

    paragraphs = []

    for para in doc.paragraphs:

        if para.text.strip():

            paragraphs.append(para.text)

    text = " ".join(paragraphs)

    text = clean_text(text)

    print("\nDOCX EXTRACTED TEXT:\n")
    print(text[:2000])

    text = text[:7000]

    return text


def parse_txt(path: str):

    with open(path, "r", encoding="utf-8") as f:

        text = f.read()

    text = clean_text(text)

    print("\nTXT EXTRACTED TEXT:\n")
    print(text[:2000])

    text = text[:7000]

    return text