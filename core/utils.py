import os
import markdown2
from django.conf import settings
from openai import OpenAI
from .models import GeneratedDoc

# -----------------------------------------------
# STEP 2: Raw File Parsing
# -----------------------------------------------

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".md", ".txt", ".json",
    ".html", ".css",
    ".yml", ".yaml",
    ".xml",
    ".ini", ".cfg",
    ".env",
}

def parse_and_generate_docs(project):
    """
    Step 2: Walk through extracted folder, read allowed files, save raw content into GeneratedDoc table.
    """
    extracted_folder = project.extracted_path
    if not extracted_folder or not os.path.exists(extracted_folder):
        return "No extracted folder found."

    # Clear old docs
    project.docs.all().delete()

    collected = 0
    for root, dirs, files in os.walk(extracted_folder):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue

            GeneratedDoc.objects.create(
                project=project,
                filename=file,
                content=content,
                generated_by_ai=False
            )
            collected += 1

    return f"Parsed {collected} files successfully."


# ----------------------------------------------------
# STEP 3: AI Documentation Generation
# ----------------------------------------------------
def generate_ai_docs(project):
    """
    Uses OpenAI to generate documentation for each file’s content.
    Creates new GeneratedDoc entries marked as AI-generated.
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    files = project.docs.filter(generated_by_ai=False)
    if not files.exists():
        return "No raw files found to generate documentation."

    created_count = 0
    for doc in files:
        prompt = f"""
        You are an expert software documentation generator.
        Read the following source file and produce clean, structured technical documentation.
        Requirements:
        - Explain purpose of the file
        - Describe functions, classes, and their responsibilities
        - Show examples if applicable
        - Include architecture notes when relevant
        - Use Markdown format
        - Do not hallucinate — only describe what is present

        --- FILE NAME ---
        {doc.filename}

        --- FILE CONTENT ---
        {doc.content}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You generate accurate technical documentation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )

            ai_output = response.choices[0].message.content

            GeneratedDoc.objects.create(
                project=project,
                filename=f"{doc.filename} — AI Documentation.md",
                content=ai_output,
                generated_by_ai=True
            )
            created_count += 1

        except Exception as e:
            print(f"AI generation failed for {doc.filename}: {e}")
            continue

    return f"AI generated documentation for {created_count} files."


# ----------------------------------------------------
# FILE VIEW UTILITIES
# ----------------------------------------------------
def build_file_tree(root_path):
    """
    Build nested directory tree for file browser
    """
    root_path = os.path.abspath(root_path)
    if not os.path.exists(root_path):
        return []

    tree = []

    for entry in sorted(os.listdir(root_path)):
        entry_path = os.path.join(root_path, entry)
        if os.path.isdir(entry_path):
            tree.append({
                "name": entry,
                "type": "dir",
                "children": build_file_tree(entry_path)
            })
        else:
            tree.append({
                "name": entry,
                "type": "file",
                "path": os.path.relpath(entry_path, root_path)
            })
    return tree


def safe_read_file(root_path, rel_path):
    """
    Read a file safely and return content with MIME type and Prism.js language
    """
    root_path = os.path.abspath(root_path)
    target_path = os.path.abspath(os.path.join(root_path, rel_path))

    if not target_path.startswith(root_path):
        raise ValueError("Invalid file path — blocked")

    if not os.path.isfile(target_path):
        raise FileNotFoundError("File not found")

    ext = os.path.splitext(target_path)[1].lower()
    prism_lang = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "jsx",
        ".tsx": "tsx",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".rb": "ruby",
        ".go": "go",
        ".rs": "rust",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown"
    }.get(ext, "none")

    try:
        with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        with open(target_path, "r", encoding="latin-1") as f:
            content = f.read()

    # Convert markdown to HTML if needed
    if ext in [".md", ".markdown"]:
        extras = ["fenced-code-blocks", "tables", "code-friendly"]
        content_html = markdown2.markdown(content, extras=extras)
        return content_html, "markdown", "markdown"

    return content, "code" if prism_lang != "none" else "text", prism_lang
