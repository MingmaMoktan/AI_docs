import os
import pathlib
import markdown2

MAX_READ_BYTES = 1_000_000  # 1MB safety limit


def build_file_tree(root_path):
    """Build nested directory tree under root_path."""
    root_path = pathlib.Path(root_path)
    if not root_path.exists():
        return []

    def _walk(curr, base):
        items = []
        try:
            for entry in sorted(curr.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower())):
                rel = str(entry.relative_to(base))

                if entry.is_dir():
                    items.append({
                        "name": entry.name,
                        "path": rel,
                        "type": "dir",
                        "children": _walk(entry, base)
                    })
                else:
                    items.append({
                        "name": entry.name,
                        "path": rel,
                        "type": "file",
                    })
        except PermissionError:
            return []
        return items

    return _walk(root_path, root_path)


def safe_read_file(root_path, rel_path):
    """Read a file safely with size limits and path protection."""
    base = pathlib.Path(root_path).resolve()
    target = (base / rel_path).resolve()

    if not str(target).startswith(str(base)):
        raise ValueError("Invalid file path — blocked")

    if not target.exists() or not target.is_file():
        raise FileNotFoundError("File not found")

    # Mime type guess
    suffix = target.suffix.lower()
    if suffix in (".md", ".markdown"):
        mime = "markdown"
    elif suffix in (".py", ".js", ".ts", ".java", ".c", ".cpp", ".rb", ".go", ".rs"):
        mime = "code"
    elif suffix in (".txt", ".yml", ".yaml", ".json", ".csv", ".ini", ".cfg"):
        mime = "text"
    else:
        mime = "text"

    size = target.stat().st_size
    if size > MAX_READ_BYTES:
        raise OSError("File too large to preview")

    try:
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(target, "r", encoding="latin-1") as f:
            content = f.read()

    # Markdown conversion
    if mime == "markdown":
        try:
            content_html = markdown2.markdown(content)
        except:
            content_html = "<pre>" + content + "</pre>"
        return content_html, "markdown"

    return content, mime

def parse_and_generate_docs(project):
    """
    Placeholder function for future LLM parsing.
    Currently does nothing.
    """
    return True


import os
from django.conf import settings
from .models import GeneratedDoc

# -----------------------------------------------
# STEP 2: Parse extracted files into raw database
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
    Step 2:
    - Walk through extracted folder
    - Read allowed files
    - Save raw content into GeneratedDoc table
    - AI generation will happen in Step 3 later
    """

    extracted_folder = project.extracted_path

    if not extracted_folder or not os.path.exists(extracted_folder):
        return "No extracted folder found."

    # Clear old docs if regenerating
    project.docs.all().delete()

    collected = 0

    # Walk through all files
    for root, dirs, files in os.walk(extracted_folder):
        for file in files:

            ext = os.path.splitext(file)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception as e:
                print(f"Failed reading {file_path}: {e}")
                continue

            # Save raw content to database
            GeneratedDoc.objects.create(
                project=project,
                filename=file,
                content=content,
                generated_by_ai=False,  # raw content, not AI yet
            )

            collected += 1

    return f"Parsed {collected} files successfully."
