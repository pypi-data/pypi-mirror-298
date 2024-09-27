import unittest
import os
from pdf_chunker.chunker import PDFChunker

class TestPDFChunker(unittest.TestCase):
    def setUp(self):
        self.chunker = PDFChunker("sample.pdf")
        self.output_folder = "chunks"

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def test_chunk_pdf(self):
        # Test if the PDF is chunked correctly
        self.chunker.chunk_pdf(self.output_folder, chunk_size=5)
        self.assertTrue(len(os.listdir(self.output_folder)) > 0)

if __name__ == '__main__':
    unittest.main()
