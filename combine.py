import time
import os
from PyPDF2 import PdfMerger, PdfReader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PDF_FILES = ["coverletter.pdf", "resume.pdf"]
OUTPUT_FILE = "application_package.pdf"

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

class PDFChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if any(event.src_path.endswith(pdf) for pdf in PDF_FILES):
            merge_pdfs()

if __name__ == "__main__":
    merge_pdfs()  # first merge immediately
    print("👀 Watching for changes... (Ctrl+C to stop)")
    observer = Observer()
    observer.schedule(PDFChangeHandler(), ".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
