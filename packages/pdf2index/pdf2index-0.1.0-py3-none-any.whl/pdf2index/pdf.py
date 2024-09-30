from pathlib import Path

import pypdfium2 as pdfium


def extract_text(filepath: Path, password: str):
    pdf = pdfium.PdfDocument(filepath, password=password)
    text_list = [page.get_textpage().get_text_bounded() for page in pdf]
    return text_list
