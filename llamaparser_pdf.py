# import os
# import base64
# import logging
# import csv
# from dotenv import load_dotenv
# from llama_parse import LlamaParse
# import fitz
#
#
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#
# load_dotenv()
#
# # Get API key and PDF path from environment variables
# LLAMA_API_KEY = os.getenv('LLAMAPARSE_API_KEY')
# pdf_path = os.getenv('new_pdf')
#
# # Validate environment variables
# absolute_pdf_path = os.path.abspath(pdf_path)
# logging.info(f"Checking file path: {absolute_pdf_path}")
#
# if not os.path.exists(absolute_pdf_path):
#     raise FileNotFoundError(f"Error: The file '{absolute_pdf_path}' was not found. Please check the file path.")
#
# # Initialize LlamaParse
# llama_parse = LlamaParse(api_key=LLAMA_API_KEY, extract_layout=True)
#
# try:
#
#     logging.info("Parsing PDF with LlamaParse...")
#     parsed_docs = llama_parse.load_data(absolute_pdf_path)
# except Exception as e:
#     logging.error(f"Error parsing the file with LlamaParse: {e}")
#     raise
#
# # Creating output directories
# output_folder = "output"
# images_folder = os.path.join(output_folder, "images")
# tables_folder = os.path.join(output_folder, "tables")
# os.makedirs(images_folder, exist_ok=True)
# os.makedirs(tables_folder, exist_ok=True)
# logging.info(f"Created output folders: {images_folder}, {tables_folder}")
#
# # Markdown output storage
# markdown_output = []
#
# image_count = 0
# tables_extracted = False
# images_extracted = False
#
# for doc_index, doc in enumerate(parsed_docs):
#     markdown_output.append(f"# Document: {doc.metadata.get('file_name', f'Unnamed_{doc_index}')}\n\n")
#     markdown_output.append(f"{doc.text}\n\n")
#
#
#     if hasattr(doc, 'tables') and doc.tables:
#         tables_extracted = True
#         markdown_output.append("## Tables\n")
#         for table_index, table in enumerate(doc.tables):
#             table_filename = f"table_{doc_index}_{table_index}.csv"
#             table_path = os.path.join(tables_folder, table_filename)
#
#
#             with open(table_path, 'w', newline='', encoding='utf-8') as csvfile:
#                 csv_writer = csv.writer(csvfile)
#                 csv_writer.writerows(table)
#
#             # Add table reference to markdown
#             markdown_output.append(f"[Table {table_index + 1}]({os.path.join('tables', table_filename)})\n\n")
#             for row in table:
#                 markdown_output.append("| " + " | ".join(row) + " |\n")
#             markdown_output.append("|" + " --- |" * len(table[0]) + "\n\n")
#
#     # Process Images from LlamaParse
#     if hasattr(doc, 'images') and doc.images:
#         images_extracted = True
#         logging.info(f"Found {len(doc.images)} images in document {doc_index}.")
#         markdown_output.append("## Images\n")
#         for img_index, img in enumerate(doc.images):
#             img_filename = f"image_{doc_index}_{img_index}.jpeg"
#             img_path = os.path.join(images_folder, img_filename)
#
#             try:
#                 decoded_image = base64.b64decode(img)
#                 with open(img_path, "wb") as img_file:
#                     img_file.write(decoded_image)
#
#                 # Add image reference to markdown
#                 markdown_output.append(f"![Image {img_index + 1}]({os.path.join('images', img_filename)})\n\n")
#                 logging.info(f"Saved LlamaParse image: {img_path}")
#
#             except Exception as e:
#                 logging.error(f"Error decoding or saving LlamaParse image {img_index + 1}: {e}")
#
#
# if not images_extracted:
#
#     # Function to extract images using PyMuPDF
#     def extract_images_with_pymupdf(pdf_path, images_folder):
#         doc = fitz.open(pdf_path)  # Open the PDF
#         image_count = 0
#
#         for page_number in range(len(doc)):
#             for img_index, img in enumerate(doc[page_number].get_images(full=True)):
#                 xref = img[0]
#                 base_image = doc.extract_image(xref)
#                 img_bytes = base_image["image"]
#
#                 # Save extracted image
#                 img_filename = f"image_{page_number+1}_{img_index+1}.png"
#                 img_path = os.path.join(images_folder, img_filename)
#
#                 with open(img_path, "wb") as img_file:
#                     img_file.write(img_bytes)
#
#                 logging.info(f"Saved image: {img_path}")
#                 image_count += 1
#
#         return image_count
#
#     # Save it in the markdown file
#     try:
#         new_image_count = extract_images_with_pymupdf(absolute_pdf_path, images_folder)
#         if new_image_count == 0:
#             logging.warning("No images found using PyMuPDF either.")
#         else:
#             markdown_output.append(f"## Extracted Images\n")
#             for i in range(1, new_image_count + 1):
#                 markdown_output.append(f"![Image {i}]({os.path.join('images', f'image_{i}.png')})\n\n")
#
#     except Exception as e:
#         logging.error(f"Error extracting images with PyMuPDF: {e}")
#
# # Save extracted content to a Markdown file
# md_file_path = os.path.join(output_folder, "extracted_output.md")
# with open(md_file_path, "w", encoding="utf-8") as f:
#     f.writelines(markdown_output)
#
# logging.info(f"Extraction completed.Check output folder: {output_folder}")
