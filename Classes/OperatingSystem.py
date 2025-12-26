"""Operating system detection and information display module."""

import os
import platform
import subprocess
from typing import Optional

try:
    from colorama import Fore, Style
except ImportError:
    # Fallback if colorama is not available
    class _ColorFallback:
        GREEN = ""
        YELLOW = ""
    
    class _StyleFallback:
        RESET_ALL = ""
    
    Fore = _ColorFallback()
    Style = _StyleFallback()


class OperatingSystem:
    """Provides operating system information and detection capabilities."""
    
    def __init__(self):
        """Initialize OS information."""
        self.name = os.name
        self.info = self._get_system_info()
        self.distro = self._get_distribution_info()

    def _get_system_info(self) -> object:
        """Get system information based on the operating system.
        
        Returns:
            Object containing system information
        """
        if self.name == "posix":
            return os.uname()
        else:
            # Create a simple object for non-POSIX systems
            return type("SystemInfo", (), {"release": platform.release()})()

    def _get_distribution_info(self) -> str:
        """Get distribution information for the current operating system.
        
        Returns:
            Distribution name and version string
        """
        if self.name == "posix":
            return self._get_linux_distro()
        elif self.name == "nt":
            return self._get_windows_info()
        else:
            return "Unknown"

    def _get_linux_distro(self) -> str:
        """Get Linux distribution information.
        
        Returns:
            Linux distribution name
        """
        try:
            result = subprocess.check_output(["lsb_release", "-i", "-s"], timeout=5)
            return result.decode().strip()
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return "Unknown Linux"

    def _get_windows_info(self) -> str:
        """Get Windows version information.
        
        Returns:
            Windows version string
        """
        try:
            version = platform.version()
            build_number = self._extract_build_number(version)
            
            if build_number >= 22000:
                return f"Windows 11 (Build {build_number})"
            else:
                return f"Windows 10 (Build {build_number})"
        except Exception:
            return "Windows"

    def _extract_build_number(self, version: str) -> int:
        """Extract build number from version string.
        
        Args:
            version: Version string from platform.version()
            
        Returns:
            Build number as integer, or 0 if extraction fails
        """
        try:
            return int(version.split(".")[-1])
        except (ValueError, IndexError):
            return 0

    def get_kernel_version(self) -> str:
        """Get kernel version information.
        
        Returns:
            Kernel version string
        """
        if self.name == "posix":
            try:
                result = subprocess.check_output(["uname", "-r"], timeout=5)
                return result.decode().strip()
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                return getattr(self.info, "release", "Unknown")
        elif self.name == "nt":
            return self._get_windows_info()
        else:
            return "Unknown"

    def display_system_info(self) -> None:
        """Display formatted system information to the console."""
        print("System Information:")
        print(
            f"{Fore.GREEN}Operating System Family: {Fore.YELLOW}{self.name}{Style.RESET_ALL}"
        )
        
        kernel_info = self.get_kernel_version()
        print(f"{Fore.GREEN}Kernel: {Fore.YELLOW}{kernel_info}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}Distribution: {Fore.YELLOW}{self.distro}{Style.RESET_ALL}")