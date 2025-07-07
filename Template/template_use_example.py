# in your new scene file, e.g. eigen_sine.py

from Template.eigenmind_template import EigenScene, ORANGE, PURPLE
from manim import *

class MySine(EigenScene):
    def build(self):
        axes = Axes(x_range=[-PI, PI], y_range=[-1.5, 1.5])
        sine = axes.plot(lambda x: np.sin(x), color=ORANGE)
        self.play(Create(axes), Create(sine))
        self.wait()
