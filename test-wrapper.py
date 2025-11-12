#!/usr/bin/env python3
"""Test if the Python wrapper works with subprocess"""

import sys
import subprocess
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("Testing Claude wrapper...")
print("=" * 60)

wrapper_path = Path("builder/claude-wrapper.py")
python_exe = sys.executable

print(f"Python: {python_exe}")
print(f"Wrapper: {wrapper_path.absolute()}")
print()

# Test 1: Run with list command
print("Test 1: Running with subprocess.run([python, wrapper, --version])")
try:
    result = subprocess.run(
        [python_exe, str(wrapper_path), "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"  ✓ Success: {result.stdout.strip()}")
    else:
        print(f"  ✗ Failed: code {result.returncode}")
        print(f"  stderr: {result.stderr}")
except Exception as e:
    print(f"  ✗ Error: {e}")

print()

# Test 2: Run with asyncio (like the SDK does)
print("Test 2: Running with asyncio.create_subprocess_exec")
import asyncio

async def test_async():
    try:
        proc = await asyncio.create_subprocess_exec(
            python_exe, str(wrapper_path), "--version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            print(f"  ✓ Success: {stdout.decode().strip()}")
        else:
            print(f"  ✗ Failed: code {proc.returncode}")
            print(f"  stderr: {stderr.decode()}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

asyncio.run(test_async())

print()
print("=" * 60)
print("If both tests passed, the wrapper will work with the SDK!")
