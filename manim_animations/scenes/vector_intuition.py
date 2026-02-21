"""
Vector as a point in space — Part 1 GIF.
Build geometric intuition: numbers → 2D → 3D → high-D.
Black background, white text, one accent (blue). Loop-friendly.
Requires LaTeX (e.g. MiKTeX on Windows) for MathTex formulas.
"""

from manim import *


class VectorAsPointInSpace(ThreeDScene):
    """Progressive narrative: definition → 2D point → 3D → high-D → summary. Under ~15s."""

    def construct(self):
        self.camera.background_color = BLACK
        # Start with 2D-like view so no sudden snap when we show axes
        self.set_camera_orientation(phi=0, theta=0, gamma=0, zoom=0.8)

        # —— Step 1: Definition (fixed in frame so formula stays horizontal from the start) ——
        formula = MathTex(r"x = [x_1, x_2, \ldots, x_d]").scale(1.2)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula), run_time=2.2)
        self.play(formula.animate.set_color(BLUE).set_stroke(width=1.5), run_time=0.6)
        self.wait(0.8)

        # —— Step 2: Collapse to 2D ——
        formula_2d = MathTex(r"x = [3, 2]").scale(1.2).to_edge(UP, buff=0.5)
        self.play(Transform(formula, formula_2d), run_time=1.0)
        self.play(formula.animate.set_color(WHITE), run_time=0.35)

        # 2D axes (camera already at phi=0)
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 5, 1],
            x_length=5,
            y_length=4,
            axis_config={"color": GRAY, "include_numbers": True},
        ).to_edge(DOWN, buff=0.8)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Create(axes), run_time=1.0)

        dot = Dot(axes.c2p(3, 2), color=BLUE, radius=0.15)
        label = MathTex(r"(3, 2)").next_to(dot, UR, buff=0.15).scale(0.9)
        self.add_fixed_in_frame_mobjects(label)
        self.play(FadeIn(dot), FadeIn(label), run_time=0.8)
        caption = Text(
            "A vector is a point in space.",
            font_size=28,
            color=WHITE,
        ).next_to(formula, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(FadeIn(caption), run_time=0.65)
        self.wait(0.8)

        # —— Step 3: Transition to 3D (keep formula/label/caption fixed so they stay horizontal until faded) ——
        formula_3d = MathTex(r"x = [3, 2, 5]").scale(1.1).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(formula_3d)
        self.play(
            FadeOut(formula),
            FadeOut(label),
            FadeOut(caption),
            FadeIn(formula_3d),
            run_time=0.8,
        )
        self.wait(0.4)

        # Switch to 3D axes and move point up
        self.play(FadeOut(dot), run_time=0.35)
        axes_3d = ThreeDAxes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            z_range=[-1, 6, 1],
            x_length=4,
            y_length=4,
            z_length=4,
            axis_config={"color": GRAY},
        )
        self.play(FadeOut(axes), run_time=0.65)
        self.add(axes_3d)
        dot_3d = Dot3D(point=axes_3d.c2p(3, 2, 0), color=BLUE, radius=0.12)
        self.add(dot_3d)
        dot_3d_target = Dot3D(point=axes_3d.c2p(3, 2, 5), color=BLUE, radius=0.12)
        self.move_camera(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.9,
            run_time=1.8,
        )
        self.play(Transform(dot_3d, dot_3d_target), run_time=1.8)
        caption_3d = Text(
            "Add one number → add one dimension.",
            font_size=24,
            color=WHITE,
        ).to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(caption_3d)
        self.play(FadeIn(caption_3d), run_time=0.65)
        self.wait(0.8)

        # —— Step 4: ML bridge (keep formula_3d/caption_3d fixed until faded) ——
        self.play(
            FadeOut(axes_3d),
            FadeOut(dot_3d),
            FadeOut(formula_3d),
            FadeOut(caption_3d),
            run_time=0.9,
        )
        self.wait(0.4)
        # Animate camera back to front view instead of instant snap
        self.move_camera(phi=0, theta=0, gamma=0, zoom=1, run_time=1.2)
        self.wait(0.5)

        # —— Loop: back to definition ——
        loop_formula = MathTex(r"x = [x_1, x_2, \ldots, x_d]").scale(1.2)
        self.add_fixed_in_frame_mobjects(loop_formula)
        self.play(FadeIn(loop_formula), run_time=1.0)
        self.wait(0.8)
