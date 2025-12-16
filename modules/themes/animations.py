# -*- coding: utf-8 -*-
"""
Animations and Spinners for Console UI
"""

import sys
import time
import threading
from typing import Optional, List

# Try importing animation libraries
try:
    from halo import Halo
    HALO_AVAILABLE = True
except ImportError:
    HALO_AVAILABLE = False

try:
    from alive_progress import alive_bar
    ALIVE_PROGRESS_AVAILABLE = True
except ImportError:
    ALIVE_PROGRESS_AVAILABLE = False

try:
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.console import Console
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from blessed import Terminal
    BLESSED_AVAILABLE = True
except ImportError:
    BLESSED_AVAILABLE = False


class Animations:
    """Console animations and spinners"""
    
    # Spinner frame sets
    SPINNERS = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['|', '/', '-', '\\'],
        'arrows': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'bounce': ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃', '▂'],
        'blocks': ['▖', '▘', '▝', '▗'],
        'pulse': ['◐', '◓', '◑', '◒'],
        'snake': ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'],
        'wave': ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈'],
        'loading': ['⡀', '⡄', '⡆', '⡇', '⣇', '⣧', '⣷', '⣿'],
        'search': ['◜', '◠', '◝', '◞', '◡', '◟'],
        'braille': ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈'],
        'clock': ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗'],
        'moon': ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'],
        'earth': ['🌍', '🌎', '🌏'],
        'star': ['✦', '✧', '⭐', '✧', '✦'],
        'fire': ['🔥', '🧯'],
        'water': ['💧', '💦', '🌊'],
    }
    
    # Progress bar styles
    PROGRESS_STYLES = {
        'default': {'fill': '█', 'empty': '░', 'left': '[', 'right': ']'},
        'blocks': {'fill': '▓', 'empty': '░', 'left': '[', 'right': ']'},
        'dots': {'fill': '●', 'empty': '○', 'left': '(', 'right': ')'},
        'arrows': {'fill': '▶', 'empty': '▷', 'left': '[', 'right': ']'},
        'solid': {'fill': '■', 'empty': '□', 'left': '|', 'right': '|'},
        'smooth': {'fill': '━', 'empty': '─', 'left': '┫', 'right': '┣'},
    }
    
    def __init__(self):
        self._spinner_running = False
        self._spinner_thread = None
        self._current_spinner = 'dots'
    
    def spinner_start(self, text: str = "Loading...", spinner_type: str = 'dots'):
        """Start a spinner animation"""
        if HALO_AVAILABLE:
            self._halo_spinner = Halo(text=text, spinner='dots')
            self._halo_spinner.start()
            return
        
        self._spinner_running = True
        self._current_spinner = spinner_type
        
        def spin():
            frames = self.SPINNERS.get(spinner_type, self.SPINNERS['dots'])
            idx = 0
            while self._spinner_running:
                frame = frames[idx % len(frames)]
                sys.stdout.write(f'\r{frame} {text}')
                sys.stdout.flush()
                idx += 1
                time.sleep(0.1)
        
        self._spinner_thread = threading.Thread(target=spin)
        self._spinner_thread.start()
    
    def spinner_stop(self, final_text: str = None):
        """Stop the spinner"""
        if HALO_AVAILABLE and hasattr(self, '_halo_spinner'):
            if final_text:
                self._halo_spinner.succeed(final_text)
            else:
                self._halo_spinner.stop()
            return
        
        self._spinner_running = False
        if self._spinner_thread:
            self._spinner_thread.join()
        
        if final_text:
            sys.stdout.write(f'\r{final_text}\n')
        else:
            sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()
    
    def progress_bar(self, iterable, total: int = None, desc: str = "Progress"):
        """Create a progress bar wrapper for iteration"""
        if ALIVE_PROGRESS_AVAILABLE:
            with alive_bar(total or len(iterable), title=desc) as bar:
                for item in iterable:
                    yield item
                    bar()
            return
        
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
            ) as progress:
                task = progress.add_task(desc, total=total or len(iterable))
                for item in iterable:
                    yield item
                    progress.update(task, advance=1)
            return
        
        # Fallback simple progress
        total = total or len(iterable)
        for i, item in enumerate(iterable):
            progress = (i + 1) / total
            bar_width = 30
            filled = int(bar_width * progress)
            bar = '[' + '█' * filled + '░' * (bar_width - filled) + ']'
            sys.stdout.write(f'\r{desc}: {bar} {progress*100:.1f}%')
            sys.stdout.flush()
            yield item
        print()
    
    def simple_progress(self, current: int, total: int, desc: str = "", 
                       style: str = 'default', width: int = 30) -> str:
        """Generate simple progress bar string"""
        s = self.PROGRESS_STYLES.get(style, self.PROGRESS_STYLES['default'])
        
        progress = current / total if total > 0 else 0
        filled = int(width * progress)
        empty = width - filled
        
        bar = s['left'] + s['fill'] * filled + s['empty'] * empty + s['right']
        percent = f' {progress * 100:.1f}%'
        
        if desc:
            return f'{desc}: {bar}{percent}'
        return f'{bar}{percent}'
    
    def typing_effect(self, text: str, delay: float = 0.03):
        """Print text with typing effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def flash_text(self, text: str, times: int = 3, delay: float = 0.2):
        """Flash text on screen"""
        for _ in range(times):
            sys.stdout.write(f'\r{text}')
            sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write('\r' + ' ' * len(text))
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write(f'\r{text}\n')
    
    def countdown(self, seconds: int, message: str = "Starting in"):
        """Show countdown timer"""
        for i in range(seconds, 0, -1):
            sys.stdout.write(f'\r{message} {i}...')
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write(f'\r{message} Go!     \n')
    
    def matrix_rain(self, duration: float = 2.0, width: int = 60):
        """Simple Matrix-style rain effect"""
        import random
        chars = '01'
        start_time = time.time()
        
        while time.time() - start_time < duration:
            line = ''.join(random.choice(chars) for _ in range(width))
            print(line)
            time.sleep(0.05)
    
    @classmethod
    def get_spinner_types(cls) -> List[str]:
        """Get list of available spinner types"""
        return list(cls.SPINNERS.keys())
    
    @classmethod
    def get_progress_styles(cls) -> List[str]:
        """Get list of available progress bar styles"""
        return list(cls.PROGRESS_STYLES.keys())