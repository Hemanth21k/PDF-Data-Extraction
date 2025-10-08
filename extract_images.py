import os
import pymupdf

def extract_images_from_pdf(pdf_document:pymupdf.Document, output_dir="output_images"):        
    # Create a directory if it doesn't already exist to save extracted images
    os.makedirs(output_dir, exist_ok=True)
    
    title = pdf_document.metadata['title']
    pdf_save_path = os.path.join(output_dir,title)
    pdf_images_path = os.path.join(pdf_save_path,"images")
    pdf_texts_path = os.path.join(pdf_save_path,"texts")
    
    os.makedirs(pdf_save_path, exist_ok=True)
    os.makedirs(pdf_images_path, exist_ok=True)
    os.makedirs(pdf_texts_path, exist_ok=True)
    
    
    
    # Iterate through each page in the PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        
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
            
            print(f"Extracted {image_filename}")
        
        # Extract text from the page
        text = page.get_text("text")
        text_filename = f"page{page_number + 1}_text.txt"
        text_path = os.path.join(pdf_texts_path, text_filename)
        with open(text_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)
    
    print("Image extraction completed.")


def open_pdf(file_path):
    try:
        pdf_document = pymupdf.open(file_path)
        print(type(pdf_document),pdf_document.metadata)
        
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            print(f"Page {page_number + 1}: {page}")
            print(page.get_text("text"))
            #Extract images from the page
            # image_list = page.get_images(full=True)
            
         
        return pdf_document
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return None

def main():
    pdfs_list = [os.path.join("input_pdfs",f) for f in os.listdir('input_pdfs')]
    print(pdfs_list)
    
    pdf_document = open_pdf(pdfs_list[0])
    if pdf_document:
        extract_images_from_pdf(pdf_document)
    
    
if __name__ == "__main__":
    main()
