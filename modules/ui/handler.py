# -*- coding: utf-8 -*-
"""
Input Handler - Enhanced user input
"""

from typing import Optional, List, Any

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.styles import Style
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.validation import Validator, ValidationError
    from prompt_toolkit.history import FileHistory
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class InputHandler:
    """Enhanced input handling with autocompletion and validation"""
    
    def __init__(self, theme: dict = None, history_file: str = '.search_history'):
        self.theme = theme or {
            'primary': 'cyan',
            'secondary': 'yellow',
            'success': 'green',
            'error': 'red'
        }
        self.history_file = history_file
        
        if RICH_AVAILABLE:
            self.console = Console()
        
        if PROMPT_TOOLKIT_AVAILABLE:
            self.style = Style.from_dict({
                'prompt': f'ansi{self.theme["primary"]}',
                'input': 'ansibright{}'.format(self.theme.get('success', 'green')),
            })
            try:
                self.history = FileHistory(history_file)
            except:
                self.history = None
    
    def get_input(self, prompt_text: str = "> ", 
                  completer_words: List[str] = None,
                  validator: callable = None,
                  default: str = "") -> str:
        """Get user input with optional completion and validation"""
        
        if PROMPT_TOOLKIT_AVAILABLE:
            return self._get_prompt_toolkit_input(
                prompt_text, completer_words, validator, default
            )
        elif RICH_AVAILABLE:
            return self._get_rich_input(prompt_text, default)
        else:
            return self._get_simple_input(prompt_text, default)
    
    def _get_prompt_toolkit_input(self, prompt_text: str, 
                                   completer_words: List[str],
                                   validator: callable,
                                   default: str) -> str:
        """Get input using prompt_toolkit"""
        completer = None
        if completer_words:
            completer = WordCompleter(completer_words, ignore_case=True)
        
        pt_validator = None
        if validator:
            class CustomValidator(Validator):
                def validate(self, document):
                    text = document.text
                    if not validator(text):
                        raise ValidationError(message='Invalid input')
            pt_validator = CustomValidator()
        
        try:
            result = prompt(
                HTML(f'<b>{prompt_text}</b>'),
                style=self.style,
                completer=completer,
                validator=pt_validator,
                history=self.history,
                default=default
            )
            return result
        except (KeyboardInterrupt, EOFError):
            return ""
    
    def _get_rich_input(self, prompt_text: str, default: str) -> str:
        """Get input using Rich"""
        return Prompt.ask(
            f"[{self.theme['primary']}]{prompt_text}[/]",
            default=default
        )
    
    def _get_simple_input(self, prompt_text: str, default: str) -> str:
        """Get simple input"""
        if default:
            prompt_text = f"{prompt_text} [{default}]: "
        result = input(prompt_text)
        return result if result else default
    
    def get_search_query(self) -> str:
        """Get search query with examples"""
        examples = [
            "123456789 (Telegram ID)",
            "+79001234567 (Phone)",
            "John Smith (Name)",
            "example@mail.com (Email)",
            "@username (Username)"
        ]
        
        if RICH_AVAILABLE:
            self.console.print(f"\n[{self.theme['info']}]Enter search query:[/]")
            self.console.print(f"[{self.theme['dim']}]Examples:[/]")
            for ex in examples:
                self.console.print(f"  [{self.theme['dim']}]- {ex}[/]")
            self.console.print()
        else:
            print("\nEnter search query:")
            print("Examples:")
            for ex in examples:
                print(f"  - {ex}")
            print()
        
        return self.get_input("Search: ")
    
    def confirm(self, message: str, default: bool = False) -> bool:
        """Get yes/no confirmation"""
        if RICH_AVAILABLE:
            return Confirm.ask(
                f"[{self.theme['secondary']}]{message}[/]",
                default=default
            )
        else:
            suffix = " [Y/n]" if default else " [y/N]"
            response = input(message + suffix + ": ").strip().lower()
            
            if not response:
                return default
            return response in ['y', 'yes', 'da', 'd']
    
    def select_option(self, options: List[str], message: str = "Select option") -> Optional[int]:
        """Select from a list of options"""
        if RICH_AVAILABLE:
            self.console.print(f"\n[{self.theme['primary']}]{message}:[/]")
            for i, opt in enumerate(options, 1):
                self.console.print(f"  [{self.theme['success']}]{i}[/]. {opt}")
        else:
            print(f"\n{message}:")
            for i, opt in enumerate(options, 1):
                print(f"  {i}. {opt}")
        
        try:
            choice = int(self.get_input("\nChoice: "))
            if 1 <= choice <= len(options):
                return choice - 1
        except ValueError:
            pass
        
        return None
    
    def get_number(self, prompt_text: str, min_val: int = None, 
                   max_val: int = None, default: int = None) -> Optional[int]:
        """Get a number with validation"""
        if default is not None:
            prompt_text = f"{prompt_text} [{default}]"
        
        while True:
            try:
                result = self.get_input(f"{prompt_text}: ")
                
                if not result and default is not None:
                    return default
                
                num = int(result)
                
                if min_val is not None and num < min_val:
                    if RICH_AVAILABLE:
                        self.console.print(f"[{self.theme['error']}]Value must be >= {min_val}[/]")
                    else:
                        print(f"Value must be >= {min_val}")
                    continue
                
                if max_val is not None and num > max_val:
                    if RICH_AVAILABLE:
                        self.console.print(f"[{self.theme['error']}]Value must be <= {max_val}[/]")
                    else:
                        print(f"Value must be <= {max_val}")
                    continue
                
                return num
                
            except ValueError:
                if RICH_AVAILABLE:
                    self.console.print(f"[{self.theme['error']}]Please enter a valid number[/]")
                else:
                    print("Please enter a valid number")
    
    def wait_for_key(self, message: str = "Press Enter to continue..."):
        """Wait for user to press a key"""
        if RICH_AVAILABLE:
            self.console.print(f"\n[{self.theme['dim']}]{message}[/]")
        else:
            print(f"\n{message}")
        input()
