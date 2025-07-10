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
    VGroup,
    Rectangle,
    SVGMobject,
    ImageMobject,
    Text,
    Write,
    UR,
    UP,
    DOWN,
    LEFT,
    RIGHT,
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

# ─── konfiguracja wysokości masek (w jednostkach sceny) ───
MASK_UP    = 8    # ile jednostek “od góry” zasłonić
MASK_DOWN  = 8    # ile od dołu

def _add_frame_mask(scene):
    """
    Dodaje dwie czarne ramki:
    ▬ górną wysokości MASK_UP,
    ▬ dolną wysokości MASK_DOWN,
    przyklejone do krawędzi ekranu.
    Szerokość = pełny kadr.
    """
    color = DARK_BG           # kolor tła kanału / sceny

    top_mask = Rectangle(
        width=50, height=MASK_UP,
        fill_color=color, fill_opacity=1, stroke_opacity=0
    ).to_edge(UP, buff=-9)

    bottom_mask = Rectangle(
        width=50, height=MASK_DOWN,
        fill_color=color, fill_opacity=1, stroke_opacity=0
    ).to_edge(DOWN, buff=-9)

    # warstwa nad animacją, pod LOGO/HOOK
    masks = VGroup(top_mask, bottom_mask).set_z_index(1)
    scene.add(masks)

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

        # maska nad wszystkimi obiektami podklasy,
        # ale pod hook / content / logo
        _add_frame_mask(self)
        
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
        logo.set_z_index(5)
        self.add_foreground_mobject(logo)
        
        # -------------------------------------------------------------------
        # Optional placeholders (displayed only if text provided)
        # -------------------------------------------------------------------
        if self.HOOK_TEXT:
            hook = Text(self.HOOK_TEXT, font_size=90, color=LIGHT_TEXT)
            hook.to_edge(UP, buff=-6)
            hook.set_z_index(5)
            self.play(Write(hook, run_time=0.8))
            self.hook_obj = hook        #  <──  zapisz referencję
            y_cursor = hook

        if self.CONTENT_TEXT:
            content = Text(self.CONTENT_TEXT, font_size=50, color=LIGHT_TEXT)
            content.next_to(y_cursor, DOWN, buff=0.5)
            content.set_z_index(5)
            self.play(Write(content, run_time=1))
            self.content_obj = content
            y_cursor = content

        if self.OUTRO_TEXT:
            outro = Text(self.OUTRO_TEXT, font_size=50, color=ORANGE)
            outro.to_edge(DOWN, buff=-4)
            outro.set_z_index(5)
            self.outro_obj = outro
            self.play(Write(outro, run_time=0.8))

        self.wait(0.2)