import PyPDF2
import os

class PDFChunker:
    def __init__(self, file_path):
        self.file_path = file_path

    def chunk_pdf(self, output_folder, chunk_size=5):
        """
        Splits the PDF into chunks of `chunk_size` pages each.
        :param output_folder: Folder where the chunks will be saved.
        :param chunk_size: Number of pages per chunk.
        :return: None
        """
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open and read the PDF file
        pdf_reader = PyPDF2.PdfReader(self.file_path)
        total_pages = len(pdf_reader.pages)

        for start_page in range(0, total_pages, chunk_size):
            pdf_writer = PyPDF2.PdfWriter()
            end_page = min(start_page + chunk_size, total_pages)

            for i in range(start_page, end_page):
                pdf_writer.add_page(pdf_reader.pages[i])

            chunk_filename = f"{output_folder}/chunk_{start_page // chunk_size + 1}.pdf"
            with open(chunk_filename, "wb") as output_file:
                pdf_writer.write(output_file)

            print(f"Created: {chunk_filename}")
