import time
import os
from PyPDF2 import PdfMerger, PdfReader


PDF_FILES = ["application_package.pdf", "Reinoso Allen Sem 5 Unofficial Transcript.pdf"]
OUTPUT_FILE = "full_application_package.pdf"

def merge_pdfs():
    # Wait for both PDFs to be fully written (avoid empty-file crash)
    for pdf in PDF_FILES:
        for _ in range(15):  # retry up to ~3 seconds
            if os.path.exists(pdf) and os.path.getsize(pdf) > 0:
                try:
                    PdfReader(pdf)
                    break
                except:
                    pass
            time.sleep(0.2)
        else:
            print(f"❌ Could not merge because {pdf} is not ready.")
            return

    merger = PdfMerger()
    for pdf in PDF_FILES:
        merger.append(pdf)

    merger.write(OUTPUT_FILE)
    merger.close()
    print(f"✅ Updated: {OUTPUT_FILE}")


if __name__ == "__main__":
    merge_pdfs()  # first merge immediately

