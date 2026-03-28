from langchain_community.vectorstores import Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
import pinecone
import os


# Initialize embedding model (must match teammate's model)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Connect to Pinecone using environment variables
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)

# Get index name from .env
pinecone_index_name = os.getenv("PINECONE_INDEX")


def load_vector_database():
    """
    Connects to Pinecone index and returns vector store
    """
    pinecone_index = pinecone.Index(pinecone_index_name)
    vector_db = Pinecone(pinecone_index, embedding_model, text_key="text")
    return vector_db


def get_relevant_chunks(user_query):
    """
    Takes user query → finds top relevant chunks from vector DB
    """
    vector_db = load_vector_database()

    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}   # top 4 results
    )

    retrieved_docs = retriever.get_relevant_documents(user_query)

    # Extract only text content
    relevant_chunks = [doc.page_content for doc in retrieved_docs]

    if not relevant_chunks:
        return "No relevant information found in the document."

    return relevant_chunks