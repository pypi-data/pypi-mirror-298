import fitz
import os
import argparse
import base64
import tempfile
import zipfile
import json
from io import BytesIO

def extract_embedded_files_to_zip(pdf_path):
    """
    Extract all embedded files from the given PDF and return them as a ZIP in memory.
    """
    doc = fitz.open(pdf_path)
    extracted_files = []

    # Extract all embedded files
    for i in range(doc.embfile_count()):
        file_info = doc.embfile_info(i)
        file_name = file_info["name"]
        file_data = doc.embfile_get(i)
        extracted_files.append((file_name, file_data))

    # Return extracted files as a ZIP in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, file_data in extracted_files:
            zip_file.writestr(file_name, file_data)

    zip_buffer.seek(0)
    return zip_buffer

def handle_base64_input(base64_data):
    """
    Handle base64 input, convert to a PDF, extract embedded files, and return ZIP.
    """
    try:
        # Decode the Base64 input
        file_bytes = base64.b64decode(base64_data)

        # Write the decoded bytes to a temporary PDF file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_pdf_path = temp_pdf.name

        # Extract embedded files and return the ZIP
        return extract_embedded_files_to_zip(temp_pdf_path)

    except Exception as e:
        print(f"Error handling Base64 input: {e}")
        return None

def handle_base64_file(base64_file_path):
    """
    Handle a file containing base64-encoded PDF data, extract files, and return ZIP.
    """
    try:
        with open(base64_file_path, 'r') as file:
            data = json.load(file)
            base64_data = data.get('file_data')

            if not base64_data:
                print(f"Error: No 'file_data' field found in {base64_file_path}.")
                return None

            return handle_base64_input(base64_data)

    except Exception as e:
        print(f"Error reading Base64 file: {e}")
        return None

def extract_embedded_files_from_pdf(pdf_path):
    """
    Extract files from a PDF and return them as a ZIP in memory.
    """
    try:
        return extract_embedded_files_to_zip(pdf_path)
    except Exception as e:
        print(f"Error extracting embedded files: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Extract embedded XML files from PDF/A-3 documents and create a normal PDF."
    )
    parser.add_argument("--pdf_path", help="Path to the PDF/A-3 file.")
    parser.add_argument("--output_folder", help="Folder to save the extracted XML files and normal PDF.")
    parser.add_argument("--base64", help="Base64-encoded PDF file.")
    parser.add_argument("--base64_file", help="Path to a JSON file containing a Base64-encoded PDF.")

    args = parser.parse_args()

    # Result will be the in-memory ZIP file containing the extracted files
    result = None

    if args.pdf_path:
        result = extract_embedded_files_from_pdf(args.pdf_path)
    elif args.base64:
        result = handle_base64_input(args.base64)
    elif args.base64_file:
        result = handle_base64_file(args.base64_file)
    else:
        print("Error: You must provide either --pdf_path, --base64, or --base64_file input.")
        return

    if result:
        if args.output_folder:
            zip_filename = os.path.join(args.output_folder, "extracted_files.zip")
            with open(zip_filename, "wb") as zip_file:
                zip_file.write(result.getvalue())
            print(f"ZIP file saved: {zip_filename}")
        else:
            zip_filename = "extracted_files.zip"
            with open(zip_filename, "wb") as zip_file:
                zip_file.write(result.getvalue())
            print(f"ZIP file created: {zip_filename}")
    else:
        print("No files were extracted.")

if __name__ == "__main__":
    main()
