"""
MERIDIAN Brain - RECALL Operation (D3.2)
High-level memory retrieval using RLM-based natural language queries.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import time

# Handle both relative and direct imports
try:
    from brain.scripts.memory_store import ChunkStore
    from brain.scripts.repl_environment import REPLSession
except ImportError:
    from memory_store import ChunkStore
    from repl_environment import REPLSession


@dataclass
class RecallResult:
    """Result of a RECALL operation."""
    answer: str
    confidence: float = 0.0
    source_chunks: List[str] = field(default_factory=list)
    traversal_path: List[str] = field(default_factory=list)
    iterations_used: int = 0
    cost_usd: float = 0.0


class RecallOperation:
    """
    High-level RECALL operation for memory retrieval.
    
    Uses RLM (Recursive Language Model) approach with the REPL environment
    to search, retrieve, and synthesize information from stored memories.
    """
    
    def __init__(
        self,
        chunk_store: ChunkStore,
        llm_client=None,
        max_iterations: int = 10,
        timeout_seconds: int = 60
    ):
        """
        Initialize RECALL operation.
        
        Args:
            chunk_store: Storage backend for chunks
            llm_client: LLM client for recursive queries
            max_iterations: Maximum recursive iterations
            timeout_seconds: Query timeout
            
        Raises:
            ValueError: If required parameters are missing
        """
        if chunk_store is None:
            raise ValueError("chunk_store is required")
        
        self.chunk_store = chunk_store
        self.llm_client = llm_client
        self.max_iterations = max_iterations
        self.timeout_seconds = timeout_seconds
        
        # Initialize REPL session if LLM client provided
        self._repl = None
        if llm_client is not None:
            self._repl = REPLSession(
                chunk_store=chunk_store,
                llm_client=llm_client,
                max_iterations=max_iterations,
                timeout_seconds=timeout_seconds
            )
    
    def recall(
        self,
        query: str,
        conversation_id: str = None,
        max_results: int = 5,
        min_confidence: float = 0.5
    ) -> RecallResult:
        """
        Recall information based on natural language query.
        
        Args:
            query: Natural language query
            conversation_id: Optional conversation context filter
            max_results: Maximum number of source chunks to return
            min_confidence: Minimum confidence threshold
            
        Returns:
            RecallResult with answer and metadata
        """
        if not query or not query.strip():
            return RecallResult(
                answer="No query provided",
                confidence=0.0
            )
        
        # If no LLM client, fall back to basic keyword search
        if self.llm_client is None:
            return self._basic_search(query, conversation_id, max_results)
        
        # Use REPL for intelligent retrieval
        return self._repl_retrieval(query, conversation_id, max_results, min_confidence)
    
    # Query expansion synonyms for common concepts
    QUERY_SYNONYMS = {
        # Task/Project management
        'task': ['task', 'bead', 'issue', 'work item', 'todo'],
        'tracking': ['tracking', 'management', 'organization', 'workflow'],
        'beads': ['beads', 'tasks', 'issues', 'tickets'],
        
        # Memory
        'memory': ['memory', 'storage', 'remember', 'recall', 'chunk'],
        'remember': ['remember', 'store', 'save', 'record'],
        
        # Project
        'project': ['project', 'meridian', 'system', 'brain'],
        'status': ['status', 'state', 'progress', 'complete', 'done'],
        
        # Architecture
        'architecture': ['architecture', 'design', 'structure', 'system'],
        'components': ['components', 'parts', 'modules', 'pieces'],
        
        # Testing
        'test': ['test', 'testing', 'validate', 'verify', 'pytest'],
        
        # Files
        'file': ['file', 'document', 'code', 'script'],
        'format': ['format', 'structure', 'layout', 'style'],
    }
    
    def _expand_query(self, query: str) -> List[str]:
        """Expand query with synonyms for better matching."""
        query_lower = query.lower()
        terms = set(query_lower.split())
        
        # Add synonyms for each term
        expanded = set(terms)
        for term in list(terms):
            for key, synonyms in self.QUERY_SYNONYMS.items():
                if term == key or term in synonyms:
                    expanded.update(synonyms)
        
        return list(expanded)
    
    def _basic_search(
        self,
        query: str,
        conversation_id: str = None,
        max_results: int = 5
    ) -> RecallResult:
        """Fallback basic keyword search without LLM."""
        # Get candidate chunks
        if conversation_id:
            chunk_ids = self.chunk_store.list_chunks(
                conversation_id=conversation_id
            )
        else:
            # Search all chunks
            chunk_ids = self.chunk_store.list_chunks()
        
        # Expand query with synonyms for better matching
        query_terms = self._expand_query(query)
        matches = []
        
        # Check ALL chunks (not just first N) to find best matches
        for chunk_id in chunk_ids:
            chunk = self.chunk_store.get_chunk(chunk_id)
            if chunk is None:
                continue
            
            content = chunk.content.lower()
            score = sum(1 for term in query_terms if term in content)
            
            if score > 0:
                matches.append((chunk_id, score, chunk))
        
        # Sort by relevance score
        matches.sort(key=lambda x: x[1], reverse=True)
        
        # Build answer from top matches
        top_matches = matches[:max_results]
        if not top_matches:
            return RecallResult(
                answer="No relevant memories found",
                confidence=0.0,
                source_chunks=[]
            )
        
        # Combine content from matches
        contents = [match[2].content for match in top_matches]
        answer = "\\n\\n".join(contents)
        
        # Calculate average confidence
        avg_confidence = sum(match[2].metadata.confidence for match in top_matches) / len(top_matches)
        
        return RecallResult(
            answer=answer,
            confidence=avg_confidence,
            source_chunks=[match[0] for match in top_matches],
            iterations_used=1
        )
    
    def _repl_retrieval(
        self,
        query: str,
        conversation_id: str = None,
        max_results: int = 5,
        min_confidence: float = 0.5
    ) -> RecallResult:
        """Use REPL for intelligent recursive retrieval."""
        # Build retrieval prompt
        context_filter = f" in conversation {conversation_id}" if conversation_id else ""
        
        retrieval_prompt = f"""You are a memory retrieval system. Answer this query based on stored memories.

