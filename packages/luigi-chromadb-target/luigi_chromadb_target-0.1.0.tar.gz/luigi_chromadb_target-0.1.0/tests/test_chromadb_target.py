import unittest
from luigi_chromadb_target import ChromaDBRegistry, ChromaTarget
import chromadb

class TestChromaTarget(unittest.TestCase):

    def setUp(self):
        # Initialize the ChromaDB client and register it
        self.registry = ChromaDBRegistry()
        self.client = chromadb.Client()
        self.client.create_collection(name="documents")
        self.registry.register_database('testdb', self.client)
        self.document_url = 'chroma://testdb/documents/foo'

    def test_write_and_read(self):
        target = ChromaTarget(self.document_url)
        with target.open('w') as f:
            f.write('content')

        with target.open('r') as f:
            content = f.read()
            self.assertEqual(content, 'content')

    def test_exists(self):
        target = ChromaTarget(self.document_url)
        self.assertFalse(target.exists())
        with target.open('w') as f:
            f.write('content')
        self.assertTrue(target.exists())

    def test_nonexistent_document(self):
        target = ChromaTarget('chroma://testdb/documents/nonexistent')
        with self.assertRaises(FileNotFoundError):
            with target.open('r') as f:
                f.read()

if __name__ == '__main__':
    unittest.main()