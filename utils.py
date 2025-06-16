from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from ebooklib import epub
import os

def add_thumbnail(input_path, output_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".pdf":
        add_thumbnail_to_pdf(input_path, output_path)
    elif ext == ".epub":
        add_thumbnail_to_epub(input_path, output_path)
    else:
        raise ValueError("Unsupported file type")

def add_thumbnail_to_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(reader.metadata)
    with open(output_path, "wb") as f:
        writer.write(f)

def add_thumbnail_to_epub(input_path, output_path):
    book = epub.read_epub(input_path)
    with open("default_thumb.jpg", "rb") as img_file:
        image_content = img_file.read()
    book.set_cover("cover.jpg", image_content)
    epub.write_epub(output_path, book)
