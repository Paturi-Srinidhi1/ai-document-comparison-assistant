# AI Document Comparison Assistant

## Project Overview

The AI Document Comparison Assistant is a Python-based web application built with Streamlit. It allows users to upload two PDF documents, extract their text, and compare their contents using Google Gemini AI.

The application helps users understand what is similar, what has changed, and which important details may require attention.

## Features

- Upload two PDF documents.
- Validate uploaded files and extract PDF text.
- Generate AI-powered summaries of both documents.
- Identify similarities and differences.
- Highlight important details such as dates, amounts, and requirements.
- Display supporting evidence and page references where available.
- Show comparison results in organized sections.
- Download a PDF report of the comparison.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- pypdf
- python-dotenv
- ReportLab

## Project Structure

```text
ai-document-comparison-assistant/
├── app.py
├── document_reader.py
├── gemini_service.py
├── report_generator.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python installed on your computer.
- A Google Gemini API key.
- Internet access for AI-powered comparison.

## Setup Instructions

### 1. Download or clone the repository

Download the project from GitHub or clone the repository to your computer.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment on Windows

```bat
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a file named `.env` in the project folder and add your own API key:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the example value with your own key. Never publish your real API key on GitHub.

### 6. Run the application

```bash
streamlit run app.py
```

The application should open in your browser.

## How to Use

1. Open the application.
2. Upload the first PDF document.
3. Upload the second PDF document.
4. Review the extracted text and comparison results.
5. Download the PDF comparison report if needed.

## Limitations

- Comparison quality depends on the text extracted from the uploaded PDFs and the AI model's response.
- Scanned PDFs may require OCR if their text cannot be extracted.
- AI-generated results may contain errors. Verify important findings against the original documents.
- AI comparison requires a valid API key, internet access, and available API quota.

## Security

API keys and other secrets must remain in the local `.env` file. Do not upload `.env` or your virtual environment to GitHub.

## Disclaimer

This project is intended to assist with document review. It does not replace professional or legal verification of important documents.