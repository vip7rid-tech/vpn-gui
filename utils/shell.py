"""
shell.py - Subprocess wrapper for executing system commands.

Provides a unified interface for running shell commands
with proper error handling and output capture.
"""

import subprocess
from typing import Tuple


def run_command(cmd: list) -> Tuple[str, str]:
    """
    Execute a system command and return its output.

    Args:
        cmd: List of command arguments (e.g., ['wg-quick', 'up', 'wg0'])

    Returns:
        Tuple of (stdout, stderr) as strings.
        On success, stderr will be empty.
        On failure, stdout may be empty and stderr will contain the error message.
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30  # Prevent hanging on stalled commands
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", f"Command timed out: {' '.join(cmd)}"
    except FileNotFoundError:
        return "", f"Command not found: {cmd[0]}"
    except PermissionError:
        return "", f"Permission denied: {' '.join(cmd)}"
    except Exception as e:
        return "", f"Unexpected error: {str(e)}"
