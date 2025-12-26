"""Server module for managing server data and ping operations."""

import json
import os
import subprocess
from pathlib import Path
from typing import List, Optional


class Server:
    """Represents a server with name and IP address for ping testing."""

    def __init__(self, name: Optional[str] = None, ip_address: Optional[str] = None):
        """Initialize a server instance.

        Args:
            name: Server display name
            ip_address: Server IP address for pinging
        """
        self.name = name
        self.ip_address = ip_address

    def load_data_from_json(self, json_file: str) -> dict:
        """Load and parse JSON data from the Data directory.

        Args:
            json_file: Name of the JSON file in the Data directory

        Returns:
            Parsed JSON data as dictionary

        Raises:
            FileNotFoundError: If the JSON file doesn't exist
            json.JSONDecodeError: If the JSON file is malformed
        """
        data_path = Path("Data") / json_file
        with open(data_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_countries(self, json_file: str) -> List[str]:
        """Extract unique countries from the JSON data.

        Args:
            json_file: Name of the JSON file containing server data

        Returns:
            Sorted list of unique country names
        """
        try:
            data = self.load_data_from_json(json_file)
            countries = {
                server_data.get("country", "Unknown") or "Unknown"
                for server_data in data.get("datacenter", {}).values()
            }
            return sorted([str(country) for country in countries])
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Error reading countries from {json_file}: {e}")
            return []

    def get_servers_by_country(self, json_file: str, country: str) -> List["Server"]:
        """Get all servers located in the specified country.

        Args:
            json_file: Name of the JSON file containing server data
            country: Country name to filter servers by

        Returns:
            List of Server objects in the specified country
        """
        try:
            data = self.load_data_from_json(json_file)
            servers = []

            for server_data in data.get("datacenter", {}).values():
                if server_data.get("country", "").lower() == country.lower():
                    server = Server(
                        name=server_data.get("name", "Unknown"),
                        ip_address=server_data.get("ip", "0.0.0.0"),
                    )
                    servers.append(server)

            return servers
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Error reading servers from {json_file}: {e}")
            return []

    def ping(self) -> bool:
        """Execute ping command to the server's IP address.

        Returns:
            True if ping was successful, False otherwise
        """
        if not self.ip_address:
            print(f"No IP address configured for server: {self.name}")
            return False

        if self.ip_address == "undefined" or self.ip_address == "0.0.0.0":
            print(f"IP address is undefined for server: {self.name}")
            return False

        try:
            ping_command = self._build_ping_command()
            result = subprocess.run(
                ping_command, capture_output=True, text=True, timeout=30
            )
            print(result.stdout)

            if result.returncode == 0:
                return True
            else:
                print(f"Ping failed for {self.name}: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"Ping timeout for {self.name}")
            return False
        except Exception as e:
            print(f"Error pinging {self.name}: {e}")
            return False

    def _build_ping_command(self) -> List[str]:
        """Build platform-specific ping command.

        Returns:
            List of command arguments for ping

        Raises:
            NotImplementedError: If the operating system is not supported
        """
        if os.name == "posix":
            return ["ping", "-c", "6", self.ip_address]
        elif os.name == "nt":
            return ["ping", "-n", "6", self.ip_address]
        else:
            raise NotImplementedError(f"Unsupported operating system: {os.name}")
