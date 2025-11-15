import os
from docx import Document
from PyPDF2 import PdfReader
from core.models import GeneratedDoc

def parse_and_generate_docs(project):
    """
    Parse files in the extracted_path of a ProjectUpload
    and create GeneratedDoc entries.
    """
    extracted_dir = project.extracted_path
    if not extracted_dir or not os.path.exists(extracted_dir):
        return "No extracted files found."

    for root, dirs, files in os.walk(extracted_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            content = ""

            # TXT files
            if file_name.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

            # DOCX files
            elif file_name.lower().endswith(".docx"):
                doc = Document(file_path)
                content = "\n".join([para.text for para in doc.paragraphs])

            # PDF files
            elif file_name.lower().endswith(".pdf"):
                reader = PdfReader(file_path)
                content = "\n".join([page.extract_text() or "" for page in reader.pages])

            else:
                continue  # skip unsupported file types

            if content.strip():
                GeneratedDoc.objects.create(project=project, content=content)

    return "Docs generated successfully."
