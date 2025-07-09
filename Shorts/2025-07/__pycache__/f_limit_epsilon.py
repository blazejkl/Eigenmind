from __future__ import annotations
import sys, pathlib
from manim import *

# ───────────── import szablonu ─────────────
THIS_FILE = pathlib.Path(__file__).resolve()
root = THIS_FILE
while root != root.parent:
    if (root / "Template").is_dir():
        break
    root = root.parent
template_dir = root / "Template"
if str(template_dir) not in sys.path:
    sys.path.append(str(template_dir))

from short_form_template import ShortFormTemplate, LIGHT_TEXT, PURPLE, ORANGE
# ───────────────────────────────────────────

class FLiimitEpsilon(ShortFormTemplate):
    HOOK_TEXT    = "Limit of a function"
    CONTENT_TEXT = None
    OUTRO_TEXT   = None

    def construct(self):
        super().construct()
