from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from datetime import datetime
import uuid


def ingest_document(text: str, source_url: str, title: str, updated_at: str = None):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectors = embeddings.embed_documents(chunks)

    client = QdrantClient(url="http://localhost:6333")
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": chunk,
                "source": source_url,
                "title": title,
                "updated_at": updated_at or datetime.utcnow().isoformat()
            }
        )
        for chunk, vector in zip(chunks, vectors)
    ]
    client.upsert(collection_name="allright_brain", points=points)