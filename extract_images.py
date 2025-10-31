import os
import pymupdf

def extract_images_from_pdf(pdf_document: pymupdf.Document, output_dir="output_images"):
    """Extract images and page text into output_dir/<PDF Title>/ and return a manifest dict.

    Returns a manifest dict with pages, text paths, and image filenames (relative to the PDF folder).
    """
    os.makedirs(output_dir, exist_ok=True)

    title = pdf_document.metadata.get('title') or "untitled"
    # sanitize title to filesystem-friendly name
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip() or "untitled"
    pdf_save_path = os.path.join(output_dir, safe_title)
    pdf_images_path = os.path.join(pdf_save_path, "images")
    pdf_texts_path = os.path.join(pdf_save_path, "texts")

    os.makedirs(pdf_save_path, exist_ok=True)
    os.makedirs(pdf_images_path, exist_ok=True)
    os.makedirs(pdf_texts_path, exist_ok=True)

    manifest = {
        "source": None,
        "title": title,
        "pages": [],
    }

    # Iterate through each page in the PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]

        page_entry = {
            "page_no": page_number + 1,
            "text_path": None,
            "images": []
        }

        # Extract images from the page
        image_list = page.get_images(full=True)

        # Iterate through each image
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Define the output image path
            image_filename = f"page{page_number + 1}_img{img_index + 1}.{image_ext}"
            image_path = os.path.join(pdf_images_path, image_filename)

            # Save the image to the output directory
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)

            page_entry["images"].append({
                "id": image_filename,
                "path": os.path.relpath(image_path, pdf_save_path)
            })

            print(f"Extracted {image_filename}")

        # Extract text from the page
        text = page.get_text("text")
        text_filename = f"page{page_number + 1}_text.txt"
        text_path = os.path.join(pdf_texts_path, text_filename)
        with open(text_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)

        page_entry["text_path"] = os.path.relpath(text_path, pdf_save_path)
        manifest["pages"].append(page_entry)

    print("Image extraction completed.")
    return manifest


def open_pdf(file_path):
    """Open a PDF and return a pymupdf Document or None."""
    try:
        pdf_document = pymupdf.open(file_path)
        return pdf_document
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return None


def main():
    pdfs_list = [os.path.join("input_pdfs", f) for f in os.listdir('input_pdfs')]
    if not pdfs_list:
        print("No PDFs found in input_pdfs/")
        return

    pdf_document = open_pdf(pdfs_list[0])
    if pdf_document:
        manifest = extract_images_from_pdf(pdf_document)
        print(manifest)


if __name__ == "__main__":
    main()
