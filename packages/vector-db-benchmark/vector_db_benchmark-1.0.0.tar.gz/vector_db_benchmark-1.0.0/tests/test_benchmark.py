import unittest
from vector_db_benchmark import VectorDBBenchmark

class DummyVectorDB:
    def create_collection(self):
        pass

    def ingest_chunks(self, vectors):
        pass

    def hybrid_search(self, query_vectors, sparse_vectors=None):
        return []

    def batch_search(self, query_vectors):
        return []

class TestVectorDBBenchmark(unittest.TestCase):

    def test_benchmark_in_memory(self):
        benchmark = VectorDBBenchmark(DummyVectorDB, is_on_disk=False, num_processes=1)
        benchmark.run_benchmark()
        self.assertTrue(len(benchmark.metrics) > 0)

if __name__ == '__main__':
    unittest.main()
