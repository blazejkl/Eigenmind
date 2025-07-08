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
    HOOK_TEXT    = "Matrix Similarity"
    CONTENT_TEXT = None
    OUTRO_TEXT   = "One Transformation - Two Different Bases"

    # helper – centralnie wyrównane etykiety macierzy
    def basis_matrix(self, label_tex: str, matrix_vals):
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
                "stroke_width": 1,
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
                "stroke_width": 6,
            },
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            axis_config={"stroke_opacity": 0},
        )

        # ─── 3. osie + kwadrat ───
        x_axis = Arrow(LEFT * 7, RIGHT * 7, color=LIGHT_TEXT, stroke_width=4)
        y_axis = Arrow(DOWN * 5,  UP * 5,  color=LIGHT_TEXT, stroke_width=4)
        square = (
            Square(2)
            .set_fill(LIGHT_TEXT, opacity=0.2)
            .set_stroke(ORANGE, width=8)
        )

        dyn = VGroup(dyn_grid, x_axis, y_axis, square)
        self.play(FadeIn(dyn), run_time=0.5)

        self.wait(0.2)

        # ─── 4. pokaż A ───
        A_vals  = [[1.5, 0.5], [0.2, 1.2]]
        A = self.basis_matrix(r"A =", A_vals).to_edge(UP, buff=-3.75)
        A.set_z_index(5)
        self.play(FadeIn(A, shift=UP * 0.5), run_time=0.5)

        self.wait(0.2)

        # ─── 5. Apply A ───
        self.play(ApplyMatrix(A_vals, dyn), run_time=1.3)

        self.wait(0.2)

        # ─── 5.5 napis „Change the basis” po prawej od macierzy A ----
        basis_prompt = Text("Change the basis", color=LIGHT_TEXT, font_size=50)
        basis_prompt.to_edge(DOWN, buff=-2.75)   # A = Twój VGroup z macierzą A
        basis_prompt.set_z_index(5)                # nad maską
        self.play(Write(basis_prompt), run_time=0.5)
        self.wait(0.2)

        # ─── 6. obrót → new basis ───
        self.play(Rotate(dyn, PI/4), run_time=1.3)

        self.wait(0.2)

        # ─── 7. wprowadź B ───
        B_vals  = [[1.7, 0.0], [-0.3, 1.0]]
        B = self.basis_matrix(r"B =", B_vals).move_to(A)
        B.set_z_index(5)
        self.play(FadeOut(A), run_time=0.5)
        self.play(FadeIn(B),  run_time=0.5)

        self.wait(0.2)

        # ─── 8. Apply B ───
        self.play(ApplyMatrix(B_vals, dyn), run_time=1.3)
        self.wait(0.5)

        # ─── 8.5 Fade Out Change the basis ───
        self.play(FadeOut(basis_prompt), run_time=0.5)

        self.wait(0.2)

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
            MoveToTarget(B,  run_time=0.5),
            FadeIn(A_left,   run_time=0.5)
        )

        self.wait(0.2)

        # ─── Stage 3 – Krok 2 ───
        self.play(
            FadeOut(dyn),          # dyn_grid + x_axis + y_axis + square
            FadeOut(static_grid),  # biała statyczna kratka
            run_time=0.5
        )

        self.wait(0.2)             # stała pauza

        # --- Stage 3 · krok 3 -----------------------------------------
        #  tekst: "A and B are similar matrices"
        similar_txt = Text("A, B - similar matrices", color=LIGHT_TEXT)
        similar_txt.to_edge(UP, buff=1.0)     # linijkę pod macierzami
        similar_txt.set_z_index(5)

        self.play(Write(similar_txt), run_time=0.5)
        self.wait(0.2)

        # --- Stage 3 · krok 4 -----------------------------------------
        #  formuły podobieństwa + dopisek o P
        formula_txt = MathTex(r"A = P\,B\,P^{-1}\quad \quad B = P^{-1} A P",
                            color=LIGHT_TEXT, font_size=70)
        formula_txt.next_to(similar_txt, DOWN, buff=0.7)
        formula_txt.set_z_index(5)

        self.play(Write(formula_txt), run_time=0.5)
        self.wait(0.2)


        note_txt = Text("*P – invertible (non-singular) matrix",
                        color=LIGHT_TEXT, font_size=30)
        note_txt.next_to(formula_txt, DOWN, buff=0.7)
        formula_txt.set_z_index(5)
        self.play(Write(note_txt), run_time=0.5)

        self.wait(0.2)

        # --- Stage 3 · krok 5 ----------------------------------------
        self.play(
            FadeOut(A_left, run_time=0.5),
            FadeOut(B,      run_time=0.5)
        )
        self.wait(0.2)

        # --- Stage 3 · krok 6  (wersja z to_edge) --------------------
        theory_block = VGroup(similar_txt, formula_txt, note_txt)   # wszystko razem
        theory_block.generate_target()
        # przyklejamy do górnej krawędzi, ale opuszczamy o 5 jed.
        theory_block.target.to_edge(UP, buff=-3.0)        # górna krawędź

        self.play(MoveToTarget(theory_block, run_time=1.3))

        self.wait(0.2)

        # -------------------------------------------------------------
        # Stage 3 · krok 7 : kolejne własności podobieństwa (bullet list)
        # -------------------------------------------------------------
        props = [
            MathTex(r"\operatorname{tr}(A)=\operatorname{tr}(B)",     color=LIGHT_TEXT, font_size=80),
            MathTex(r"\det A = \det B",                               color=LIGHT_TEXT, font_size=80),
            MathTex(r"\operatorname{rank} A = \operatorname{rank} B", color=LIGHT_TEXT, font_size=80),
            MathTex(r"\forall_i\;\lambda_i(A)=\lambda_i(B)",          color=LIGHT_TEXT, font_size=80),  # eigenvalues
        ]

        # pierwszy wstaw zaraz pod theory_block, reszta schodzi w dół
        y_cursor = theory_block          # to jest blok z „similar matrices” + wzory
        for i, line in enumerate(props):
            line.next_to(y_cursor, DOWN, buff=1.2)
            line.set_z_index(5)
            self.play(Write(line), run_time=0.5)
            self.wait(0.2)
            y_cursor = line              # kolejna linijka pod poprzednią

        self.wait(1.0)

        # -------------------------------------------------------------
        # Stage 3 · krok 7  – CTA  + powrót do "nagiego" logo λ
        # -------------------------------------------------------------

        # 1) dopisek FOLLOW
        follow_txt = Text("Follow for more", color=PURPLE, font_size=80)
        follow_txt.next_to(props[-1], DOWN, buff=1.2)   # props[-1] = ostatnia linijka eigenvalues
        follow_txt.set_z_index(5)

        self.play(Write(follow_txt), run_time=0.5)
        
        self.wait(1.0)                                  # pauza 0.5 s

        # 2) znikamy wszystko oprócz logo λ
        #    (logo był dodany w szablonie jako foreground_mobject)
        everything = VGroup(
            self.hook_obj,
            self.outro_obj,          
            similar_txt,         # "A, B – similar matrices"
            theory_block,       # wzory + przypis
            *props,              # lista tr, det, rank, eigenvalues
            follow_txt
        )
        self.play(FadeOut(everything), run_time=0.6)
        self.wait(0.2)           # zostaje tylko logo λ → idealne do loopu