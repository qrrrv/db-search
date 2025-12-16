# -*- coding: utf-8 -*-
"""
Animated Themes System
15 Beautiful Themes with Animations
"""

from .theme_loader import ThemeLoader, AnimatedTheme

# Theme names
THEME_NAMES = [
    'default', 'hacker', 'ocean', 'fire', 'purple',
    'cyberpunk', 'neon', 'sunset', 'arctic', 'dracula',
    'retro', 'forest', 'galaxy', 'blood', 'gold'
]

__all__ = ['ThemeLoader', 'AnimatedTheme', 'THEME_NAMES']