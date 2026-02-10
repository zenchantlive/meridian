"""
MERIDIAN Brain - REPL Environment (D1.3)
RLM-style external memory REPL with secure sandbox execution.
"""

import ast
import builtins
import threading
import time
import io
import sys
from contextlib import contextmanager
from typing import Any, Dict, Optional, Callable
from pathlib import Path


class SandboxViolation(Exception):
    """Raised when code attempts to violate sandbox security."""
    pass


class MaxIterationsError(Exception):
    """Raised when max iterations exceeded."""
    pass


class TimeoutError(Exception):
    """Raised when execution times out."""
    pass


# Allowed built-ins for sandbox
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
    'callable', 'chr', 'classmethod', 'complex', 'delattr', 'dict',
    'dir', 'divmod', 'enumerate', 'filter', 'float', 'format', 'frozenset',
    'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input',
    'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals',
    'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'ord',
    'pow', 'print', 'property', 'range', 'repr', 'reversed',
    'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str',
    'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__build_class__',
    '__name__', 'True', 'False', 'None', 'Exception', 'TypeError',
    'ValueError', 'KeyError', 'IndexError', 'AttributeError', 'RuntimeError',
    'StopIteration', 'ArithmeticError', 'LookupError', 'AssertionError',
    'NotImplementedError', 'ZeroDivisionError', 'OverflowError',
}

# Blocked imports/modules
BLOCKED_MODULES = {
    'os', 'sys', 'subprocess', 'socket', 'urllib', 'http', 'ftplib',
    'smtplib', 'telnetlib', 'poplib', 'imaplib', 'nntplib', 'ssl',
    'email', 'xmlrpc', 'concurrent.futures.process', 'multiprocessing',
    'ctypes', 'cffi', 'mmap', 'resource', 'posix', 'nt', 'pwd', 'grp',
    'spwd', 'crypt', 'termios', 'tty', 'pty', 'fcntl', 'msvcrt',
    'winreg', '_winapi', 'select', 'selectors', 'asyncio.subprocess',
}


class SandboxVisitor(ast.NodeVisitor):
    """AST visitor to check for sandbox violations."""
    
    def __init__(self, allowed_paths: Optional[list] = None):
        self.allowed_paths = allowed_paths or []
        self.violations = []
    
    def visit_Import(self, node):
        for alias in node.names:
            module = alias.name.split('.')[0]
            if module in BLOCKED_MODULES:
                self.violations.append(f"Import of '{module}' is not allowed")
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module:
            module = node.module.split('.')[0]
            if module in BLOCKED_MODULES:
                self.violations.append(f"Import from '{module}' is not allowed")
        self.generic_visit(node)
    
    def visit_Call(self, node):
        # Check for eval/exec/compile
        if isinstance(node.func, ast.Name):
            if node.func.id in ('eval', 'exec', 'compile'):
                self.violations.append(f"Use of '{node.func.id}()' is not allowed")
        # Check for __import__
        if isinstance(node.func, ast.Name) and node.func.id == '__import__':
            self.violations.append("Use of '__import__()' is not allowed")
        # Check for open()
        if isinstance(node.func, ast.Name) and node.func.id == 'open':
            self.violations.append("Use of 'open()' is not allowed")
        self.generic_visit(node)


