import os
import sys
import json
import hashlib
from pathlib import Path

from extract_images import open_pdf, extract_images_from_pdf


def sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(pdf_path: str, manifest: dict, output_dir: str = "output_images") -> dict:
    title = manifest.get("title") or Path(pdf_path).stem
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip() or "untitled"
    pdf_save_path = os.path.join(output_dir, safe_title)

    # compute checksums for images and augment manifest entries with sha256
    for page in manifest.get("pages", []):
        for img in page.get("images", []):
            img_path = os.path.join(pdf_save_path, img["path"])
            if os.path.exists(img_path):
                img["sha256"] = sha256_of_file(img_path)
            else:
                img["sha256"] = None

    manifest["source"] = pdf_path

    manifest_path = os.path.join(pdf_save_path, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest


def extract_data_cli(pdf_path: str, output_dir: str = "output_images") -> dict:
    pdf_doc = open_pdf(pdf_path)
    if pdf_doc is None:
        raise RuntimeError(f"Failed to open PDF: {pdf_path}")

    manifest = extract_images_from_pdf(pdf_doc, output_dir=output_dir)
    manifest = write_manifest(pdf_path, manifest, output_dir=output_dir)
    return manifest


def main():
    # if len(sys.argv) < 2:
    #     print("Usage: python extractor.py input_pdfs/file.pdf [output_dir]")
    #     sys.exit(1)

    # pdf_path = sys.argv[1]
    # output_dir = sys.argv[2] if len(sys.argv) > 2 else "output_images"
    output_dir = "output_images"
    
    #currently reading directly from input (temporary)
    pdfs_list = [os.path.join("input_pdfs", f) for f in os.listdir('input_pdfs')]
    pdf_path = pdfs_list[0]
    manifest = extract_data_cli(pdf_path, output_dir=output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
