#!/usr/bin/env python3
"""
Ralph Loop for Windows - Python implementation

Based on Geoffrey Huntley's Ralph Wiggum methodology:
https://github.com/fstandhartinger/ralph-wiggum

Usage:
    python scripts/ralph-loop.py           # Build mode (unlimited)
    python scripts/ralph-loop.py 20        # Build mode (max 20 iterations)
    python scripts/ralph-loop.py plan      # Planning mode
"""

import sys
import os
import subprocess
import re
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
LOG_DIR = PROJECT_DIR / "logs"
SPECS_DIR = PROJECT_DIR / "specs"
CONSTITUTION = PROJECT_DIR / ".specify" / "memory" / "constitution.md"
PROMPT_BUILD = PROJECT_DIR / "PROMPT_build.md"

def log(message: str):
    """Print timestamped log message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_specs():
    """Find all spec directories."""
    if not SPECS_DIR.exists():
        return []
    specs = []
    for spec_dir in sorted(SPECS_DIR.iterdir()):
        if spec_dir.is_dir():
            spec_file = spec_dir / "spec.md"
            if spec_file.exists():
                specs.append((spec_dir.name, spec_file))
    return specs

def find_incomplete_spec():
    """Find the first incomplete spec."""
    specs = get_specs()
    for name, path in specs:
        content = path.read_text(encoding='utf-8')
        # Check if spec has a completion marker
        if '<promise>DONE</promise>' not in content:
            return name, path
    return None, None

def run_iteration(iteration: int, max_iterations: int = 0) -> bool:
    """Run one Ralph iteration. Returns True if DONE found."""
    log(f"=== Iteration {iteration} ===")
    
    # Find work
    spec_name, spec_path = find_incomplete_spec()
    if not spec_path:
        log("No incomplete specs found!")
        return True
    
    log(f"Working on: {spec_name}")
    
    # Check for beads if no specs
    log("Run 'bd ready' manually to see bead status")
    
    # Read constitution and prompt
    constitution_text = ""
    if CONSTITUTION.exists():
        constitution_text = CONSTITUTION.read_text(encoding='utf-8')
    
    prompt_text = ""
    if PROMPT_BUILD.exists():
        prompt_text = PROMPT_BUILD.read_text(encoding='utf-8')
    
    spec_content = spec_path.read_text(encoding='utf-8')
    
    # Print instructions for the agent
    log("=" * 60)
    log("RALPH INSTRUCTIONS:")
    log("=" * 60)
    print("\n" + prompt_text)
    print("\n" + "=" * 60)
    log(f"CURRENT SPEC: {spec_name}")
    log("=" * 60)
    print("\n" + spec_content)
    print("\n" + "=" * 60)
    log("TASK:")
    log("=" * 60)
    print(f"""
1. Implement the requirements in {spec_name}
2. Run all tests
3. Verify acceptance criteria
4. Commit and push changes
5. Add '<promise>DONE</promise>' to {spec_path} when complete

DO NOT output 'DONE' until truly complete.
""")
    
    # In real Ralph, this would invoke the AI agent
    # For now, we just provide the context and wait
    log("Ready for implementation.")
    log("Run your implementation, then add '<promise>DONE</promise>' to the spec file.")
    
    return False

def main():
    """Main Ralph loop."""
    args = sys.argv[1:]
    
    mode = "build"
    max_iterations = 0
    
    for arg in args:
        if arg == "plan":
            mode = "plan"
        elif arg.isdigit():
            max_iterations = int(arg)
    
    log(f"Ralph Loop starting - Mode: {mode}, Max iterations: {max_iterations or 'unlimited'}")
    
    if mode == "plan":
        log("Planning mode not yet implemented in Python version")
        log("Use: bd ready  # to see available work")
        return
    
    iteration = 0
    while True:
        iteration += 1
        
        if max_iterations > 0 and iteration > max_iterations:
            log(f"Reached max iterations ({max_iterations})")
            break
        
        # Run one iteration
        done = run_iteration(iteration, max_iterations)
        
        if done:
            log("All work complete!")
            break
        
        # In autonomous mode, we would check for DONE marker
        # For manual mode, just run once
        log("Iteration complete. Check spec for '<promise>DONE</promise>' marker.")
        break

if __name__ == "__main__":
    main()
