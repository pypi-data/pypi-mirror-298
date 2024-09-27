import unittest
import chromadb
from luigi_chromadb_target import ChromaTarget

class TestChromaTarget(unittest.TestCase):

    def setUp(self):
        self.client = chromadb.Client()
        self.collection_name = 'documents'
        self.client.create_collection(name=self.collection_name, get_or_create=True)
        self.document_id = 'foo'

    def test_write_and_read(self):
        target = ChromaTarget(self.client, self.collection_name, self.document_id)
        with target.open('w') as f:
            f.write('content')

        with target.open('r') as f:
            content = f.read()
            self.assertEqual(content, 'content')

    def test_exists(self):
        target = ChromaTarget(self.client, self.collection_name, self.document_id)
        self.assertFalse(target.exists())
        with target.open('w') as f:
            f.write('content')
        self.assertTrue(target.exists())

    def test_nonexistent_document(self):
        target = ChromaTarget(self.client, self.collection_name, 'non-existent-document-id')
        with self.assertRaises(FileNotFoundError):
            with target.open('r') as f:
                f.read()

if __name__ == '__main__':
    unittest.main()