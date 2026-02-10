"""
MERIDIAN Brain - Memory Storage System

Provides RLM-based memory storage with JSON chunks and graph linking.
"""

from .memory_store import (
    ChunkStore,
    ChunkIndex,
    Chunk,
    ChunkMetadata,
    ChunkLinks,
    ChunkType,
    init_storage
)

from .auto_linker import (
    AutoLinker,
    LinkGraph,
    add_manual_link,
    create_chunk_with_links,
    calculate_link_strength
)
from .remember_operation import RememberOperation

# REPL Environment (D1.3)
try:
    from .repl_environment import (
        REPLSession,
        FINAL,
        llm_query,
        SandboxViolation,
        MaxIterationsError,
        TimeoutError
    )
    from .repl_functions import (
        read_chunk,
        search_chunks,
        list_chunks_by_tag,
        get_linked_chunks
    )
    _REPL_AVAILABLE = True
except ImportError:
    _REPL_AVAILABLE = False

__all__ = [
    # Memory store
    "ChunkStore",
    "ChunkIndex",
    "Chunk",
    "ChunkMetadata",
    "ChunkLinks",
    "ChunkType",
    "init_storage",
    # Auto-linker
    "AutoLinker",
    "LinkGraph",
    "add_manual_link",
    "create_chunk_with_links",
    "calculate_link_strength",
    # Remember operation
    "RememberOperation",
    # REPL Environment (D1.3)
    "REPLSession",
    "FINAL",
    "SandboxViolation",
    "MaxIterationsError",
    "TimeoutError",
    "read_chunk",
    "search_chunks",
    "list_chunks_by_tag",
    "get_linked_chunks",
]