def check_safety(code: str) -> list:
    """Check code for sandbox violations."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []  # Let SyntaxError be handled elsewhere
    
    visitor = SandboxVisitor()
    visitor.visit(tree)
    return visitor.violations


# Standalone llm_query function for import compatibility
def llm_query(prompt: str, context: Dict[str, Any] = None) -> str:
    """
    Standalone llm_query function.
    Note: This is a placeholder - use REPLSession.llm_query() for actual queries.
    """
    raise RuntimeError("llm_query must be called from a REPLSession instance")


def FINAL(answer) -> None:
    """Signal that REPL has reached final answer."""
    raise RuntimeError("FINAL() must be called from within a REPL session")


class REPLSession:
    """
    RLM REPL Session - secure sandbox for recursive LLM execution.
    """
    
    def __init__(self, chunk_store=None, llm_client=None, 
                 max_iterations: int = 10, timeout_seconds: int = 60, max_depth: int = 5):
        """
        Initialize REPL session.
        
        Args:
            chunk_store: ChunkStore instance for memory access
            llm_client: LLM client for recursive queries
            max_iterations: Maximum recursive iterations allowed
            timeout_seconds: Execution timeout
            max_depth: Maximum recursion depth
        """
        if chunk_store is None:
            raise ValueError("chunk_store is required")
        if llm_client is None:
            raise ValueError("llm_client is required")
        
        self.chunk_store = chunk_store
        self.llm_client = llm_client
        self.max_iterations = max_iterations
        self.timeout_seconds = timeout_seconds
        self.max_depth = max_depth
        
        self._state: Dict[str, Any] = {}  # User state (empty initially)
        self._iteration_count = 0
        self._total_cost = 0.0
        self._result = None
        self._complete = False
        self._lock = threading.RLock()
        self._output = []
        self._stderr = []
        
        # Create isolated namespace for execution
        self._namespace = {}
        self._setup_namespace()
    
    def _setup_namespace(self):
        """Set up the sandbox namespace."""
        # Safe builtins
        safe_builtins = {name: getattr(builtins, name) 
                        for name in ALLOWED_BUILTINS 
                        if hasattr(builtins, name)}
        
        # Inject memory functions
        from repl_functions import read_chunk, search_chunks, list_chunks_by_tag, get_linked_chunks
        
        # Create bound methods
        safe_builtins['read_chunk'] = self._read_chunk_wrapper
        safe_builtins['search_chunks'] = self._search_chunks_wrapper
        safe_builtins['list_chunks_by_tag'] = self._list_chunks_by_tag_wrapper
        safe_builtins['get_linked_chunks'] = self._get_linked_chunks_wrapper
        safe_builtins['llm_query'] = self._llm_query_wrapper
        safe_builtins['FINAL'] = self._final_wrapper
        
        self._namespace = {
            '__builtins__': safe_builtins,
            '__name__': '__repl__',
        }
        
        # Merge user state into namespace
        self._namespace.update(self._state)
    
    def _read_chunk_wrapper(self, chunk_id: str):
        """Wrapper for read_chunk."""
        from repl_functions import read_chunk
        return read_chunk(chunk_id, self.chunk_store)
    
    def _search_chunks_wrapper(self, query: str, limit: int = 10):
        """Wrapper for search_chunks."""
        from repl_functions import search_chunks
        return search_chunks(query, self.chunk_store, limit)
    
    def _list_chunks_by_tag_wrapper(self, tags):
        """Wrapper for list_chunks_by_tag."""
        from repl_functions import list_chunks_by_tag
        # Handle single tag or list of tags
        if isinstance(tags, str):
            return list_chunks_by_tag(tags, self.chunk_store)
        elif isinstance(tags, list):
            return list_chunks_by_tag(tags, self.chunk_store)
        return []
    
    def _get_linked_chunks_wrapper(self, chunk_id: str, link_type: str = None):
        """Wrapper for get_linked_chunks."""
        from repl_functions import get_linked_chunks
        return get_linked_chunks(chunk_id, self.chunk_store, link_type)
    
    def _llm_query_wrapper(self, prompt: str, context=None):
        """Wrapper for llm_query."""
        with self._lock:
            self._iteration_count += 1
            if self._iteration_count > self.max_iterations:
                raise MaxIterationsError(
                    f"Maximum iterations ({self.max_iterations}) exceeded"
                )
        
        # Build full prompt with context
        full_prompt = prompt
        if context:
            context_str = "\n".join(f"{k}: {v}" for k, v in context.items())
            full_prompt = f"Context:\n{context_str}\n\nPrompt:\n{prompt}"
        
        # Call LLM
        try:
            response = self.llm_client.complete(full_prompt)
            # Track cost if available
            if hasattr(response, 'cost_usd'):
                self._total_cost += response.cost_usd
            return response.text if hasattr(response, 'text') else str(response)
        except AttributeError:
            # Simple mock case
            return str(self.llm_client.complete(full_prompt))
    
    def _final_wrapper(self, answer) -> None:
        """Wrapper for FINAL."""
        if self._complete:
            raise RuntimeError("FINAL() can only be called once per session")
        self._result = answer
        self._complete = True
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state dictionary (user-defined variables only)."""
        return self._state.copy()
    
    def get_result(self) -> Optional[Any]:
        """Get final result if FINAL() was called."""
        return self._result
    
    def is_complete(self) -> bool:
        """Check if FINAL() has been called."""
        return self._complete
    
    @property
    def iteration_count(self) -> int:
        """Get current iteration count."""
        return self._iteration_count
    
    def get_cost(self) -> float:
        """Get total cost accumulated."""
        return self._total_cost
    
    def get_output(self) -> str:
        """Get captured output."""
        return "\n".join(self._output)
    
    def get_stderr(self) -> str:
        """Get captured stderr."""
        return "\n".join(self._stderr)
    
    def clear_output(self):
        """Clear captured output."""
        self._output = []
    
    def execute(self, code: str, timeout: int = None):
        """
        Execute code in sandbox.
        
        Args:
            code: Python code to execute
            timeout: Optional timeout override
            
        Returns:
            Result of the last expression or None
            
        Raises:
            RuntimeError: If called after FINAL()
            SandboxViolation: If code violates sandbox
        """
        if self._complete:
            raise RuntimeError("REPL already complete")
        
        if not code or not code.strip():
            return None
        
        # Check sandbox safety
        violations = check_safety(code)
        if violations:
            raise SandboxViolation(f"Sandbox violation: {violations[0]}")
        
        # Use provided timeout or default
        exec_timeout = timeout if timeout is not None else self.timeout_seconds
        
        start_time = time.time()
        
        # Capture stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            
            # Try to eval as expression first
            try:
                compiled = compile(code, '<repl>', 'eval')
                result = eval(compiled, self._namespace)
                
                # Check timeout
                if time.time() - start_time > exec_timeout:
                    raise TimeoutError(f"Execution exceeded {exec_timeout} seconds")
                
                # Capture output
                self._output.append(stdout_capture.getvalue())
                self._stderr.append(stderr_capture.getvalue())
                
                return result
            except SyntaxError:
                # Not an expression, try exec
                pass
            
            # Compile and execute as statements
            compiled = compile(code, '<repl>', 'exec')
            exec(compiled, self._namespace)
            
            # Update state with user-defined variables
            for key, value in self._namespace.items():
                if not key.startswith('_') and key not in ('__builtins__', '__name__'):
                    self._state[key] = value
            
            # Check timeout
            if time.time() - start_time > exec_timeout:
                raise TimeoutError(f"Execution exceeded {exec_timeout} seconds")
            
            # Capture output
            self._output.append(stdout_capture.getvalue())
            self._stderr.append(stderr_capture.getvalue())
            
            return None
            
        except TimeoutError:
            raise
        except Exception as e:
            # Re-raise as-is for tests to catch
            raise
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def retrieve(self, query=None, max_iterations=None) -> Optional[Any]:
        """Get the final answer if complete."""
        return self._result if self._complete else None
    
    def reset(self):
        """Reset session state."""
        self._state = {}
        self._iteration_count = 0
        self._total_cost = 0.0
        self._result = None
        self._complete = False
        self._output = []
        self._stderr = []
        self._setup_namespace()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.reset()
        return False
