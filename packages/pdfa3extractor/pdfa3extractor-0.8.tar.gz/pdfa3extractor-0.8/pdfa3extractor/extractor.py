import fitz
import os
import argparse
import base64
import tempfile
import zipfile
from io import BytesIO

def extract_embedded_files(pdf_path, output_folder=None):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    extracted_files = []

    # Extract embedded XML files
    for i in range(doc.embfile_count()):
        # Get the embedded file info
        file_info = doc.embfile_info(i)
        file_name = file_info["name"]

        # Extract the embedded file if it is an XML
        if file_name.endswith(".xml"):
            file_data = doc.embfile_get(i)
            extracted_files.append((file_name, file_data))

            # Save the extracted file if output_folder is provided
            if output_folder:
                os.makedirs(output_folder, exist_ok=True)
                output_path = os.path.join(output_folder, file_name)
                with open(output_path, "wb") as output_file:
                    output_file.write(file_data)
                print(f"Extracted: {output_path}")

    # If output_folder is not provided, return the ZIP file directly
    if not output_folder:
        return create_zip_from_extracted_files(extracted_files)
    else:
        # Optionally, you can also save a "normal" PDF without embedded files
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_pdf_path = os.path.join(output_folder, f"{base_name}_converted.pdf")
        doc_new = fitz.open()  # Create a new PDF
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            doc_new.insert_pdf(doc, from_page=page_num, to_page=page_num)

        doc_new.save(output_pdf_path)
        print(f"Normal PDF saved as: {output_pdf_path}")

def handle_base64_input(base64_data, output_folder=None):
    try:
        # Decode the Base64 input
        file_bytes = base64.b64decode(base64_data)
        
        # Create a temporary file for the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_pdf_path = temp_pdf.name
            
        # Extract embedded files from the temporary PDF
        return extract_embedded_files(temp_pdf_path, output_folder)

    except Exception as e:
        print(f"Error handling Base64 input: {e}")

def handle_base64_file(base64_file_path, output_folder=None):
    try:
        with open(base64_file_path, 'r') as file:
            # Assuming the file contains a JSON payload with a base64 field
            data = json.load(file)
            base64_data = data.get('file_data')

            if not base64_data:
                print(f"Error: No 'file_data' field found in {base64_file_path}.")
                return

            return handle_base64_input(base64_data, output_folder)

    except Exception as e:
        print(f"Error reading Base64 file: {e}")

def create_zip_from_extracted_files(extracted_files):
    """Create a ZIP file from the list of extracted files."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, file_data in extracted_files:
            zip_file.writestr(file_name, file_data)

    zip_buffer.seek(0)
    return zip_buffer

def main():
    parser = argparse.ArgumentParser(
        description="Extract embedded XML files from PDF/A-3 documents and create a normal PDF."
    )
    parser.add_argument("--pdf_path", help="Path to the PDF/A-3 file.")
    parser.add_argument("--output_folder", help="Folder to save the extracted XML files and normal PDF.")
    parser.add_argument("--base64", help="Base64-encoded PDF file.")
    parser.add_argument("--base64_file", help="Path to a JSON file containing a Base64-encoded PDF.")

    args = parser.parse_args()

    if args.pdf_path:
        result = extract_embedded_files(args.pdf_path, args.output_folder)
    elif args.base64:
        result = handle_base64_input(args.base64, args.output_folder)
    elif args.base64_file:
        result = handle_base64_file(args.base64_file, args.output_folder)
    else:
        print("Error: You must provide either --pdf_path, --base64, or --base64_file input.")
        return

    # If no output folder was provided, output the ZIP file
    if result and not args.output_folder:
        zip_filename = "extracted_files.zip"
        with open(zip_filename, "wb") as zip_file:
            zip_file.write(result.getvalue())
        print(f"ZIP file created: {zip_filename}")

if __name__ == "__main__":
    main()
