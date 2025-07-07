# Eigenmind/Long-form/2025-07/Project 1/waving_trig.py

import os, sys
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../")
    )
)

import numpy as np
from manim import (
    ValueTracker,
    always_redraw,
    PI,
    linear,
)
from Template.eigenmind_template import EigenScene, ORANGE, PURPLE

class WavingTrig(EigenScene):
    def __init__(self, **kwargs):
        # Force no gradient background
        super().__init__(use_gradient=False, **kwargs)

    def build(self):
        # 1) Axes + labels
        axes = self.make_axes(
            x_range=[-PI, PI, PI/2],
            y_range=[-1.5, 1.5, 1]
        )
        x_label = self.make_label("x", axes.x_axis, "RIGHT")
        y_label = self.make_label("y", axes.y_axis, "UP")
        self.add(axes, x_label, y_label)

        # 2) Phase tracker
        phase = ValueTracker(0)

        # 3) Orange sin curve
        sin_curve = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x + phase.get_value()),
                x_range=[-PI, PI],
                color=ORANGE,
                stroke_width=4
            )
        )
        # 4) Purple cos curve
        cos_curve = always_redraw(
            lambda: axes.plot(
                lambda x: np.cos(x + phase.get_value()),
                x_range=[-PI, PI],
                color=PURPLE,
                stroke_width=4
            )
        )
        self.add(sin_curve, cos_curve)

        self.frame.scale(1.25)
        
        self.wait(5)

        # 5) Animate both
        self.play(
            phase.animate.set_value(120 * PI),
            run_time=60,
            rate_func=linear
        )

        self.wait(5)
