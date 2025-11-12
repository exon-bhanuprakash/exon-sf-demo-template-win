#!/usr/bin/env python3
"""
Verify that the Windows fix will work before running the build
"""

import sys
import os
import shutil
import subprocess

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("VERIFYING WINDOWS FIX")
print("=" * 60)
print()

# Test 1: Find npm directory
print("✓ Test 1: Finding npm directory...")
npm_dir = os.path.join(os.environ.get('APPDATA', ''), 'npm')
if os.path.exists(npm_dir):
    print(f"  ✓ Found: {npm_dir}")
else:
    print(f"  ✗ NOT FOUND: {npm_dir}")
    print("  Try running: npm config get prefix")
    sys.exit(1)

# Test 2: Check if claude.cmd exists
print()
print("✓ Test 2: Checking if claude.cmd exists...")
claude_cmd = os.path.join(npm_dir, 'claude.cmd')
if os.path.exists(claude_cmd):
    print(f"  ✓ Found: {claude_cmd}")
else:
    print(f"  ✗ NOT FOUND: {claude_cmd}")
    sys.exit(1)

# Test 3: Add npm to PATH
print()
print("✓ Test 3: Adding npm to PATH...")
original_path = os.environ.get('PATH', '')
os.environ['PATH'] = f"{npm_dir};{original_path}"
print(f"  ✓ Added {npm_dir} to PATH")

# Test 4: Verify shutil.which finds claude
print()
print("✓ Test 4: Checking if 'claude' is found in PATH...")
claude_path = shutil.which('claude')
if claude_path:
    print(f"  ✓ Found: {claude_path}")
else:
    print("  ✗ NOT FOUND")
    sys.exit(1)

# Test 5: Test executing claude with subprocess
print()
print("✓ Test 5: Testing subprocess execution...")
try:
    result = subprocess.run(
        ['claude', '--version'],
        capture_output=True,
        text=True,
        shell=True,
        timeout=5
    )
    if result.returncode == 0:
        version = result.stdout.strip()
        print(f"  ✓ Success: {version}")
    else:
        print(f"  ✗ Failed with code {result.returncode}")
        print(f"  stderr: {result.stderr}")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 6: Verify claude-agent-sdk is installed
print()
print("✓ Test 6: Checking claude-agent-sdk...")
try:
    from claude_agent_sdk import ClaudeAgentOptions
    print("  ✓ claude-agent-sdk is installed")
except ImportError:
    print("  ✗ claude-agent-sdk NOT installed")
    print("  Run: pip install claude-agent-sdk")
    sys.exit(1)

# Test 7: Try creating ClaudeAgentOptions without cli_path
print()
print("✓ Test 7: Testing ClaudeAgentOptions...")
try:
    from pathlib import Path
    options = ClaudeAgentOptions(
        permission_mode='bypassPermissions',
        cwd=str(Path.cwd()),
        setting_sources=["project"]
    )
    print("  ✓ ClaudeAgentOptions created successfully")
    print("  ✓ SDK will find 'claude' in PATH automatically")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# All tests passed
print()
print("=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print()
print("The Windows fix is working correctly.")
print("You can now run:")
print()
print("  python resume.py \"C:\\00_All_Work\\exon-sf-tech-demo\"")
print()
print("Or start a fresh build:")
print()
print("  python start.py")
print()
print("=" * 60)