Query: "{query}"{context_filter}

Available functions:
- search_chunks(query, limit) - Search for relevant chunks
- read_chunk(chunk_id) - Read full chunk content
- list_chunks_by_tag(tag) - Find chunks by tag
- get_linked_chunks(chunk_id) - Follow memory links
- FINAL(answer) - Return final answer

Instructions:
1. Search for relevant memories using search_chunks()
2. Read promising chunks with read_chunk()
3. Follow links if needed with get_linked_chunks()
4. Synthesize a clear, concise answer
5. Use FINAL() to return your answer

Be thorough but efficient. Consider chunk confidence scores."""
        
        # Execute retrieval via REPL
        start_time = time.time()
        try:
            answer = self._repl.retrieve(
                query=retrieval_prompt,
                max_iterations=self.max_iterations
            )
            
            # If no answer, return empty result
            if answer is None:
                return RecallResult(
                    answer="No relevant memories found",
                    confidence=0.0,
                    iterations_used=self._repl.iteration_count
                )
            
            # Get source chunks from REPL state
            source_chunks = self._extract_source_chunks()
            
            # Calculate metrics
            iterations = self._repl.iteration_count
            cost = getattr(self._repl, '_total_cost', 0.0)
            
            # Estimate confidence based on source quality
            confidence = self._calculate_confidence(source_chunks)
            
            return RecallResult(
                answer=str(answer),
                confidence=confidence,
                source_chunks=source_chunks,
                iterations_used=iterations,
                cost_usd=cost
            )
            
        except Exception as e:
            # Fallback to basic search on error
            return self._basic_search(query, conversation_id, max_results)
    
    def _extract_source_chunks(self) -> List[str]:
        """Extract chunk IDs accessed during REPL execution."""
        # This is a heuristic based on REPL state
        # In a full implementation, we'd track all read_chunk calls
        state = self._repl.get_state()
        
        # Look for variables that might contain chunk IDs
        source_chunks = []
        for var_name, value in state.items():
            if isinstance(value, str) and value.startswith("chunk-"):
                source_chunks.append(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and item.startswith("chunk-"):
                        source_chunks.append(item)
        
        return list(set(source_chunks))  # Remove duplicates
    
    def _calculate_confidence(self, source_chunks: List[str]) -> float:
        """Calculate confidence based on source chunks."""
        if not source_chunks:
            return 0.0
        
        confidences = []
        for chunk_id in source_chunks:
            chunk = self.chunk_store.get_chunk(chunk_id)
            if chunk:
                confidences.append(chunk.metadata.confidence)
        
        if not confidences:
            return 0.5  # Default mid confidence
        
        return sum(confidences) / len(confidences)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get recall operation statistics."""
        return {
            "total_queries": 0,  # Would track in production
            "avg_confidence": 0.0,
            "avg_iterations": 0.0,
            "total_cost_usd": 0.0
        }
