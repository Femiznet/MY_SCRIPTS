"""Build and configuration script for the package distribution."""

import subprocess
import platform

def verify_installation(commands:list[str], use_path:str) -> str | None:
    """Verifies tool installation at the specified path.

    Parameters:
        commands (list[str]): Specific command to run based on the tool.
        use_path (str): Path to run the command.

    Returns:
        str | None: The version string if installed, otherwise None.
    """

    for command in commands:
        cmd = command.split()

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            cwd=use_path,
        )

        if result.returncode == 0:
            return result.stdout

import platform

def get_os():
    """Get the name of the host operating system.

    Returns:
        str: Name of the operating system (e.g., 'Windows', 'Linux', 'Darwin').
    """
    return platform.system()

