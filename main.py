"""Main CLI application for the Flarion Universal Ping Tester."""

import asyncio
import sys
from typing import Dict, List, Optional

from Classes.OperatingSystem import OperatingSystem
from Classes.Server import Server


class PingTesterApp:
    """Main application class for the ping tester CLI."""

    JSON_FILES: Dict[str, str] = {"datacenter": "datacenters.json", "game": "game.json"}

    def __init__(self):
        """Initialize the application."""
        self.os_info = OperatingSystem()
        self.server = Server()

    async def initialize(self) -> None:
        """Initialize the application and display system information."""
        self.os_info.display_system_info()
        await asyncio.sleep(1)

    def display_main_menu(self) -> None:
        """Display the main menu options."""
        print("\nWelcome to Flarion Universal Ping Tester CLI!")
        print("\nSelect an option:")
        print("1. List Internet Service Providers")
        print("2. List Game Servers")
        print("3. Custom")
        print("4. Exit")

    def handle_datacenter_menu(self) -> None:
        """Handle the datacenter/ISP selection menu."""
        countries = self.server.get_countries(self.JSON_FILES["datacenter"])

        if not countries:
            print("No countries available in data.")
            return

        print("\nAvailable Countries:")
        for i, country in enumerate(countries, 1):
            print(f"{i}. {country}")

        try:
            country_choice = input("Select a country (number): ")
            country_index = int(country_choice) - 1

            if 0 <= country_index < len(countries):
                selected_country = countries[country_index]
                self.handle_server_selection(selected_country)
            else:
                print("Invalid country selection.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    def handle_server_selection(self, country: str) -> None:
        """Handle server selection for a given country.

        Args:
            country: Selected country name
        """
        servers = self.server.get_servers_by_country(
            self.JSON_FILES["datacenter"], country
        )

        if not servers:
            print(f"No servers found in {country}.")
            return

        print(f"\nServers in {country}:")
        for i, server in enumerate(servers, 1):
            print(f"{i}. {server.name} ({server.ip_address})")

        server_choice = input("Select a server to ping (number) or 'back': ")

        if server_choice.lower() != "back":
            try:
                server_index = int(server_choice) - 1
                if 0 <= server_index < len(servers):
                    selected_server = servers[server_index]
                    print(f"\nPinging {selected_server.name}...")
                    selected_server.ping()
                    
                    input("\nPress Enter to return to main menu...")
                    return
                else:
                    print("Invalid server selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def handle_game_menu(self) -> None:
        """Handle the game servers menu."""
        print("Game servers feature is not implemented yet.")

    def handle_custom_menu(self) -> None:
        """Handle the custom ping menu."""
        print("Custom ping feature is not implemented yet.")

    def handle_exit(self) -> None:
        """Handle application exit."""
        print("Thank you for using Flarion Universal Ping Tester!")
        self._show_exit_notification()

    def _show_exit_notification(self) -> None:
        """Show system notification on exit if available."""
        try:
            if sys.platform == "win32":
                self._show_windows_notification()
            else:
                self._show_linux_notification()
        except ImportError:
            pass

    def _show_windows_notification(self) -> None:
        """Show Windows toast notification."""
        try:
            import win10toast

            toaster = win10toast.ToastNotifier()
            toaster.show_toast(
                "Flarion Ping Tester", "Exiting application...", duration=3
            )
        except ImportError:
            pass

    def _show_linux_notification(self) -> None:
        """Show Linux desktop notification."""
        try:
            import subprocess

            subprocess.run(
                [
                    "notify-send",
                    "Flarion Ping Tester CLI",
                    "Exiting application by user request...",
                ],
                check=False,
            )
        except Exception:
            pass

    async def run(self) -> None:
        """Run the main application loop."""
        await self.initialize()

        while True:
            try:
                self.display_main_menu()
                choice = input("Enter your choice: ").lower()

                if choice in {"1", "datacenter"}:
                    self.handle_datacenter_menu()
                elif choice in {"2", "game"}:
                    self.handle_game_menu()
                elif choice in {"3", "custom"}:
                    self.handle_custom_menu()
                elif choice in {"4", "exit"}:
                    self.handle_exit()
                    break
                else:
                    print("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\n\nExiting application...")
                self.handle_exit()
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


async def main() -> None:
    """Main entry point for the application."""
    app = PingTesterApp()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
