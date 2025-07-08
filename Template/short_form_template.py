"""
Short‑form video template for Eigenmind.

Features
--------
• 9:16 (1080×1920) at 60 fps, dark background.
• Uses core palette (#121212, #E0E0E0, #FF5722, #673AB7).
• λ‑logo watermark always on top (PNG or SVG fallback).
• Optional hook / content / outro placeholders – skip by leaving the text empty.
"""

import os
from manim import (
    config,
    SVGMobject,
    ImageMobject,
    Text,
    Write,
    UR,
    UP,
    DOWN,
)

# ---------------------------------------------------------------------------
# Global render config
# ---------------------------------------------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.background_color = DARK_BG = "#121212"

# Palette
LIGHT_TEXT = "#E0E0E0"
ORANGE = "#FF5722"
PURPLE = "#673AB7"

# ---------------------------------------------------------------------------
# Base scene class
# ---------------------------------------------------------------------------
try:
    from base_scene import BaseScene  # project‑specific utilities (if present)
except ImportError:
    from manim import Scene as BaseScene


class ShortFormTemplate(BaseScene):
    """Base for all Eigenmind TikTok / Shorts clips.

    Override class attributes `HOOK_TEXT`, `CONTENT_TEXT`, `OUTRO_TEXT` in subclasses
    (or set them to an empty string/None to suppress that placeholder).
    """


    # Default placeholders – override per‑scene
    HOOK_TEXT: str | None = "Hook goes here"
    CONTENT_TEXT: str | None = "Main content here"
    OUTRO_TEXT: str | None = "Call to Action"

    def construct(self):
        
        # -------------------------------------------------------------------
        # λ‑watermark (always visible, brand colours preserved)
        # -------------------------------------------------------------------
        base_dir = os.path.dirname(__file__)
        # prefer PNG (supports gradient fill), fallback to SVG
        logo_path_png = os.path.join(base_dir, "logo.png")
        logo_path_svg = os.path.join(base_dir, "logo.svg")
        logo = (
            ImageMobject(logo_path_png)
            if os.path.isfile(logo_path_png)
            else SVGMobject(logo_path_svg)
        )
        logo.scale(0.15)
        logo.to_edge(DOWN, buff=-7)
        self.add_foreground_mobject(logo)
        
        # -------------------------------------------------------------------
        # Optional placeholders (displayed only if text provided)
        # -------------------------------------------------------------------
        if self.HOOK_TEXT:
            hook = Text(self.HOOK_TEXT, font_size=100, color=LIGHT_TEXT)
            hook.to_edge(UP, buff=-6)
            self.play(Write(hook, run_time=0.8))
            y_cursor = hook

        if self.CONTENT_TEXT:
            content = Text(self.CONTENT_TEXT, font_size=50, color=LIGHT_TEXT)
            content.next_to(y_cursor, DOWN, buff=0.5)
            self.play(Write(content, run_time=1))
            y_cursor = content

        if self.OUTRO_TEXT:
            outro = Text(self.OUTRO_TEXT, font_size=56, color=ORANGE)
            outro.to_edge(DOWN, buff=-4)
            self.play(Write(outro, run_time=0.8))

        self.wait(0.2)