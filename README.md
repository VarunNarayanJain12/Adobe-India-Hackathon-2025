```markdown
# PDF Outline Extractor

🚀 A Dockerized Python solution that processes PDF documents and extracts a structured outline (headings H1, H2, H3) into a JSON format.

---

## 🧩 Problem Statement

The task is to parse and understand the structural outline of PDF documents and convert them into a standardized machine-readable format. This includes:

- Detecting section titles and subheadings.
- Differentiating heading levels (H1, H2, H3) based on visual and pattern cues.
- Returning a JSON with the extracted document structure.

---

## 🧠 Solution Overview

The solution uses the **PyMuPDF (`fitz`)** library to extract text, font sizes, and metadata from PDF files. Headings are inferred using:

- Font size hierarchy.
- Bold font flags.
- Numeric patterns like `1.`, `1.1.`, `1.1.1` for structural cues.

### 📂 Input

Directory containing one or more `.pdf` files.

### 📄 Output

A JSON file per input PDF containing:
```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "1 Introduction",
      "page": 1
    },
    ...
  ]
}
```

---

## 🛠 Technologies Used

| Tool         | Purpose                                |
|--------------|----------------------------------------|
| Python 3.10   | Programming Language                   |
| PyMuPDF (`fitz`) | PDF text extraction & parsing       |
| Docker       | Containerization for platform-agnostic builds |
| argparse     | Command-line interface parsing         |
| json         | Output formatting                      |

---

## 📦 Setup Instructions

### 1️⃣ Build Docker Image

```bash
docker build --platform linux/amd64 -t pdf-extractor.submission .
```

### 2️⃣ Run the Container

```bash
docker run --rm -v "$(pwd)/input:/app/input:ro" -v "$(pwd)/output/repoidentifier:/app/output" --network none pdf-extractor.submission
```

✅ Processed JSONs will be saved to `output/repoidentifier/`.

---

## 📁 Folder Structure

```
.
├── Dockerfile
├── extractor.py
├── input/
│   └── file01.pdf
├── output/
│   └── repoidentifier/
├── README.md
```

---

## 🧪 Sample Output

```json
{
  "title": "Introduction to AI",
  "outline": [
    {
      "level": "H1",
      "text": "1. Overview",
      "page": 1
    },
    {
      "level": "H2",
      "text": "1.1 History",
      "page": 2
    }
  ]
}
```

---

## 📌 Notes

- Supports both single and batch PDF processing.
- Assumes visible font sizes and boldness as structural indicators.
- Files are read-only (`:ro`) to ensure input integrity.
- No internet/network access (`--network none`) for security compliance.

---

## 📬 Contact

**Varun Narayan Jain**  
For queries, feel free to reach out via GitHub or email.

---
```
