#!/usr/bin/env python3
import asyncio
import sys

async def test():
    print("Testing .bat wrapper with asyncio (like the SDK uses)...")
    try:
        proc = await asyncio.create_subprocess_exec(
            r'builder\claude-wrapper.bat',
            '--version',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        print(f"Return code: {proc.returncode}")
        print(f"stdout: {stdout.decode().strip()}")
        if stderr:
            print(f"stderr: {stderr.decode().strip()}")

        if proc.returncode == 0:
            print("\n✓ SUCCESS: .bat wrapper works with asyncio!")
            sys.exit(0)
        else:
            print("\n✗ FAILED: .bat wrapper returned non-zero code")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)

asyncio.run(test())
