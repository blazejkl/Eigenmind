from manim import *


class SineWave(Scene):
    def construct(self):
        # colors...
        DARK_BG, WHITE, ORANGE, PURPLE = "#121212", "#E0E0E0", "#FF5722", "#673AB7"
        config.background_color = DARK_BG

        axes = Axes(
            x_range=[-PI, PI, PI/2],
            y_range=[-1.5, 1.5, 1],
            x_axis_config={"color": ORANGE, "include_tip": True},
            y_axis_config={"color": PURPLE, "include_tip": True},
            axis_config={"stroke_width": 2},
        )
        # manually place your labels
        x_label = Text("x", color=WHITE).next_to(axes.x_axis.get_end(), DOWN)
        y_label = Text("y", color=WHITE).next_to(axes.y_axis.get_end(), RIGHT)
        self.add(axes, x_label, y_label)

        # ValueTracker to animate our phase
        phase = ValueTracker(0)

        # sine curve, always redrawn each frame with updated phase
        sine = always_redraw(lambda: axes.plot(
            lambda x: np.sin(x + phase.get_value()),
            color=ORANGE,
            stroke_width=3
        ))
        self.add(sine)

        # animate phase from 0 → 2π over 4 seconds, linear motion
        self.play(phase.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        self.wait()