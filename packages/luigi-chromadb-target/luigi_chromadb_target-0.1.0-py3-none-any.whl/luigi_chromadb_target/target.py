import io
from contextlib import contextmanager
import luigi

from .registry import ChromaDBRegistry

class ChromaTarget(luigi.target.Target):
    def __init__(self, document_url):
        # document_url schema - chroma://<database>/<collection>/<document_id>
        self.chroma_adapter = ChromaDBRegistry()
        self.document_url = document_url

    def exists(self):
        return self.chroma_adapter.document_exists(self.document_url)

    def put(self, document):
        self.chroma_adapter.store_document(self.document_url, document)

    def get(self):
        return self.chroma_adapter.fetch_document(self.document_url)

    @contextmanager
    def open(self, mode='r'):
        buffer = None
        try:
            if mode == 'r':
                document = self.get()
                if document is None:
                    raise FileNotFoundError(f"Document '{self.document_url}' does not exist.")
                buffer = io.StringIO(document)
                yield buffer
            elif mode == 'w':
                buffer = io.StringIO()
                yield buffer
            else:
                raise ValueError(f"Mode {mode} not supported.")
        finally:
            if buffer is not None:
                if mode == 'w':
                    content = buffer.getvalue()
                    self.put(content)
                buffer.close()