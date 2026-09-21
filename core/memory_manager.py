"""
AetherMind Cortex Memory Manager
Provides privacy-first structured long-term memory (SQLite) and semantic vector search (ChromaDB).
"""

import os
import uuid
from typing import List, Dict, Any, Optional
import chromadb
from database.connection import DBConnection
from core.logger import get_logger

logger = get_logger("MemoryManager")

class MemoryManager:
    """Manages User, Project, and Conversation long-term memories with semantic vector lookup."""

    def __init__(self, db_conn: Optional[DBConnection] = None):
        self.db_conn = db_conn or DBConnection()
        
        # Initialize local ChromaDB Client (100% offline)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chroma_path = os.path.join(base_dir, "database", "memory_vector")
        os.makedirs(chroma_path, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name="aethermind_memories",
            metadata={"description": "AetherMind Long-Term Memory Vector Store"}
        )
        logger.info("MemoryManager initialized with local SQLite & ChromaDB Vector Store.")

    def add_memory(
        self,
        category: str,
        key: str,
        content: str,
        importance: int = 5,
        is_pinned: bool = False
    ) -> str:
        """
        Adds a new memory item to SQLite and embeds it into ChromaDB.
        
        Args:
            category: 'user', 'project', or 'conversation'
            key: Short descriptive key/title
            content: Main memory content text
            importance: Integer scale 1-10
            is_pinned: Boolean pin state
        """
        memory_id = str(uuid.uuid4())
        try:
            # 1. SQLite Relational Storage
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO memories (id, category, key, content, importance, is_pinned, is_archived)
                    VALUES (?, ?, ?, ?, ?, ?, 0)
                    """,
                    (memory_id, category.lower(), key, content, importance, 1 if is_pinned else 0)
                )

            # 2. ChromaDB Vector Embedding
            embedding_text = f"Category: {category} | Key: {key} | Details: {content}"
            self.collection.add(
                ids=[memory_id],
                documents=[embedding_text],
                metadatas=[{
                    "category": category.lower(),
                    "key": key,
                    "importance": importance,
                    "is_pinned": 1 if is_pinned else 0
                }]
            )
            logger.info(f"Added memory record [{memory_id}] - {category}:{key}")
            return memory_id
        except Exception as e:
            logger.error(f"Failed to add memory: {e}")
            return memory_id

    def list_memories(
        self,
        category: Optional[str] = None,
        include_archived: bool = False
    ) -> List[Dict[str, Any]]:
        """Lists stored memories filtered by category and archive state."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                query = "SELECT id, category, key, content, importance, is_pinned, is_archived, created_at FROM memories WHERE 1=1"
                params = []
                
                if category and category.lower() != "all":
                    query += " AND category = ?"
                    params.append(category.lower())
                
                if not include_archived:
                    query += " AND is_archived = 0"

                query += " ORDER BY is_pinned DESC, importance DESC, created_at DESC"
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to list memories: {e}")
            return []

    def update_memory_status(self, memory_id: str, is_pinned: Optional[bool] = None, is_archived: Optional[bool] = None) -> bool:
        """Updates pin or archive status of a memory."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                if is_pinned is not None:
                    cursor.execute("UPDATE memories SET is_pinned = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (1 if is_pinned else 0, memory_id))
                if is_archived is not None:
                    cursor.execute("UPDATE memories SET is_archived = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (1 if is_archived else 0, memory_id))
            logger.info(f"Updated memory [{memory_id}] status")
            return True
        except Exception as e:
            logger.error(f"Failed to update memory status for [{memory_id}]: {e}")
            return False

    def delete_memory(self, memory_id: str) -> bool:
        """Deletes a memory record from SQLite and ChromaDB vector store."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            
            # Delete from vector database
            try:
                self.collection.delete(ids=[memory_id])
            except Exception as ve:
                logger.warning(f"ChromaDB delete note: {ve}")
                
            logger.info(f"Deleted memory [{memory_id}]")
            return True
        except Exception as e:
            logger.error(f"Failed to delete memory [{memory_id}]: {e}")
            return False

    def search_semantic_memories(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """
        Performs semantic vector search over long-term memories matching query text.
        """
        if not query.strip():
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=min(limit, max(1, self.collection.count()))
            )
            
            matched_ids = results.get("ids", [[]])[0]
            if not matched_ids:
                return []

            # Retrieve full records from SQLite
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                placeholders = ",".join(["?"] * len(matched_ids))
                cursor.execute(f"SELECT id, category, key, content, importance FROM memories WHERE id IN ({placeholders}) AND is_archived = 0", matched_ids)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Semantic search error: {e}")
            return []

    def get_context_prompt_injection(self, query: str) -> str:
        """
        Retrieves relevant long-term memory context formatted for LLM system prompt injection.
        """
        memories = self.search_semantic_memories(query, limit=3)
        if not memories:
            # Fallback to pinned high importance memories
            memories = self.list_memories(include_archived=False)[:3]

        if not memories:
            return ""

        context_str = "\n--- Long-Term Memory Context ---\n"
        for m in memories:
            context_str += f"- [{m['category'].upper()}] {m['key']}: {m['content']} (Importance: {m['importance']}/10)\n"
        context_str += "-----------------------------------\n"
        return context_str
