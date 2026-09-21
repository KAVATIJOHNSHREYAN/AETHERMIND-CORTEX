"""
AetherMind Cortex Offline Knowledge Engine
Manages document vector database (ChromaDB), hybrid search, and RAG context injection.
"""

import os
import uuid
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from database.connection import DBConnection
from core.logger import get_logger
from core.document_processor import DocumentProcessor

logger = get_logger("KnowledgeEngine")

class KnowledgeEngine:
    """Offline Knowledge RAG Engine powered by ChromaDB vector collection."""

    def __init__(self, db_conn: Optional[DBConnection] = None):
        self.db_conn = db_conn or DBConnection()
        self.processor = DocumentProcessor()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chroma_path = os.path.join(base_dir, "database", "knowledge_vector")
        os.makedirs(chroma_path, exist_ok=True)

        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name="aethermind_knowledge",
            metadata={"description": "AetherMind Offline Document RAG Collection"}
        )
        logger.info("KnowledgeEngine initialized with local ChromaDB Vector Store.")

    def ingest_file(self, file_path: str) -> Dict[str, Any]:
        """
        Ingests a document file, checking for duplicates, chunking text, and storing vector embeddings.
        """
        if not os.path.exists(file_path):
            return {"success": False, "message": f"File does not exist: {file_path}"}

        file_name = os.path.basename(file_path)
        file_hash = DocumentProcessor.calculate_file_hash(file_path)

        # Check duplicate hash in SQLite
        with self.db_conn.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, chunk_count FROM indexed_documents WHERE file_hash = ?", (file_hash,))
            existing = cursor.fetchone()
            if existing:
                logger.info(f"Document already indexed (Hash match): {file_name}")
                return {
                    "success": True,
                    "message": f"Document '{file_name}' already indexed.",
                    "doc_id": existing["id"],
                    "chunk_count": existing["chunk_count"],
                    "duplicate": True
                }

        # Extract & Chunk text
        extracted_text, file_type = self.processor.extract_text(file_path)
        if not extracted_text:
            return {"success": False, "message": f"No extractable text found in '{file_name}'."}

        doc_id = str(uuid.uuid4())
        metadata_base = {
            "doc_id": doc_id,
            "file_name": file_name,
            "file_path": file_path,
            "file_type": file_type
        }

        chunks = self.processor.chunk_text(extracted_text, metadata_base)
        if not chunks:
            return {"success": False, "message": "Failed to create document text chunks."}

        # Add to ChromaDB Vector Store
        chunk_ids = [f"{doc_id}_chunk_{c['metadata']['chunk_index']}" for c in chunks]
        chunk_docs = [c["content"] for c in chunks]
        chunk_metas = [c["metadata"] for c in chunks]

        self.collection.add(
            ids=chunk_ids,
            documents=chunk_docs,
            metadatas=chunk_metas
        )

        # Save record in SQLite
        with self.db_conn.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO indexed_documents (id, file_name, file_path, file_hash, file_type, chunk_count)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (doc_id, file_name, file_path, file_hash, file_type, len(chunks))
            )

        logger.info(f"Successfully indexed document '{file_name}' ({len(chunks)} chunks).")
        return {
            "success": True,
            "message": f"Successfully indexed '{file_name}' ({len(chunks)} chunks).",
            "doc_id": doc_id,
            "chunk_count": len(chunks),
            "duplicate": False
        }

    def list_indexed_documents(self) -> List[Dict[str, Any]]:
        """Lists all currently indexed documents."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, file_name, file_path, file_type, chunk_count, created_at FROM indexed_documents ORDER BY created_at DESC")
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to list indexed documents: {e}")
            return []

    def remove_document(self, doc_id: str) -> bool:
        """Removes a document from SQLite index and deletes its chunks from ChromaDB."""
        try:
            # 1. Remove from SQLite
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM indexed_documents WHERE id = ?", (doc_id,))

            # 2. Remove chunks from ChromaDB matching doc_id
            self.collection.delete(where={"doc_id": doc_id})
            logger.info(f"Removed indexed document [{doc_id}].")
            return True
        except Exception as e:
            logger.error(f"Failed to remove indexed document [{doc_id}]: {e}")
            return False

    def search_rag_chunks(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Performs hybrid semantic retrieval across indexed document chunks matching query.
        """
        if not query.strip() or self.collection.count() == 0:
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=min(limit, self.collection.count())
            )

            ids = results.get("ids", [[]])[0]
            docs = results.get("documents", [[]])[0]
            metas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0] if "distances" in results else [0.0] * len(ids)

            retrieved = []
            for i in range(len(ids)):
                retrieved.append({
                    "id": ids[i],
                    "content": docs[i],
                    "metadata": metas[i],
                    "distance": distances[i] if i < len(distances) else 0.0
                })
            return retrieved
        except Exception as e:
            logger.error(f"Error querying RAG knowledge collection: {e}")
            return []

    def get_rag_context_injection(self, query: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Retrieves top document context and formats RAG prompt injection & citations list.
        """
        chunks = self.search_rag_chunks(query, limit=3)
        if not chunks:
            return "", []

        context_str = "\n--- Retrived Document Knowledge Context (RAG) ---\n"
        citations = []

        for idx, chunk in enumerate(chunks, 1):
            meta = chunk["metadata"]
            source_file = meta.get("file_name", "Unknown File")
            context_str += f"[{idx}] Source: {source_file} (Chunk {meta.get('chunk_index', 0)})\nContent: {chunk['content']}\n\n"
            citations.append({
                "source": source_file,
                "chunk_index": meta.get("chunk_index", 0),
                "content_snippet": chunk['content'][:120] + "..."
            })

        context_str += "-----------------------------------------------------\n"
        return context_str, citations
