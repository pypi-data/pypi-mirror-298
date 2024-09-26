import threading
import chromadb
from urllib.parse import urlparse, ParseResult
from typing import Tuple

class SingletonMeta(type):
    _instances = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ChromaDBRegistry(metaclass=SingletonMeta):
    def __init__(self):
        self.databases = {}
        self._lock = threading.Lock()

    def register_database(self, database_name: str, database: chromadb.ClientAPI):
        with self._lock:
            if database_name not in self.databases:
                self.databases[database_name] = database

    def store_document(self, document_url: str, document: str):
        database_name, collection_name, document_id = self._parse_url(document_url)
        database = self._get_database(database_name)
        collection = self._get_collection(database, collection_name)
        collection.upsert(documents=[document], ids=[document_id])

    def fetch_document(self, document_url: str) -> str:
        database_name, collection_name, document_id = self._parse_url(document_url)
        database = self._get_database(database_name)
        collection = self._get_collection(database, collection_name)
        response = collection.get(ids=[document_id], include=['documents'])
        documents = response.get('documents')
        return documents[0] if documents else None

    def document_exists(self, document_url: str) -> bool:
        return self.fetch_document(document_url) is not None

    def _parse_url(self, document_url: str) -> Tuple[str, str, str]:
        parsed_url: ParseResult = urlparse(document_url)

        if parsed_url.scheme != 'chroma':
            raise ValueError("Invalid URL scheme. Expected 'chroma'.")

        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError(
                "Invalid document URL format. Expected 'chroma://<database>/<collection>/<document_id>'."
            )

        database_name = parsed_url.netloc
        collection_name = path_parts[0]
        document_id = "/".join(path_parts[1:])

        return database_name, collection_name, document_id

    def _get_database(self, database_name: str) -> chromadb.ClientAPI:
        database = self.databases.get(database_name)
        if not database:
            raise ValueError(f"Database '{database_name}' not registered.")
        return database

    def _get_collection(
        self, database: chromadb.ClientAPI, collection_name: str
    ) -> chromadb.Collection:
        try:
            return database.get_collection(collection_name)
        except Exception:
            raise ValueError(f"Collection '{collection_name}' does not exist in the database.")