"""euler_wave.py – Stage 2 (Neon tracer, purple theme, v3)

Tweaks per feedback
───────────────────
• Graph scaled **20 % larger** (coordinates × 1.2).  
• Vertex radius → **0.22** (≈ +20 %).  
• Edge stroke width → **8** px (thicker).  
• Tracer dot & trail also 8 px and radius bumped to **0.19**.  
• Animation speed unchanged (0.375 s per edge).

Euler circuit: 1‑2‑3‑5‑6‑4‑2‑5‑4‑3‑1

Render:
    manim -pqh Shorts/2025-07/euler_wave.py EulerWaveStage2
"""

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

from Template.short_form_template import ShortFormTemplate, LIGHT_TEXT, PURPLE  # noqa: E402


class EulerWaveStage2(ShortFormTemplate):
    HOOK_TEXT = "Eulerian Path"
    CONTENT_TEXT = "(visits every edge exactly once)"
    OUTRO_TEXT = None

    def construct(self):
        super().construct()

        # ---------------- coordinates (scaled 1.2×) ----------------
        coords = {
            1: [0,   4.8, 0],
            2: [-2.4, 2.4, 0],
            3: [ 2.4, 2.4, 0],
            4: [-2.4,-2.4, 0],
            5: [ 2.4,-2.4, 0],
            6: [0,  -4.8, 0],
        }

        edges_list = [
            (1, 2), (1, 3),
            (2, 3),
            (2, 4), (3, 5),
            (4, 6), (5, 6),
            (4, 5),
            (2, 5), (3, 4),
        ]

        graph = Graph(
            vertices=list(coords.keys()),
            edges=edges_list,
            layout=coords,
            vertex_config={"fill_color": PURPLE, "radius": 0.22},
            edge_config={"stroke_color": LIGHT_TEXT, "stroke_width": 8},
        )
        self.play(Create(graph, run_time=1.6, lag_ratio=0.1))
        self.wait(0.1)

        # ---------------- tracer setup ----------------
        path_vertices = [1, 2, 3, 5, 6, 4, 2, 5, 4, 3, 1]
        dot = Dot(point=graph.vertices[1].get_center(), radius=0.19, color=PURPLE)
        tracer = TracedPath(dot.get_center, stroke_color=PURPLE, stroke_width=8)
        self.add(tracer)

        def edge_obj(u: int, v: int):
            return graph.edges[(u, v)] if (u, v) in graph.edges else graph.edges[(v, u)]

        for u, v in zip(path_vertices, path_vertices[1:]):
            path_line = Line(graph.vertices[u].get_center(), graph.vertices[v].get_center())
            self.play(MoveAlongPath(dot, path_line, rate_func=linear), run_time=0.45)
            self.play(edge_obj(u, v).animate.set_stroke(color=PURPLE, width=8), run_time=0.001)

        self.play(FadeOut(dot), run_time=0.3)
        self.wait(0.5)
