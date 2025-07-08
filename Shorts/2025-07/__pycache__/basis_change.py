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


class BasisChangeFull(ShortFormTemplate):
    HOOK_TEXT    = "One Transformation"
    CONTENT_TEXT = None
    OUTRO_TEXT   = "Two Different Basis"

    # helper – centralnie wyrównane etykiety macierzy
    def basis_matrix(self, label_tex: str, matrix_vals):
        #   B_{i} =  [ … ]  (wyrównanie pionowe)
        lbl = MathTex(label_tex, color=LIGHT_TEXT)
        mat = Matrix(matrix_vals).set_color(LIGHT_TEXT)
        lbl.next_to(mat, LEFT, buff=0.25)
        return VGroup(lbl, mat)

    def construct(self):
        super().construct()

        # ─── 1. statyczna biała kratka ───
        static_grid = NumberPlane(
            background_line_style={
                "stroke_color": LIGHT_TEXT,
                "stroke_opacity": 0.15,
                "stroke_width": 0.6,
            },
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            axis_config={"stroke_opacity": 0},
        )
        self.add(static_grid)

        # ─── 2. dynamiczna fioletowa kratka ───
        dyn_grid = NumberPlane(
            background_line_style={
                "stroke_color": PURPLE,
                "stroke_opacity": 0.25,
                "stroke_width": 4,
            },
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            axis_config={"stroke_opacity": 0},
        )

        # ─── 3. osie + kwadrat ───
        x_axis = Arrow(LEFT * 7, RIGHT * 7, color=LIGHT_TEXT, stroke_width=2)
        y_axis = Arrow(DOWN * 5,  UP * 5,  color=LIGHT_TEXT, stroke_width=2)
        square = (
            Square(2)
            .set_fill(LIGHT_TEXT, opacity=0.2)
            .set_stroke(ORANGE, width=4)
        )

        dyn = VGroup(dyn_grid, x_axis, y_axis, square)
        self.play(FadeIn(dyn), run_time=1)

        self.wait(0.5)

        # ─── 4. pokaż A ───
        A_vals  = [[1.5, 0.5], [0.2, 1.2]]
        A = self.basis_matrix(r"A =", A_vals).to_edge(UP, buff=-3.5)
        A.set_z_index(5)
        self.play(FadeIn(A, shift=UP * 0.5), run_time=1)

        self.wait(0.5)

        # ─── 5. Apply A ───
        self.play(ApplyMatrix(A_vals, dyn), run_time=3.0)

        self.wait(0.5)

        # ─── 6. obrót → new basis ───
        self.play(Rotate(dyn, PI/4), run_time=2.0)

        self.wait(0.5)

        # ─── 7. wprowadź B ───
        B_vals  = [[1.7, 0.0], [-0.3, 1.0]]
        B = self.basis_matrix(r"B =", B_vals).move_to(A)
        B.set_z_index(5)
        self.play(FadeOut(A), run_time=0.5)
        self.play(FadeIn(B),  run_time=0.5)

        self.wait(0.5)

        # ─── 8. Apply B ───
        self.play(ApplyMatrix(B_vals, dyn), run_time=3.0)
        self.wait(0.5)


        # ─── Stage 3 · krok 1 ───
        # (1) przesuwamy istniejącą macierz B w prawo
        B.generate_target()
        B.target.shift(RIGHT * 3)

        # (2) odtwarzamy macierz A po lewej
        A_left = self.basis_matrix(r"A =", A_vals)
        A_left.set_z_index(5)                    # nad maską
        A_left.next_to(B.target, LEFT, buff=1.2) # ta sama wysokość

        # (3) jednoczesna animacja
        self.play(
            MoveToTarget(B,  run_time=1.0),
            FadeIn(A_left,   run_time=1.0)
        )

        self.wait(0.5)

        # ─── Stage 3 – Krok 2 ───
        self.play(
            FadeOut(dyn),          # dyn_grid + x_axis + y_axis + square
            FadeOut(static_grid),  # biała statyczna kratka
            run_time=0.5
        )

        self.wait(0.5)             # stała pauza



