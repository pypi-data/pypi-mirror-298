from setuptools import setup, find_packages

setup(
    name="pdf_chunker",  # The name of your package
    version="0.1.0",  # The version of your package
    description="A Python library for splitting PDF files into smaller chunks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="youremail@example.com",
    url="https://github.com/yourusername/pdf_chunker",  # Your project URL
    packages=find_packages(),
    install_requires=[
        "PyPDF2==3.0.0",  # Specify the version of PyPDF2
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the Python versions that your library supports
)
