# vector_db_benchmark/benchmark.py

import multiprocessing
import numpy as np
import time
import psutil
import random
import sys
import matplotlib.pyplot as plt


class VectorDBBenchmark:
    def __init__(self, vector_db_class, is_on_disk=True, num_processes=100, random_seed=None):
        self.vector_db_class = vector_db_class
        self.is_on_disk = is_on_disk
        self.num_processes = num_processes
        self.random_seed = random_seed
        self.metrics = {}
        self.random_data = {}  # Stores random data for processes

    def _check_methods(self):
        required_methods_on_disk = [
            'create_collection_and_index',
            'load_collection',
            'ingest_chunks',
            'batch_search'
        ]
        required_methods_in_memory = [
            'create_collection',
            'ingest_chunks',
            'batch_search'
        ]

        methods = required_methods_on_disk if self.is_on_disk else required_methods_in_memory
        missing_methods = [method for method in methods if not hasattr(self.vector_db_class, method)]
        if missing_methods:
            print(f'Error: The class {self.vector_db_class.__name__} is missing methods: {missing_methods}')
            sys.exit(1)

    def _generate_random_data(self):
        # Set random seed
        if self.random_seed is not None:
            random.seed(self.random_seed)
            np.random.seed(self.random_seed)

        for i in range(self.num_processes):
            # Random number of vectors between 10 and 1000
            num_vectors = random.randint(10, 1000)
            vectors = np.random.rand(num_vectors, 1024).astype(np.float32)

            num_searches = random.randint(5, 20)
            sleep_times = [random.uniform(5, 20) for _ in range(num_searches)]
            query_vectors = [np.random.rand(1024).astype(np.float32) for _ in range(num_searches)]

            # Store data for each process
            self.random_data[i] = {
                'num_vectors': num_vectors,
                'vectors': vectors,
                'num_searches': num_searches,
                'sleep_times': sleep_times,
                'query_vectors': query_vectors,
            }

    def _run_process(self, process_id, return_dict, random_data):
        process = psutil.Process()
        initial_memory = process.memory_info().rss

        data = random_data[process_id]
        num_vectors = data['num_vectors']
        vectors = data['vectors']
        num_searches = data['num_searches']
        sleep_times = data['sleep_times']
        query_vectors_list = data['query_vectors']

        vector_db = self.vector_db_class()

        collection_name = f"benchmark_collection_{process_id}"

        if self.is_on_disk:
            # For MilvusDB, we need to call create_collection_and_index with necessary parameters
            vector_db.create_collection_and_index(
                collection_name=collection_name,
                dense_vector_field={
                    'dense_dimension': vectors.shape[1],
                    'index_type': 'IVF_FLAT',  # Adjust as necessary
                    'metric_type': 'L2',       # Adjust as necessary
                    'params': {'nlist': 128},  # Adjust as necessary
                }
            )
            vector_db.load_collection(collection_name)
        else:
            vector_db.create_collection(collection_name)

        start_ingest = time.time()
        # Prepare chunks for MilvusDB.ingest_chunks
        chunks = []
        for i in range(num_vectors):
            chunk = {
                'vector': vectors[i]
            }
            chunks.append(chunk)

        vector_db.ingest_chunks(collection_name, chunks)
        end_ingest = time.time()
        ingest_time = end_ingest - start_ingest

        search_times = []
        for idx in range(num_searches):
            time.sleep(sleep_times[idx])
            query_vector = query_vectors_list[idx].tolist()
            start_search = time.time()

            # Use batch_search
            queries = [query_vector]
            search_params = {
                "anns_field": "vector",
                "param": {"metric_type": "L2", "params": {"nprobe": 10}},
                "limit": 10,
            }
            results = vector_db.batch_search(
                collection_name,
                queries=queries,
                search_params=search_params
            )

            end_search = time.time()
            search_time = end_search - start_search
            search_times.append(search_time)
            print(f'Process {process_id}, Search {idx+1}/{num_searches}, Time: {search_time:.4f} s')

        final_memory = process.memory_info().rss
        memory_used = final_memory - initial_memory
        average_search_time = sum(search_times) / len(search_times)

        # Clean up collection
        vector_db.drop_collection(collection_name)

        return_dict[process_id] = {
            'ingest_time': ingest_time,
            'average_search_time': average_search_time,
            'memory_used_mb': memory_used / (1024 * 1024),
            'num_vectors': num_vectors,
            'num_searches': num_searches,
            'search_times': search_times
        }

    def run_benchmark(self):
        self._check_methods()
        self._generate_random_data()

        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        # Share random data with child processes
        random_data = manager.dict(self.random_data)
        processes = []
        for i in range(self.num_processes):
            p = multiprocessing.Process(target=self._run_process, args=(i, return_dict, random_data))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        self.metrics = dict(return_dict)
        self._generate_reports()

    def _generate_reports(self):
        # Print summary
        print('\nSummary:')
        for process_id, metrics in self.metrics.items():
            print(f'Process {process_id}:')
            print(f'  Ingestion Time: {metrics["ingest_time"]:.4f} s')
            print(f'  Average Search Time: {metrics["average_search_time"]:.4f} s')
            print(f'  Memory Used: {metrics["memory_used_mb"]:.2f} MB')
            print(f'  Number of Vectors: {metrics["num_vectors"]}')
            print(f'  Number of Searches: {metrics["num_searches"]}')

        # Generate graphs
        self._plot_ingestion_times()
        self._plot_search_times()

    def _plot_ingestion_times(self):
        process_ids = []
        ingestion_times = []
        for pid, metrics in self.metrics.items():
            process_ids.append(pid)
            ingestion_times.append(metrics['ingest_time'])

        plt.figure()
        plt.bar(process_ids, ingestion_times)
        plt.xlabel('Process ID')
        plt.ylabel('Ingestion Time (s)')
        plt.title('Ingestion Time per Process')
        plt.savefig('ingestion_time.png')
        plt.close()
        print('Ingestion time graph saved as ingestion_time.png')

    def _plot_search_times(self):
        for pid, metrics in self.metrics.items():
            search_times = metrics['search_times']
            plt.figure()
            plt.plot(range(len(search_times)), search_times, marker='o')
            plt.xlabel('Search Iteration')
            plt.ylabel('Search Time (s)')
            plt.title(f'Search Times for Process {pid}')
            plt.savefig(f'search_times_process_{pid}.png')
            plt.close()
            print(f'Search times graph for Process {pid} saved as search_times_process_{pid}.png')
