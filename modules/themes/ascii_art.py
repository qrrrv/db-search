# -*- coding: utf-8 -*-
"""
ASCII Art Generator - Beautiful banners and graphics
"""

try:
    from art import text2art, art, FONT_NAMES
    ART_AVAILABLE = True
except ImportError:
    ART_AVAILABLE = False

try:
    from pyfiglet import Figlet, FigletFont
    PYFIGLET_AVAILABLE = True
except ImportError:
    PYFIGLET_AVAILABLE = False


class ASCIIArt:
    """ASCII Art generator for banners and decorations"""
    
    # Pre-made ASCII art banners
    BANNERS = {
        'default': r"""
    ____  ____     _____ _____    _    ____   ____ _   _ 
   |  _ \| __ )   / ___|| ____|  / \  |  _ \ / ___| | | |
   | | | |  _ \   \___ \|  _|   / _ \ | |_) | |   | |_| |
   | |_| | |_) |   ___) | |___ / ___ \|  _ <| |___|  _  |
   |____/|____/   |____/|_____/_/   \_\_| \_\\____|_| |_|
""",
        'compact': r"""
  ___  ___   ___ ___   _   ___  ___ _  _ 
 |   \| _ ) / __| __| /_\ | _ \/ __| || |
 | |) | _ \ \__ \ _| / _ \|   / (__| __ |
 |___/|___/ |___/___/_/ \_\_|_\\___|_||_|
""",
        'box': r"""
+--------------------------------------------------+
|     DATABASE SEARCH TOOL v2.0 PRO                |
|     Fast Multi-threaded Search Engine            |
+--------------------------------------------------+
""",
        'cyber': r"""
 ╔═══════════════════════════════════════════════════╗
 ║  ██████╗ ██████╗     ███████╗███████╗ █████╗ ██████╗ ██╗  ██╗  ║
 ║  ██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔══██╗██║  ██║  ║
 ║  ██║  ██║██████╔╝    ███████╗█████╗  ███████║██████╔╝███████║  ║
 ║  ██║  ██║██╔══██╗    ╚════██║██╔══╝  ██╔══██║██╔══██╗██╔══██║  ║
 ║  ██████╔╝██████╔╝    ███████║███████╗██║  ██║██║  ██║██║  ██║  ║
 ║  ╚═════╝ ╚═════╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ║
 ╚═══════════════════════════════════════════════════╝
""",
        'simple': r"""
=======================================================
          D B   S E A R C H   T O O L   v2.0
=======================================================
""",
        'hacker': r"""
 [*]==========================================[*]
 |    ___  ___   __               _           |
 |   / _ \/ _ ) / _\___  ___ _ __| |_         |
 |  / // / _  | \ \/ -_)/ _ \ '_/| ' \        |
 | /____/____/ /___|___|\_,_|_|  |_||_|       |
 |                                            |
 [*]==========================================[*]
""",
        'matrix': r"""
    .___________. __    __   _______     
    |           ||  |  |  | |   ____|    
    `---|  |----`|  |__|  | |  |__       
        |  |     |   __   | |   __|      
        |  |     |  |  |  | |  |____     
        |__|     |__|  |__| |_______|    
                                         
   .___  ___.      ___   .___________..______       __  ___   ___ 
   |   \/   |     /   \  |           ||   _  \     |  | \  \ /  / 
   |  \  /  |    /  ^  \ `---|  |----`|  |_)  |    |  |  \  V  /  
   |  |\/|  |   /  /_\  \    |  |     |      /     |  |   >   <   
   |  |  |  |  /  _____  \   |  |     |  |\  \----.|  |  /  .  \  
   |__|  |__| /__/     \__\  |__|     | _| `._____||__| /__/ \__\ 
""",
    }
    
    # Decorative elements
    DECORATIONS = {
        'line_single': '-' * 60,
        'line_double': '=' * 60,
        'line_star': '*' * 60,
        'line_dash': '- ' * 30,
        'line_dot': '.' * 60,
        'box_top': '+' + '-' * 58 + '+',
        'box_bottom': '+' + '-' * 58 + '+',
        'arrow_right': '-->',
        'arrow_left': '<--',
        'bullet': '*',
        'check': '[+]',
        'cross': '[-]',
        'info': '[i]',
        'warning': '[!]',
        'question': '[?]',
    }
    
    # Status indicators
    STATUS = {
        'ok': '[OK]',
        'error': '[ERROR]',
        'warning': '[WARN]',
        'info': '[INFO]',
        'debug': '[DEBUG]',
        'success': '[SUCCESS]',
        'fail': '[FAIL]',
        'loading': '[...]',
        'done': '[DONE]',
    }
    
    @classmethod
    def generate_banner(cls, text: str = "DB SEARCH", font: str = 'slant') -> str:
        """Generate ASCII art banner"""
        # Try ART library first
        if ART_AVAILABLE:
            try:
                return text2art(text, font=font)
            except:
                pass
        
        # Try pyfiglet
        if PYFIGLET_AVAILABLE:
            try:
                fig = Figlet(font=font)
                return fig.renderText(text)
            except:
                try:
                    fig = Figlet(font='slant')
                    return fig.renderText(text)
                except:
                    pass
        
        # Fallback to pre-made
        return cls.BANNERS.get('default', text)
    
    @classmethod
    def get_banner(cls, style: str = 'default') -> str:
        """Get pre-made banner"""
        return cls.BANNERS.get(style, cls.BANNERS['default'])
    
    @classmethod
    def list_fonts(cls) -> list:
        """List available fonts"""
        fonts = []
        
        if PYFIGLET_AVAILABLE:
            try:
                fonts.extend(FigletFont.getFonts()[:20])  # First 20 fonts
            except:
                pass
        
        if ART_AVAILABLE:
            try:
                fonts.extend(list(FONT_NAMES)[:20])
            except:
                pass
        
        if not fonts:
            fonts = ['slant', 'banner', 'doom', 'small', 'standard']
        
        return list(set(fonts))
    
    @classmethod
    def get_decoration(cls, name: str) -> str:
        """Get decorative element"""
        return cls.DECORATIONS.get(name, '')
    
    @classmethod
    def get_status(cls, name: str) -> str:
        """Get status indicator"""
        return cls.STATUS.get(name, '[?]')
    
    @classmethod
    def create_box(cls, text: str, width: int = 60) -> str:
        """Create a box around text"""
        lines = text.split('\n')
        max_len = min(max(len(line) for line in lines), width - 4)
        
        result = ['+' + '-' * (max_len + 2) + '+']
        for line in lines:
            padded = line[:max_len].ljust(max_len)
            result.append(f'| {padded} |')
        result.append('+' + '-' * (max_len + 2) + '+')
        
        return '\n'.join(result)
    
    @classmethod
    def create_header(cls, text: str, char: str = '=', width: int = 60) -> str:
        """Create a header with decorative lines"""
        padding = (width - len(text) - 2) // 2
        line = char * width
        header_line = char * padding + ' ' + text + ' ' + char * padding
        
        if len(header_line) < width:
            header_line += char
        
        return f"{line}\n{header_line}\n{line}"
    
    @classmethod
    def progress_bar_ascii(cls, progress: float, width: int = 30) -> str:
        """Create ASCII progress bar"""
        filled = int(width * progress)
        empty = width - filled
        
        bar = '[' + '#' * filled + '-' * empty + ']'
        percent = f' {progress * 100:.1f}%'
        
        return bar + percent