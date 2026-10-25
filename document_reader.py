
from io import BytesIO

from pypdf import PdfReader


MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
MAX_PAGES = 200

class PDFProcessingError(Exception):
    """Raised when a PDF cannot be processed safely."""


def extract_pdf(uploaded_file):
    """
    Validate an uploaded PDF and extract text page by page.

    Returns a dictionary containing the file name,
    page count, extracted text, page details and
    character count.
    """

    if uploaded_file is None:
        raise PDFProcessingError("Please upload a PDF file.")

    filename = uploaded_file.name

    if not filename.lower().endswith(".pdf"):
        raise PDFProcessingError(
            f"{filename}: Only PDF files are supported."
        )

    pdf_bytes = uploaded_file.getvalue()

    if not pdf_bytes:
        raise PDFProcessingError(
            f"{filename}: The uploaded file is empty."
        )

    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise PDFProcessingError(
            f"{filename}: File exceeds the 20 MB limit."
        )

    try:
        reader = PdfReader(BytesIO(pdf_bytes), strict=True)

        if reader.is_encrypted:
            raise PDFProcessingError(
                f"{filename}: Password-protected PDFs "
                "are not supported in this version."
            )
        if len(reader.pages) > MAX_PAGES:
            raise PDFProcessingError(
                f"{filename}: This PDF contains more than "
                f"{MAX_PAGES} pages. Please upload a smaller PDF."
            )
            
        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:
                raise PDFProcessingError(
                    f"{filename}: Could not read page "
                    f"{page_number}."
                ) from exc

            pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

    except PDFProcessingError:
        raise
    except Exception as exc:
        raise PDFProcessingError(
            f"{filename}: This PDF is invalid, damaged, "
            "or could not be opened."
        ) from exc

    full_text = "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages
        if page["text"]
    )

    if not full_text.strip():
        raise PDFProcessingError(
            f"{filename}: No readable text was found. "
            "The PDF may be scanned or image-only. "
            "OCR support can be added later."
        )
    if len(full_text.strip()) < 50:
        raise PDFProcessingError(
            f"{filename}: Too little readable text was found. "
            "Please upload a PDF containing more text."
        )

    return {
        "filename": filename,
        "page_count": len(pages),
        "character_count": len(full_text),
        "text": full_text,
        "pages": pages
    }