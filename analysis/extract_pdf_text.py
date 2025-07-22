import os
BASE_DIR = os.environ.get("PROJECT_ROOT", os.path.dirname(os.path.abspath(__file__)))
import fitz  # PyMuPDF

pdf_path = os.path.join(BASE_DIR, "data", "raw", "dpr_doc", "012_Reznichenko.pdf")
output_txt = os.path.join(BASE_DIR, "data", "raw", "dpr_doc", "012_Reznichenko_extracted.txt")

doc = fitz.open(pdf_path)
with open(output_txt, "w", encoding="utf-8") as out_file:
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        out_file.write(f"\n--- Page {page_num + 1} ---\n")
        out_file.write(text)

print(f"Extracted text saved to {output_txt}")