# luigi-chromadb-target

A Luigi Target implementation using ChromaDB.

## Installation

Install the package via pip:

```bash
pip install luigi-chromadb-target
```

## Usage

```python
from luigi_chromadb_target import ChromaTarget
import chromadb

# initialize the client (and the collection)
client = chromadb.Client()
client.create_collection(name="documents")

# Use ChromaTarget
target = ChromaTarget(client, "documents", "my-document-id")
with target.open('w') as f:
    f.write('This is some content.')

with target.open('r') as f:
    content = f.read()
    print(content)  # Outputs: This is some content.
```