import fitz  # PyMuPDF
import os
import json
import re
import argparse

def detect_heading_level(text):
    match = re.match(r"^(\d+)(\.\d+)?(\.\d+)?\s", text.strip())
    if match:
        if match.group(3):
            return "H3"
        elif match.group(2):
            return "H2"
        else:
            return "H1"
    return None

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    all_spans = []

    title = doc.metadata.get("title", "").strip()
    if not title: 
        page = doc.load_page(0)
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if len(text) > 10 and span["size"] > 10:
                        all_spans.append(span)
        title_span = max(all_spans, key=lambda s: s["size"], default={"text": "Untitled"})
        title = title_span["text"].strip()

    spans = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = " ".join([span["text"] for span in line["spans"]]).strip()
                if not line_text:
                    continue
                span = line["spans"][0]
                spans.append({
                    "text": line_text,
                    "size": span["size"],
                    "font": span["font"],
                    "flags": span["flags"],
                    "page": page_num + 1
                })

    unique_sizes = sorted({s["size"] for s in spans}, reverse=True)
    size_h1 = unique_sizes[0] if len(unique_sizes) > 0 else 12
    size_h2 = unique_sizes[1] if len(unique_sizes) > 1 else size_h1
    size_h3 = unique_sizes[2] if len(unique_sizes) > 2 else size_h2

    outline = []
    seen = set()

    for span in spans:
        level = detect_heading_level(span["text"])
        if not level:
            if span["size"] >= size_h1:
                level = "H1"
            elif span["size"] >= size_h2:
                level = "H2"
            elif span["size"] >= size_h3:
                level = "H3"

        is_bold = span["flags"] & 2 != 0
        if not level and is_bold and span["size"] > 10:
            level = "H2"

        if level and span["text"] not in seen:
            seen.add(span["text"])
            outline.append({
                "level": level,
                "text": span["text"],
                "page": span["page"]
            })

    return {
        "title": title.strip(),
        "outline": outline
    }

def main():
    print("🚀 extractor.py has started executing inside the container...")

    parser = argparse.ArgumentParser(description="PDF Outline Extractor")
    parser.add_argument('--input', required=True, help='Path to input PDF file or directory')
    args = parser.parse_args()

    input_path = args.input
    output_dir = "/app/output"

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(input_path):
        print(f"❌ Error: '{input_path}' does not exist.")
        return

    if os.path.isfile(input_path):
        # Single file mode
        filename = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{filename}.json")
        print(f"📄 Processing file: {input_path}")
        result = extract_outline(input_path)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✅ Output saved to: {output_path}")

    elif os.path.isdir(input_path):
        # Batch mode
        print(f"📁 Processing folder: {input_path}")
        for filename in os.listdir(input_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(input_path, filename)
                output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
                print(f"📤 Writing output to: {output_path}")

                print(f"📄 Processing: {filename}")
                result = extract_outline(file_path)

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

        print("✅ All PDFs processed.")

    else:
        print(f"❌ Error: '{input_path}' is neither a file nor a directory.")

if __name__ == "__main__":
    main()
