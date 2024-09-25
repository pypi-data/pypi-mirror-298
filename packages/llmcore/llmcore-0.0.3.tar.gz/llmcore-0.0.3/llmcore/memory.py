from typing import List, Dict, Any, Optional
from scipy import spatial
import numpy as np

from llmcore.vector_databases.vector_database_base import VectorDatabase
from llmcore.vector_databases.pinecone_database import PineconeDatabase
from llmcore.vector_databases.chroma_database import ChromaDatabase
from llmcore.core import LLMConfig

def get_vector_database(config: LLMConfig) -> Optional[VectorDatabase]:
    if not config.vector_db_provider:
        return None
    provider = config.vector_db_provider.lower()
    if provider == "pinecone":
        return PineconeDatabase(endpoint=config.vector_db_endpoint, api_key=config.vector_db_api_key)
    elif provider == "chromadb":
        return ChromaDatabase(endpoint=config.vector_db_endpoint)
    # Add more providers here as needed
    else:
        raise ValueError(f"Unsupported vector database provider: {config.vector_db_provider}")

class MemoryManager:
    def __init__(self, config: LLMConfig, capacity: int = 32000):
        # The capacity is the maximum number of memories that can be stored.
        self.capacity = capacity

        # The memories is a list of memories that are stored in the memory manager.
        self.memories: List[Dict[str, Any]] = []

        # The vector_db is the vector database that is used to store the memories.
        self.vector_db = get_vector_database(config)

        # The vector_dim is the dimension of the vectors that are stored in the memory manager.
        self.vector_dim = None

    async def add_memory(self, memory: Dict[str, Any]):
        if not isinstance(memory.get('vector'), (list, np.ndarray)):
            raise ValueError("Memory 'vector' must be a list of floats or a numpy array.")
        
        # Convert to numpy array if it's a list
        if isinstance(memory['vector'], list):
            memory['vector'] = np.array(memory['vector'], dtype=float)
        
        memory['vector'] = memory['vector'].flatten()

        # Set the vector dimension based on the first memory added
        if self.vector_dim is None:
            self.vector_dim = memory['vector'].shape[0]
        elif memory['vector'].shape[0] != self.vector_dim:
            raise ValueError(f"Memory 'vector' must have dimension {self.vector_dim}.")
        
        if len(self.memories) >= self.capacity:
            self.memories.pop(0)
        self.memories.append(memory)
        
        if self.vector_db:
            try:
                await self.vector_db.add_vector(memory['vector'].tolist(), {"content": memory['content']})
            except KeyError as e:
                raise ValueError(f"Memory dict is missing required key: {str(e)}") from e
            except Exception as e:
                raise RuntimeError(f"Failed to add vector to database: {str(e)}") from e

    async def get_relevant_memories(self, query_vector: List[float], k: int = 5, threshold: float = 0.5) -> List[Dict[str, Any]]:
        from llmcore.core import RelevantMemory
        
        # 0. Validation for the query vector
        if not isinstance(query_vector, (list, np.ndarray)):
            raise TypeError("Query vector must be a list of floats or a numpy array.")
        query_vector = np.array(query_vector, dtype=float).flatten()
        if self.vector_dim is not None and query_vector.shape[0] != self.vector_dim:
            raise ValueError(f"Query vector must have dimension {self.vector_dim}.")

        if self.vector_db:
            results = await self.vector_db.search_vectors(query_vector, k)
            return [RelevantMemory(content=result['content'], score=result['score']) for result in results if result['score'] >= threshold]
        else:
            def convert_to_vector(vec):
                if isinstance(vec, list) and all(isinstance(x, (int, float)) for x in vec):
                    return np.array(vec, dtype=float)
                elif isinstance(vec, str):
                    # Attempt to convert string representation to list of floats
                    try:
                        return np.array([float(x) for x in vec.strip('[]').split(',')], dtype=float)
                    except ValueError:
                        print(f"Error converting string to vector: {vec[:100]}...")  # Print first 100 chars of the string
                        return None
                elif isinstance(vec, np.ndarray):
                    return vec
                else:
                    print(f"Unexpected vector type: {type(vec)}")
                    return None

            try:
                valid_memories = []
                for i, mem in enumerate(self.memories):
                    converted_vector = convert_to_vector(mem.get('vector'))
                    if converted_vector is not None:
                        mem['vector'] = converted_vector
                        valid_memories.append(mem)
            except Exception as e:
                print(f"Error processing memories: {str(e)}")
                return []

            try:
                query_vector_np = np.array(query_vector, dtype=float)
                similarities = []
                for i, mem in enumerate(valid_memories):
                    try:
                        sim = self._calculate_similarity(query_vector_np, mem['vector'])
                        similarities.append(sim)
                    except Exception as e:
                        print(f"Error calculating similarity for memory {i}: {str(e)}")
            except Exception as e:
                print(f"Error calculating similarities: {str(e)}")
                return []

            try:
                sorted_indices = np.argsort(similarities)[::-1]
                results = [
                    RelevantMemory(content=valid_memories[i].get('content', ''), score=similarities[i])
                    for i in sorted_indices[:k] if similarities[i] >= threshold
                ]

                return results
            except Exception as e:
                print(f"Error sorting and filtering results: {str(e)}")
                return []

    def _calculate_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        try:
            return 1 - spatial.distance.cosine(vector1, vector2)
        except Exception as e:
            print(f"Error in _calculate_similarity: {str(e)}")
            raise

    def clear(self):
        self.memories.clear()
        if self.vector_db:
            # Implement vector DB clear if supported
            pass