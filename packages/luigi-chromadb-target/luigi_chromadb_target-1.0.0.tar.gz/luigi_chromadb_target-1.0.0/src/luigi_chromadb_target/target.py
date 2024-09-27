import io
from contextlib import contextmanager
import chromadb
import luigi

class ChromaTarget(luigi.target.Target):

    def __init__(self, database:chromadb.ClientAPI, collection_name:str, document_id: str):
        self.database = database
        self.collection_name = collection_name
        self.document_id = document_id

    def _get_collection(self) -> chromadb.Collection:
        try:
            return self.database.get_collection(self.collection_name)
        except Exception:
            raise ValueError(f"Collection '{self.collection_name}' does not exist in the database.")

    def exists(self):
        return self.get() is not None

    def put(self, document:str):
        collection = self._get_collection()
        collection.upsert(documents=[document], ids=[self.document_id])

    def get(self):
        collection = self._get_collection()
        response = collection.get(ids=[self.document_id], include=['documents'])
        documents = response.get('documents')
        return documents[0] if documents else None

    @contextmanager
    def open(self, mode='r'):
        buffer = None
        try:
            if mode == 'r':
                document = self.get()
                if document is None:
                    raise FileNotFoundError(f"Document '{self.document_id}' does not exist.")
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