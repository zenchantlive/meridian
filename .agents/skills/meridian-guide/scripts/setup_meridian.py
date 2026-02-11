#!/usr/bin/env python3
"""
MERIDIAN Brain Setup Script

Initializes a new MERIDIAN Brain installation with proper directory structure
and configuration files.

Usage:
    python setup_meridian.py [target_directory]

If no directory is specified, uses current directory.
"""

import os
import sys
import argparse
from pathlib import Path


def create_directory_structure(base_path: Path):
    """Create MERIDIAN Brain directory structure."""
    
    directories = [
        # Core memory storage
        "brain/memory",
        "brain/memory/tags",
        "brain/memory/links",
        
        # Scripts
        "brain/scripts",
        
        # Original MERIDIAN structure
        "brain/personalities",
        "brain/sliders",
        "brain/gauges",
        
        # Memory management
        "memory",
        "memory/adr",
        
        # Configuration
        ".specify/memory",
        ".claude/commands",
        ".cursor/commands",
        
        # Logs and temp
        "logs",
        "history",
    ]
    
    for dir_path in directories:
        full_path = base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {dir_path}")


def create_constitution(base_path: Path, project_name: str):
    """Create initial constitution file."""
    
    constitution_content = f"""# {project_name} Constitution

> MERIDIAN Brain Enhanced - Intelligent agent operating system with RLM-based memory

**Version:** 1.0.0
**Created:** {__import__('datetime').datetime.now().strftime("%Y-%m-%d")}

---

## Core Principles

### I. Memory-First
Every significant interaction should be remembered. When in doubt, store it.

### II. Progressive Enhancement
Start with BASE personality, enhance based on context.

### III. Confidence Scoring
Always indicate certainty levels. High confidence (>0.9) for facts, lower for interpretations.

---

## Default Configuration

**Personality Mode:** BASE
**Auto-remember:** True
**Confidence Threshold:** 0.7

---

## Workflows

### Memory Creation
1. Identify if information is worth remembering
2. Choose appropriate type (preference, fact, pattern, decision, note)
3. Tag with relevant categories
4. Set confidence based on certainty

### Context Retrieval
1. Search for relevant memories before responding
2. Consider linked chunks for additional context
3. Weight by confidence and recency

---

## Project-Specific Notes

(Add your project-specific guidance here)
"""
    
    constitution_path = base_path / ".specify/memory/constitution.md"
    constitution_path.write_text(constitution_content)
    print(f"  Created: {constitution_path.relative_to(base_path)}")


def create_agents_md(base_path: Path):
    """Create AGENTS.md entry point."""
    
    agents_content = """# Agent Instructions

**Read:** `.specify/memory/constitution.md`

That file is your source of truth for this project.

## Quick Commands

- **Remember**: Use `remember_operation.remember()`
- **Search**: Use `chunk_store.list_chunks(tags=[...])`
- **Switch Mode**: Read `brain/personalities/[MODE].md`
- **System Status**: `chunk_store.get_stats()`
"""
    
    agents_path = base_path / "AGENTS.md"
    agents_path.write_text(agents_content)
    print(f"  Created: {agents_path.relative_to(base_path)}")


def create_claude_md(base_path: Path):
    """Create CLAUDE.md entry point."""
    
    claude_content = """# Agent Instructions

**Read:** `.specify/memory/constitution.md`

That file is your source of truth for this project.
"""
    
    claude_path = base_path / "CLAUDE.md"
    claude_path.write_text(claude_content)
    print(f"  Created: {claude_path.relative_to(base_path)}")


def create_gitignore(base_path: Path):
    """Create .gitignore for MERIDIAN Brain."""
    
    gitignore_content = """# MERIDIAN Brain - Git Ignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Local configuration (optional - remove if you want to track)
# .specify/memory/constitution.md

# Temporary files
.rlm_temp/
.temp/
tmp/
"""
    
    gitignore_path = base_path / ".gitignore"
    gitignore_path.write_text(gitignore_content)
    print(f"  Created: {gitignore_path.relative_to(base_path)}")


def create_readme(base_path: Path, project_name: str):
    """Create project README."""
    
    readme_content = f"""# {project_name}

Powered by MERIDIAN Brain Enhanced - an intelligent agent operating system.

## Features

- **RLM Memory System**: Persistent, queryable memory with graph linking
- **Personality Modes**: Pre-configured behavioral profiles
- **Configuration Sliders**: Fine-tune agent behavior
- **Secure REPL**: Sandbox for recursive LLM execution

## Quick Start

```python
from brain.scripts import ChunkStore, RememberOperation

# Initialize memory
store = ChunkStore("brain/memory")
remember = RememberOperation(store)

# Create a memory
result = remember.remember(
    content="User prefers dark mode",
    conversation_id="setup",
    tags=["preference", "ui"],
    confidence=0.95
)
```

## Documentation

- Setup Guide: See skill `meridian-guide`
- Architecture: `brain/scripts/` and `brain/MEMORY_SCHEMA.md`
- Personalities: `brain/personalities/*.md`
- Sliders: `brain/sliders/*.md`

## Project Configuration

- Constitution: `.specify/memory/constitution.md`
- Agent Instructions: `AGENTS.md`

---

Built with MERIDIAN Brain Enhanced
"""
    
    readme_path = base_path / "README.md"
    readme_path.write_text(readme_content)
    print(f"  Created: {readme_path.relative_to(base_path)}")


def verify_installation(base_path: Path) -> bool:
    """Verify MERIDIAN Brain can be imported."""
    
    print("\\nVerifying installation...")
    
    # Check if brain/scripts exists (should be copied from template or installed)
    brain_scripts = base_path / "brain" / "scripts"
    if not brain_scripts.exists():
        print("  ⚠️  Warning: brain/scripts/ not found")
        print("     Copy from meridian repository or install: pip install meridian-brain")
        return False
    
    # Try importing
    try:
        sys.path.insert(0, str(base_path))
        from brain.scripts import ChunkStore, RememberOperation
        print("  ✓ Core components import successfully")
        return True
    except ImportError as e:
        print(f"  ⚠️  Import error: {e}")
        print("     Ensure MERIDIAN Brain is installed: pip install -e .")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Set up MERIDIAN Brain Enhanced in a directory"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Target directory (default: current directory)"
    )
    parser.add_argument(
        "--name",
        default="My MERIDIAN Project",
        help="Project name"
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip installation verification"
    )
    
    args = parser.parse_args()
    
    base_path = Path(args.directory).resolve()
    print(f"Setting up MERIDIAN Brain in: {base_path}")
    print(f"Project name: {args.name}\\n")
    
    # Create structure
    print("Creating directory structure...")
    create_directory_structure(base_path)
    
    # Create files
    print("\\nCreating configuration files...")
    create_constitution(base_path, args.name)
    create_agents_md(base_path)
    create_claude_md(base_path)
    create_gitignore(base_path)
    create_readme(base_path, args.name)
    
    # Verify
    if not args.skip_verify:
        verify_installation(base_path)
    
    print("\\n" + "="*60)
    print("Setup complete!")
    print("="*60)
    print(f"\\nNext steps:")
    print(f"  1. Review: {base_path / '.specify/memory/constitution.md'}")
    print(f"  2. Edit: {base_path / 'README.md'} with project details")
    print(f"  3. Install: pip install -e . (if MERIDIAN is a dependency)")
    print(f"  4. Test: python -c \"from brain.scripts import ChunkStore\"")
    print(f"\\nFor full documentation, use the meridian-guide skill.")


if __name__ == "__main__":
    main()

