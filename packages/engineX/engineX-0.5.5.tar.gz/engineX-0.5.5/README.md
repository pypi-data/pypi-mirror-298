
# SynapseAI

SynapseAI is a Python package for semantic search in PDF documents and web pages. It allows users to extract relevant information from PDFs and websites based on natural language queries.

## Installation

You can install SynapseAI using pip:

```bash
pip install synapseai
```

## Usage

synapseai provides two main functions: `process_pdf` for analyzing PDF documents and `crawl_and_query` for searching web pages.

### Processing a PDF

To search within a PDF document:

```python
from synapseai import process_pdf

pdf_path = "path/to/your/document.pdf"
query = "What is the main topic of this document?"

results = process_pdf(pdf_path, query)

for chunk, similarity in results:
    print(f"Similarity: {similarity:.4f}")
    print(f"Chunk: {chunk[:200]}...")
    print("-" * 50)
```

### Crawling and Querying a Web Page

To search the content of a web page:

```python
from synapseai import crawl_and_query

url = "https://example.com"
query = "What services does this website offer?"

results = crawl_and_query(url, query)

for chunk, similarity in results:
    print(f"Similarity: {similarity:.4f}")
    print(f"Chunk: {chunk[:200]}...")
    print("-" * 50)
```

Both functions return a list of tuples, where each tuple contains a relevant text chunk and its similarity score to the query.

## Configuration

synapseai can be customized by modifying the `config.py` file in the package directory. Here are the available configuration options:

### Embedding Model

- **Variable:** `EMBEDDING_MODEL`
- **Default:** `"sentence-transformers/all-MiniLM-L6-v2"`
- **Description:** The name of the Hugging Face model used for text embeddings.

### Text Chunking

- **Variables:** `CHUNK_SIZE` and `CHUNK_OVERLAP`
- **Defaults:** `CHUNK_SIZE = 1024`, `CHUNK_OVERLAP = 80`
- **Description:** Control how the text is split into chunks for processing.
  - **CHUNK_SIZE:** Maximum number of characters in each chunk.
  - **CHUNK_OVERLAP:** Number of characters that overlap between consecutive chunks.

### Search Results

- **Variable:** `TOP_K_RESULTS`
- **Default:** `5`
- **Description:** The number of top results to return from the semantic search.

### How to Modify Configuration

To change these settings, locate the `config.py` file in your synapseai installation directory and edit the values. For example:

```python
# config.py

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
CHUNK_SIZE = 2048
CHUNK_OVERLAP = 100
TOP_K_RESULTS = 10
```

After modifying the config file, restart your Python environment or reload the synapseai package for the changes to take effect.

### Viewing Current Configuration

You can view the current configuration settings in your Python script or interactive session:

```python
import synapseai

synapseai.print_config()
```

This will display the current values of all configuration options.

## Examples

### Analyzing a Research Paper

```python
from synapseai import process_pdf

pdf_path = "research_paper.pdf"
query = "What are the key findings of this research?"

results = process_pdf(pdf_path, query)

print("Key findings from the research paper:")
for chunk, similarity in results:
    print(f"Relevance: {similarity:.2f}")
    print(chunk)
    print("-" * 50)
```

### Extracting Information from a Company Website

```python
from synapseai import crawl_and_query

url = "https://www.company.com/about"
query = "What is the company's mission statement?"

results = crawl_and_query(url, query)

print("Company mission statement:")
for chunk, similarity in results:
    if similarity > 0.8:  # Only print highly relevant results
        print(chunk)
        break
```

## Troubleshooting

If you encounter any issues:

- Ensure you have the latest version of synapseai installed.
- Check that all dependencies are correctly installed.
- Verify that the PDF file or URL you're trying to access is valid and accessible.
- If you've modified the configuration, try reverting to default settings.

For persistent issues, please open an issue on our GitHub repository.
https://github.com/FastianAbdullah/Synapse-AI

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
