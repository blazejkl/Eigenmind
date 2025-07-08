from __future__ import annotations
import sys, pathlib
from manim import *

# ─────────────────────────────────────────────────────────────────────────────
# Import template utilities
# ─────────────────────────────────────────────────────────────────────────────
THIS_FILE = pathlib.Path(__file__).resolve()
root = THIS_FILE
while root != root.parent:
    if (root / "Template").is_dir():
        break
    root = root.parent
if str(root) not in sys.path:
    sys.path.append(str(root))

from Template.short_form_template import ShortFormTemplate, LIGHT_TEXT, PURPLE, ORANGE  # noqa: E402

class BasisChangeStage1(ShortFormTemplate):
    HOOK_TEXT    = "One transformation"
    CONTENT_TEXT = None
    OUTRO_TEXT   = None

    def construct(self):
        super().construct()

        # 1) Siatka tła w kolorze fioletowym
        plane = NumberPlane(
            background_line_style={"stroke_color": PURPLE, "stroke_opacity": 0.2},
            axis_config={"include_ticks": False, "stroke_color": PURPLE},
            x_range=[-8, 8, 1],  # wydłużona oś X
            y_range=[-5, 5, 1],
        )
        self.play(FadeIn(plane), run_time=0.5)

        # 2) Oś OX (bez granic ekranu) w off-white
        x_axis = plane.x_axis.set_color(LIGHT_TEXT)
        x_axis.add_tip(tip_length=0.2)
        # 3) Oś OY z grotem w off-white
        y_axis = plane.y_axis.set_color(LIGHT_TEXT)
        y_axis.add_tip(tip_length=0.2)
        self.add(x_axis, y_axis)

        # 4) Kwadrat: fill off-white, stroke pomarańczowe
        square = Square(side_length=2)
        square.set_fill(LIGHT_TEXT, opacity=0.2)
        square.set_stroke(ORANGE, width=4)
        self.play(FadeIn(square), run_time=0.5)

        # 5) Pojawienie się macierzy A w off-white
        A = [[1.5, 0.5],
             [0.2, 1.2]]
        mat = Matrix(A).to_corner(UR).set_color(LIGHT_TEXT)
        self.play(FadeIn(mat, shift=UP * 0.5), run_time=0.5)
        self.wait(0.2)

        # 6) Zastosowanie A do siatki i kwadratu
        self.play(
            ApplyMatrix(A, plane),
            ApplyMatrix(A, square),
            run_time=1.5,
        )

        # 7) Hold na beat
        self.wait(0.5)
