from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="engineX",
    version="0.5.6",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
        'docx2txt',
        'langchain',
        'langchain_community',
        'langchain_text_splitters',
        'faiss-cpu',
        'numpy',
        'Pillow',
        'pytesseract',
        'PyPDF2',
    ],
    entry_points={
        'console_scripts': [
            'enginex=enginex.main:main',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)