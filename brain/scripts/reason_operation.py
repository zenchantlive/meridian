"""
MERIDIAN Brain - REASON Operation (D3.3)
High-level memory analysis and synthesis using RLM.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import time

# Handle both relative and direct imports
try:
    from brain.scripts.memory_store import ChunkStore
    from brain.scripts.recall_operation import RecallOperation, RecallResult
except ImportError:
    from memory_store import ChunkStore
    from recall_operation import RecallOperation, RecallResult


@dataclass
class ReasonResult:
    """Result of a REASON operation."""
    synthesis: str
    insights: List[str] = field(default_factory=list)
    evidence: Dict[str, List[str]] = field(default_factory=dict)
    confidence: float = 0.0
    source_chunks: List[str] = field(default_factory=list)
    iterations_used: int = 0
    cost_usd: float = 0.0


class ReasonOperation:
    """
    High-level REASON operation for memory analysis and synthesis.
    
    Uses RLM to:
    - Analyze patterns across memories
    - Synthesize insights from multiple sources
    - Identify contradictions or gaps
    - Generate conclusions with evidence
    """
    
    def __init__(
        self,
        chunk_store: ChunkStore,
        llm_client=None,
        max_iterations: int = 10
    ):
        """
        Initialize REASON operation.
        
        Args:
            chunk_store: Storage backend
            llm_client: LLM for reasoning
            max_iterations: Maximum analysis iterations
        """
        if chunk_store is None:
            raise ValueError("chunk_store is required")
        
        self.chunk_store = chunk_store
        self.llm_client = llm_client
        self.max_iterations = max_iterations
        
        # Initialize recall for gathering evidence
        self._recall = None
        if llm_client is not None:
            self._recall = RecallOperation(
                chunk_store=chunk_store,
                llm_client=llm_client,
                max_iterations=max_iterations
            )
    
    def reason(
        self,
        query: str,
        context_chunks: List[str] = None,
        analysis_type: str = "synthesis"
    ) -> ReasonResult:
        """
        Perform reasoning analysis on memories.
        
        Args:
            query: Analysis question or topic
            context_chunks: Optional specific chunks to analyze
            analysis_type: Type of analysis (synthesis, comparison, pattern, gap)
            
        Returns:
            ReasonResult with synthesis and insights
        """
        if not query or not query.strip():
            return ReasonResult(
                synthesis="No query provided",
                confidence=0.0
            )
        
        # Gather evidence
        if context_chunks:
            evidence = self._gather_evidence(context_chunks)
        else:
            evidence = self._search_evidence(query)
        
        if not evidence:
            return ReasonResult(
                synthesis="No relevant evidence found for analysis",
                confidence=0.0
            )
        
        # Perform analysis based on type
        if analysis_type == "synthesis":
            return self._synthesize(query, evidence)
        elif analysis_type == "comparison":
            return self._compare(query, evidence)
        elif analysis_type == "pattern":
            return self._find_patterns(query, evidence)
        elif analysis_type == "gap":
            return self._identify_gaps(query, evidence)
        else:
            return self._synthesize(query, evidence)
    
    def _gather_evidence(self, chunk_ids: List[str]) -> Dict[str, Any]:
        """Gather evidence from specific chunks."""
        evidence = {
            "chunks": [],
            "tags": set(),
            "types": set()
        }
        
        for chunk_id in chunk_ids:
            chunk = self.chunk_store.get_chunk(chunk_id)
            if chunk:
                evidence["chunks"].append(chunk)
                evidence["tags"].update(chunk.tags)
                evidence["types"].add(chunk.type)
        
        evidence["tags"] = list(evidence["tags"])
        evidence["types"] = list(evidence["types"])
        
        return evidence
    
    def _search_evidence(self, query: str) -> Dict[str, Any]:
        """Search for relevant evidence."""
        # Use recall to find relevant chunks
        if self._recall is None:
            # Fallback to basic search
            chunk_ids = self.chunk_store.list_chunks()
            return self._gather_evidence(chunk_ids[:10])
        
        recall_result = self._recall.recall(query, max_results=10)
        return self._gather_evidence(recall_result.source_chunks)
    
    def _synthesize(self, query: str, evidence: Dict[str, Any]) -> ReasonResult:
        """Synthesize insights from evidence."""
        chunks = evidence["chunks"]
        
        # Build synthesis from chunk contents
        contents = [chunk.content for chunk in chunks]
        
        if not contents:
            return ReasonResult(
                synthesis="No content to synthesize",
                confidence=0.0
            )
        
        # Simple synthesis: combine unique insights
        synthesis = self._build_synthesis(query, contents)
        
        # Extract insights
        insights = self._extract_insights(contents)
        
        # Calculate confidence
        avg_confidence = sum(
            chunk.metadata.confidence for chunk in chunks
        ) / len(chunks) if chunks else 0.0
        
        return ReasonResult(
            synthesis=synthesis,
            insights=insights,
            evidence={"sources": [chunk.id for chunk in chunks]},
            confidence=avg_confidence,
            source_chunks=[chunk.id for chunk in chunks],
            iterations_used=1
        )
    
    def _build_synthesis(self, query: str, contents: List[str]) -> str:
        """Build synthesis text from contents."""
        # Simple synthesis - in production this would use LLM
        if not contents:
            return "No information available"
        
        if len(contents) == 1:
            return contents[0]
        
        # Combine multiple sources
        synthesis_parts = [f"Based on {len(contents)} sources:"]
        for i, content in enumerate(contents[:5], 1):
            synthesis_parts.append(f"{i}. {content}")
        
        return "\\n".join(synthesis_parts)
    
    def _extract_insights(self, contents: List[str]) -> List[str]:
        """Extract key insights from contents."""
        insights = []
        
        # Simple insight extraction - look for patterns
        for content in contents:
            if "prefer" in content.lower():
                insights.append(f"Preference identified: {content[:100]}...")
            if "like" in content.lower():
                insights.append(f"Positive sentiment: {content[:100]}...")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_insights = []
        for insight in insights:
            if insight not in seen:
                seen.add(insight)
                unique_insights.append(insight)
        
        return unique_insights[:5]  # Top 5 insights
    
    def _compare(self, query: str, evidence: Dict[str, Any]) -> ReasonResult:
        """Compare different pieces of evidence."""
        chunks = evidence["chunks"]
        
        if len(chunks) < 2:
            return ReasonResult(
                synthesis="Need at least 2 items to compare",
                confidence=0.0
            )
        
        # Build comparison
        comparison_parts = ["Comparison:"]
        for i, chunk in enumerate(chunks, 1):
            comparison_parts.append(f"\\nOption {i}: {chunk.content}")
        
        synthesis = "\\n".join(comparison_parts)
        
        return ReasonResult(
            synthesis=synthesis,
            insights=[f"Comparing {len(chunks)} options"],
            confidence=0.7,
            source_chunks=[chunk.id for chunk in chunks]
        )
    
    def _find_patterns(self, query: str, evidence: Dict[str, Any]) -> ReasonResult:
        """Find patterns across evidence."""
        chunks = evidence["chunks"]
        tags = evidence.get("tags", [])
        types = evidence.get("types", [])
        
        insights = []
        
        # Pattern: Common tags
        if tags:
            insights.append(f"Common themes: {', '.join(tags[:5])}")
        
        # Pattern: Content types
        if types:
            insights.append(f"Content types: {', '.join(types)}")
        
        # Pattern: Temporal (if timestamps available)
        if chunks:
            dates = [chunk.metadata.created_at for chunk in chunks if hasattr(chunk.metadata, 'created_at')]
            if dates:
                insights.append(f"Evidence spans {len(set(dates))} time periods")
        
        return ReasonResult(
            synthesis=f"Found {len(insights)} patterns across {len(chunks)} memories",
            insights=insights,
            confidence=0.75,
            source_chunks=[chunk.id for chunk in chunks]
        )
    
    def _identify_gaps(self, query: str, evidence: Dict[str, Any]) -> ReasonResult:
        """Identify gaps in knowledge."""
        chunks = evidence["chunks"]
        
        gaps = []
        
        # Check for low confidence items
        low_confidence = [
            chunk for chunk in chunks
            if chunk.metadata.confidence < 0.6
        ]
        if low_confidence:
            gaps.append(f"{len(low_confidence)} items have low confidence")
        
        # Check for missing links
        unlinked = [
            chunk for chunk in chunks
            if not chunk.links
        ]
        if unlinked:
            gaps.append(f"{len(unlinked)} items have no connections")
        
        if not gaps:
            gaps.append("No significant gaps identified")
        
        return ReasonResult(
            synthesis=f"Knowledge gap analysis: {'; '.join(gaps)}",
            insights=gaps,
            confidence=0.6,
            source_chunks=[chunk.id for chunk in chunks]
        )
    
    def analyze_contradictions(
        self,
        chunk_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Analyze chunks for potential contradictions.
        
        Args:
            chunk_ids: Chunks to analyze
            
        Returns:
            List of potential contradictions
        """
        contradictions = []
        
        chunks = []
        for chunk_id in chunk_ids:
            chunk = self.chunk_store.get_chunk(chunk_id)
            if chunk:
                chunks.append(chunk)
        
        # Simple contradiction detection
        # Look for chunks with contradicts links
        for chunk in chunks:
            if hasattr(chunk.links, 'contradicts') and chunk.links.contradicts:
                for target_id in chunk.links.contradicts:
                    contradictions.append({
                        "chunk_a": chunk.id,
                        "chunk_b": target_id,
                        "reasoning": "Explicit contradiction link"
                    })
        
        return contradictions
    
    def get_stats(self) -> Dict[str, Any]:
        """Get reasoning operation statistics."""
        return {
            "total_analyses": 0,
            "avg_confidence": 0.0,
            "avg_insights": 0.0
        }
