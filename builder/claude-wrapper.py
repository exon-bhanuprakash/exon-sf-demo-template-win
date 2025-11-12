#!/usr/bin/env python3
"""
Claude Code CLI Wrapper for Windows
This wrapper ensures claude.cmd can be executed properly by the claude-agent-sdk
Handles stdin/stdout/stderr passthrough for interactive sessions
"""

import sys
import subprocess
import os

# Find the actual claude.cmd
CLAUDE_CMD = r"C:\Users\DELL\AppData\Roaming\npm\claude.cmd"

if not os.path.exists(CLAUDE_CMD):
    # Try to find it dynamically
    import shutil
    claude_path = shutil.which('claude.cmd')
    if claude_path:
        CLAUDE_CMD = claude_path
    else:
        print(f"Error: Could not find claude.cmd", file=sys.stderr)
        sys.exit(1)

# Execute claude.cmd with all arguments passed to this wrapper
# Pass through stdin/stdout/stderr for interactive sessions
try:
    # On Windows, we need shell=True to execute .cmd files
    # Pass stdin/stdout/stderr directly for full interactivity
    proc = subprocess.Popen(
        [CLAUDE_CMD] + sys.argv[1:],
        shell=True,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    # Wait for completion
    returncode = proc.wait()
    sys.exit(returncode)

except Exception as e:
    print(f"Error executing Claude Code CLI: {e}", file=sys.stderr)
    sys.exit(1)
