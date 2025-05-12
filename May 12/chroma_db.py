import chromadb
import os
from chromadb.utils import embedding_functions

class ChromaDBManager:
    """
    A class to manage ChromaDB operations including initialization and document storage.
    """
    
    def __init__(self, collection_name="documents", persist_directory="chroma_db"):
        """
        Initialize the ChromaDB client and collection.
        
        Args:
            collection_name (str): Name of the collection to create or use
            persist_directory (str): Directory to persist the ChromaDB data
        """
        # Create the persist directory if it doesn't exist
        if not os.path.exists(persist_directory):
            os.makedirs(persist_directory)
            
        # Initialize the ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use the default embedding function (all-MiniLM-L6-v2)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )
        
        print(f"ChromaDB initialized with collection: {collection_name}")
    
    def add_documents(self, documents, ids=None, metadatas=None):
        """
        Add documents to the ChromaDB collection.
        
        Args:
            documents (list): List of document texts to add
            ids (list, optional): List of unique IDs for the documents
            metadatas (list, optional): List of metadata dictionaries for the documents
            
        Returns:
            bool: True if documents were added successfully, False otherwise
        """
        try:
            # Generate IDs if not provided
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(documents))]
            
            # Generate empty metadata if not provided
            if metadatas is None:
                metadatas = [{} for _ in range(len(documents))]
            
            # Add documents to the collection
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            
            print(f"Added {len(documents)} documents to the collection")
            return True
            
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")
            return False
    
    def query_collection(self, query_text, n_results=5):
        """
        Query the collection for similar documents.
        
        Args:
            query_text (str): The query text
            n_results (int): Number of results to return
            
        Returns:
            dict: Query results
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            return results
        
        except Exception as e:
            print(f"Error querying ChromaDB: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize ChromaDB
    db_manager = ChromaDBManager()
    
    # Sample documents
    sample_docs = [
        "ChromaDB is a vector database for storing and querying embeddings.",
        "Vector databases are optimized for similarity search operations.",
        "Embeddings are numerical representations of data like text or images.",
        "Retrieval Augmented Generation (RAG) combines retrieval systems with generative AI.",
        "Agentic RAG systems can autonomously decide what information to retrieve."
    ]
    
    # Sample metadata
    sample_metadata = [
        {"source": "definition", "category": "database"},
        {"source": "definition", "category": "database"},
        {"source": "definition", "category": "embeddings"},
        {"source": "definition", "category": "rag"},
        {"source": "definition", "category": "agentic_rag"}
    ]
    
    # Add documents to ChromaDB
    db_manager.add_documents(
        documents=sample_docs,
        ids=[f"sample_{i}" for i in range(len(sample_docs))],
        metadatas=sample_metadata
    )
    
    # Query the collection
    query = "What is a vector database?"
    results = db_manager.query_collection(query)
    
    print("\nQuery Results:")
    print(f"Query: {query}")
    
    if results:
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            print(f"\nResult {i+1}:")
            print(f"Document: {doc}")
            print(f"Metadata: {metadata}")
            print(f"Distance: {distance}")
