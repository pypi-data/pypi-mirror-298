# luigi-chromadb-target

A Luigi Target implementation using ChromaDB.

## Installation

Install the package via pip:

```bash
pip install luigi-chromadb-target
```

## Usage

```python
from luigi_chromadb_target import ChromaDBRegistry, ChromaTarget
import chromadb

# Initialize and register the database
registry = ChromaDBRegistry()
client = chromadb.Client()
client.create_collection(name="documents")
registry.register_database('my_database', client)

# Use ChromaTarget
target = ChromaTarget('chroma://my_database/documents/my_document')
with target.open('w') as f:
    f.write('This is some content.')

with target.open('r') as f:
    content = f.read()
    print(content)  # Outputs: This is some content.
```