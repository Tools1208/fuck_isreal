import os
import sys
import importlib
import pkgutil
from colorama import Fore, Style, init
import pyfiglet
from datetime import datetime
import logging
from typing import Dict, Any

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    filename='tool.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ToolInterface:
    """Base class for all tools"""
    name: str = "Unnamed Tool"
    description: str = "No description available"
    author: str = "Anonymous"
    version: str = "1.0"

    def execute(self) -> None:
        """Main execution method for the tool"""
        raise NotImplementedError("Tool execution not implemented")

class ToolManager:
    """Manages tool discovery and execution"""
    def __init__(self):
        self.tools: Dict[str, ToolInterface] = {}
        self.load_tools()

    def load_tools(self) -> None:
        """Dynamically load all tools from tools directory"""
        try:
            # Dynamically import all modules in the tools package
            for _, module_name, _ in pkgutil.iter_modules(['tools']):
                if module_name.startswith('_'):
                    continue
                    
                # Import the module
                module = importlib.import_module(f'tools.{module_name}')
                
                # Find Tool class in the module
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, ToolInterface) and attribute != ToolInterface:
                        tool_instance = attribute()
                        tool_id = f"{len(self.tools)+1:02d}"
                        self.tools[tool_id] = tool_instance
                        logging.info(f"Loaded tool: {tool_instance.name} ({tool_id})")
        except Exception as e:
            logging.error(f"Error loading tools: {str(e)}")
            print(f"{Fore.RED}[!] Failed to load tools - Check tool.log for details")

    def get_tool(self, tool_id: str) -> ToolInterface:
        """Get tool by ID"""
        return self.tools.get(tool_id)

class MainApp:
    """Main application class"""
    BANNER = pyfiglet.figlet_format("Fuck_Isreal", font="slant")
    CREDITS = f"""{Fore.RED}
Fuck Isreal By  : Anonymous Jordan Team 
Link  : https://t.me/AnonymousJordan
{Style.RESET_ALL}"""
    
    def __init__(self):
        self.tool_manager = ToolManager()
        self.show_splash()

    def show_splash(self) -> None:
        """Display the splash screen"""
        os.system('clear')
        print(self.BANNER)
        print(self.CREDITS)
        print(f"{Fore.CYAN}System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.MAGENTA}Loaded {len(self.tool_manager.tools)} tools\n")

    def display_menu(self) -> None:
        """Display the main menu"""
        print(f"{Fore.GREEN}{'='*40}")
        print(f"{Fore.YELLOW}Main Menu")
        print(f"{Fore.GREEN}{'='*40}")
        
        for tool_id, tool in self.tool_manager.tools.items():
            print(f"{Fore.CYAN}[{tool_id}] {tool.name}")
            print(f"{Fore.WHITE}{'-'*40}")
            print(f"Description: {tool.description}")
            print(f"Author: {tool.author}")
            print(f"Version: {tool.version}\n")
        
        print(f"{Fore.RED}[99] Exit")
        print(f"{Fore.YELLOW}[98] Reload Tools")
        print(f"{Fore.BLUE}[97] Help")

    def run(self) -> None:
        """Main application loop"""
        while True:
            try:
                self.show_splash()
                self.display_menu()
                
                choice = input(f"\n{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")
                
                if choice == '99':
                    self.exit_app()
                elif choice == '98':
                    self.tool_manager.load_tools()
                    print(f"{Fore.GREEN}[+] Tools reloaded successfully!")
                    input("\nPress Enter to continue...")
                elif choice == '97':
                    self.show_help()
                elif choice in self.tool_manager.tools:
                    self.execute_tool(choice)
                else:
                    print(f"{Fore.RED}[!] Invalid choice! Please try again.")
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}[!] Program interrupted by user.")
                self.exit_app()
            except Exception as e:
                logging.error(f"Main loop error: {str(e)}")
                print(f"{Fore.RED}[!] An unexpected error occurred. Check tool.log for details")
                input("\nPress Enter to continue...")

    def execute_tool(self, tool_id: str) -> None:
        """Execute selected tool"""
        tool = self.tool_manager.get_tool(tool_id)
        if not tool:
            print(f"{Fore.RED}[!] Tool {tool_id} not found!")
            return
            
        try:
            print(f"\n{Fore.GREEN}[+] Executing: {tool.name}")
            print(f"{Fore.WHITE}{'-'*40}")
            tool.execute()
        except NotImplementedError:
            print(f"{Fore.RED}[!] Tool execution not implemented")
        except Exception as e:
            logging.error(f"Error executing {tool.name}: {str(e)}")
            print(f"{Fore.RED}[!] Error executing tool: {str(e)}")
        finally:
            input("\nPress Enter to return to menu...")

    def show_help(self) -> None:
        """Display help information"""
        help_text = f"""
{Fore.CYAN}Help Documentation:
{Fore.GREEN}1. {Fore.YELLOW}Tool Selection:
   - Enter the tool number to execute
   - Tools are dynamically loaded from /tools directory

{Fore.GREEN}2. {Fore.YELLOW}Special Commands:
   - 99: Exit the application
   - 98: Reload tools (use after adding new tools)
   - 97: Show this help message

{Fore.GREEN}3. {Fore.YELLOW}Logging:
   - All actions are logged to tool.log
   - Errors are recorded with timestamps

{Fore.GREEN}4. {Fore.YELLOW}Development:
   - Create new tools by adding Python files to /tools
   - Implement ToolInterface class for automatic detection
"""
        print(help_text)
        input("\nPress Enter to return to menu...")

    def exit_app(self) -> None:
        """Graceful exit handler"""
        print(f"{Fore.RED}\n[+] Exiting application...")
        logging.info("Application exited by user")
        sys.exit(0)

if __name__ == "__main__":
    try:
        app = MainApp()
        app.run()
    except Exception as e:
        logging.critical(f"Application failed to start: {str(e)}")
        print(f"{Fore.RED}[!] Critical error: {str(e)}")
        sys.exit(1)
