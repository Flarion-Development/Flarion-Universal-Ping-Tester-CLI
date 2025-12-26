"""Main CLI application for the Flarion Universal Ping Tester."""

import asyncio
import os
import sys
from typing import Dict, List, Optional

from Classes.Locale import Locale
from Classes.OperatingSystem import OperatingSystem
from Classes.Server import Server


class PingTesterApp:
    """Main application class for the ping tester CLI."""

    JSON_FILES: Dict[str, str] = {"datacenter": "datacenters.json", "game": "game.json"}

    def __init__(self):
        """Initialize the application."""
        self.os_info = OperatingSystem()
        self.server = Server()
        self.locale = Locale()
    
    def clear_console(self) -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    async def initialize(self) -> None:
        """Initialize the application and display system information."""
        self.clear_console()
        self.os_info.display_system_info(locale=self.locale)
        await asyncio.sleep(1)

    def display_main_menu(self) -> None:
        """Display the main menu options."""
        self.clear_console()
        print(f"\n{self.locale.get('welcome')}")
        print(f"\n{self.locale.get('select_option')}")
        print(f"1. {self.locale.get('list_isp')}")
        print(f"2. {self.locale.get('list_game')}")
        print(f"3. {self.locale.get('custom')}")
        print(f"4. {self.locale.get('exit')}")

    def handle_datacenter_menu(self) -> None:
        """Handle the datacenter/ISP selection menu."""
        countries = self.server.get_countries(self.JSON_FILES["datacenter"])

        if not countries:
            print(self.locale.get("no_countries"))
            input(f"\n{self.locale.get('press_enter')}")
            return

        self.clear_console()
        print(f"\n{self.locale.get('available_countries')}")
        for i, country in enumerate(countries, 1):
            print(f"{i}. {country}")

        try:
            country_choice = input(self.locale.get("select_country") + " ")
            country_index = int(country_choice) - 1

            if 0 <= country_index < len(countries):
                selected_country = countries[country_index]
                self.handle_server_selection(selected_country)
            else:
                print(self.locale.get("invalid_country"))
                input(f"\n{self.locale.get('press_enter')}")

        except ValueError:
            print(self.locale.get("invalid_input"))
            input(f"\n{self.locale.get('press_enter')}")

    def handle_server_selection(self, country: str) -> None:
        """Handle server selection for a given country.

        Args:
            country: Selected country name
        """
        servers = self.server.get_servers_by_country(
            self.JSON_FILES["datacenter"], country
        )

        if not servers:
            print(self.locale.get("no_servers", country=country))
            input(f"\n{self.locale.get('press_enter')}")
            return

        self.clear_console()
        print(f"\n{self.locale.get('servers_in', country=country)}:")
        for i, server in enumerate(servers, 1):
            print(f"{i}. {server.name} ({server.ip_address})")

        server_choice = input(self.locale.get("select_server") + " ")

        if server_choice.lower() != "back":
            try:
                server_index = int(server_choice) - 1
                if 0 <= server_index < len(servers):
                    selected_server = servers[server_index]
                    self.clear_console()
                    print(
                        f"\n{self.locale.get('pinging', server_name=selected_server.name)}..."
                    )
                    selected_server.ping()

                    input(f"\n{self.locale.get('press_enter')}")
                    return
                else:
                    print(self.locale.get("invalid_server"))
            except ValueError:
                print(self.locale.get("invalid_input"))

    def handle_game_menu(self) -> None:
        """Handle the game servers menu."""
        self.clear_console()
        print(self.locale.get("game_not_implemented"))
        input(f"\n{self.locale.get('press_enter')}")

    def handle_custom_menu(self) -> None:
        """Handle the custom ping menu."""
        self.clear_console()
        print(self.locale.get("custom_not_implemented"))
        input(f"\n{self.locale.get('press_enter')}")

    def handle_exit(self) -> None:
        """Handle application exit."""
        print(self.locale.get("thank_you"))
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
                choice = input(self.locale.get("enter_choice") + " ").lower()

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
                    print(self.locale.get("invalid_choice"))

            except KeyboardInterrupt:
                print(f"\n\n{self.locale.get('exiting')}")
                self.handle_exit()
                break
            except Exception as e:
                print(self.locale.get("unexpected_error", error=e))


async def main() -> None:
    """Main entry point for the application."""
    app = PingTesterApp()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
