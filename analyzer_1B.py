import os
import json
from datetime import datetime

import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util
import numpy as np

DATA_DIR = "/data"
PDF_DIR = os.path.join(DATA_DIR, "PDFs")
INPUT_JSON = os.path.join(DATA_DIR, "challenge1b_input.json")
OUTPUT_JSON = os.path.join(DATA_DIR, "challenge1b_output.json")

# Load model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')


def load_input(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_sections_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if text.strip():
            sections.append({
                "page_number": page_num,
                "text": text.strip()
            })

    doc.close()
    return sections


def embed_texts(texts):
    return model.encode(texts, convert_to_tensor=True)


def main():
    if not os.path.exists(INPUT_JSON):
        print(f"❌ Input file not found at {INPUT_JSON}")
        return

    input_data = load_input(INPUT_JSON)

    persona = input_data["persona"]["role"]
    job = input_data["job_to_be_done"]["task"]
    documents = input_data["documents"]

    print(f"📥 Processing {len(documents)} documents...")

    all_sections = []
    section_metadata = []

    for doc in documents:
        filename = doc["filename"]
        title = doc["title"]
        full_path = os.path.join(PDF_DIR, filename)

        if not os.path.exists(full_path):
            print(f"❌ PDF not found: {filename}")
            continue

        print(f"📄 Reading: {filename}")
        sections = extract_sections_from_pdf(full_path)

        for section in sections:
            all_sections.append(section["text"])
            section_metadata.append({
                "document": filename,
                "page_number": section["page_number"],
                "text": section["text"]
            })

    print("🔍 Embedding job description and sections...")
    job_embedding = embed_texts([job])[0]
    section_embeddings = embed_texts(all_sections)

    print("📊 Computing similarities...")
    similarities = util.cos_sim(job_embedding, section_embeddings)[0].cpu().numpy()
    top_indices = np.argsort(similarities)[::-1][:5]

    extracted_sections = []
    subsection_analysis = []

    for rank, idx in enumerate(top_indices, start=1):
        section = section_metadata[idx]
        extracted_sections.append({
            "document": section["document"],
            "section_title": section["text"][:80].replace("\n", " "),  # trimmed
            "importance_rank": rank,
            "page_number": section["page_number"]
        })

        subsection_analysis.append({
            "document": section["document"],
            "refined_text": section["text"],
            "page_number": section["page_number"]
        })

    output_data = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(OUTPUT_JSON, "w", encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Done! Output written to: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
