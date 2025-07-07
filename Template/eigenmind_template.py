from manim import (
    Scene,
    Rectangle,
    SVGMobject,
    config,
    UL,
)

# ─────────────────────────────────────────────────────────────
# Eigenmind™ core palette
DARK_BG     = "#121212"
WHITE_TX    = "#E0E0E0"
ORANGE      = "#FF5722"
PURPLE      = "#673AB7"
# Axis/label defaults
TIP_LENGTH      = 0.1   # smaller arrowhead
LABEL_FONT_SIZE = 20     # smaller letters
# ─────────────────────────────────────────────────────────────

class EigenScene(Scene):
    """Base Scene for all Eigenmind animations."""

    def __init__(self, use_gradient: bool = False, **kwargs):
        # 4K × 60 fps + dark bg
        config.pixel_width       = 3840
        config.pixel_height      = 2160
        config.frame_rate        = 60
        config.background_color  = DARK_BG
        super().__init__(**kwargs)
        self.use_gradient = use_gradient

    def construct(self):
        # (no gradient by default)
        if self.use_gradient:
            gradient = Rectangle(
                width=config.frame_width,
                height=config.frame_height,
                fill_opacity=1
            ).set_fill(
                color=[ORANGE, PURPLE],
                opacity=[1,1],
                family=True
            ).set_z_index(-1)
            self.add(gradient)

        # tiny λ‐logo watermark (optional)
        logo = SVGMobject("Template/logo.svg")
        logo.set_height(0.4)
        logo.to_corner(UL, buff=0.2)
        logo.set_opacity(0.08)
        self.add(logo)

        # hand off to subclass
        self.build()

    def build(self):
        raise NotImplementedError(
            "Override build() in your EigenScene subclass."
        )

    @staticmethod
    def make_axes(x_range, y_range):
        from manim import Axes
        return Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={
                "color": WHITE_TX,
                "stroke_width": 2,
                "tip_length": TIP_LENGTH,
            },
            x_axis_config={"include_tip": True},
            y_axis_config={"include_tip": True},
        )

    @staticmethod
    def make_label(text, axis, direction):
        from manim import Text
        from manim import DOWN, UP, LEFT, RIGHT
        label = Text(text, font_size=LABEL_FONT_SIZE, color=WHITE_TX)
        label.next_to(
            axis.get_end(),
            {"DOWN": DOWN, "UP": UP, "LEFT": LEFT, "RIGHT": RIGHT}[direction],
            buff=0.2,
        )
        return label
