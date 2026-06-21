"""
Dot product and norm — Part 2 GIF.
Shows dot product vs angle (positive → zero → negative), norms, and a short cosine-similarity hint.
Black background, white/gray text, one accent (blue). Same visual style as vector_intuition.
"""

from manim import *
import numpy as np


class DotProductAndNorm(Scene):
    """Dot product changes with angle; live norms; optional normalization hint."""

    def construct(self):
        self.camera.background_color = BLACK

        # —— Step 1: Plane and fixed vector x ——
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.15},
        ).set_color(GRAY)
        self.add(plane)

        x = np.array([3.0, 1.0, 0.0])
        vx = Vector(x, buff=0).set_stroke(width=8).set_color(BLUE)
        lx = MathTex(r"\mathbf{x}").scale(0.9).set_color(WHITE).next_to(vx.get_end(), UR, buff=0.15)
        self.play(Create(vx), FadeIn(lx), run_time=0.8)
        self.wait(0.3)

        # —— Step 2: Rotating vector y and angle arc ——
        y_len = 3.2
        theta = ValueTracker(20 * DEGREES)

        def y_vec():
            t = theta.get_value()
            return np.array([y_len * np.cos(t), y_len * np.sin(t), 0.0])

        vy = always_redraw(
            lambda: Vector(y_vec(), buff=0).set_stroke(width=8).set_color(GRAY)
        )
        ly = always_redraw(
            lambda: MathTex(r"\mathbf{y}")
            .scale(0.9)
            .set_color(GRAY)
            .next_to(vy.get_end(), UR, buff=0.15)
        )
        arc = always_redraw(
            lambda: Angle(
                Line(ORIGIN, vx.get_end()),
                Line(ORIGIN, vy.get_end()),
                radius=0.8,
                other_angle=False,
            ).set_stroke(width=5).set_color(GRAY)
        )
        self.play(Create(vy), FadeIn(ly), Create(arc), run_time=0.8)
        self.wait(0.3)

        # —— Step 3: Live readouts (dot product, norms, state) ——
        # Position labels first; add updating numbers as separate mobjects (not inside VGroup)
        # so they stay visible when always_redraw updates.
        dot_eq = (
            MathTex(r"\mathbf{x}^\top \mathbf{y} =")
            .scale(0.85)
            .set_color(WHITE)
            .to_corner(UL)
        )
        dot_value = always_redraw(
            lambda: DecimalNumber(
                np.dot(x[:2], y_vec()[:2]),
                num_decimal_places=2,
            )
            .scale(0.85)
            .set_color(WHITE)
            .next_to(dot_eq, RIGHT, buff=0.2)
        )

        normx_text = MathTex(r"\|\mathbf{x}\|=").scale(0.85).set_color(GRAY)
        normx_val = (
            DecimalNumber(np.linalg.norm(x[:2]), num_decimal_places=2)
            .scale(0.85)
            .set_color(GRAY)
        )
        normx_group = (
            VGroup(normx_text, normx_val)
            .arrange(RIGHT, buff=0.2)
            .next_to(dot_eq, DOWN, aligned_edge=LEFT)
        )

        normy_text = (
            MathTex(r"\|\mathbf{y}\|=")
            .scale(0.85)
            .set_color(GRAY)
            .next_to(normx_group, DOWN, aligned_edge=LEFT)
        )
        normy_value = always_redraw(
            lambda: DecimalNumber(
                np.linalg.norm(y_vec()[:2]), num_decimal_places=2
            )
            .scale(0.85)
            .set_color(GRAY)
            .next_to(normy_text, RIGHT, buff=0.2)
        )

        def dot_val():
            return np.dot(x[:2], y_vec()[:2])

        state = always_redraw(
            lambda: Text(
                "positive"
                if dot_val() > 0.05
                else ("zero" if abs(dot_val()) <= 0.05 else "negative"),
                font_size=28,
                color=GRAY,
            ).to_corner(UR)
        )

        self.play(
            FadeIn(dot_eq),
            FadeIn(dot_value),
            FadeIn(normx_group),
            FadeIn(normy_text),
            FadeIn(normy_value),
            FadeIn(state),
            run_time=0.6,
        )
        self.wait(0.4)

        # —— Step 4: Sweep angle (positive → zero → negative → positive) ——
        self.play(
            theta.animate.set_value(90 * DEGREES),
            run_time=1.4,
            rate_func=smooth,
        )
        self.wait(0.3)
        self.play(
            theta.animate.set_value(160 * DEGREES),
            run_time=1.4,
            rate_func=smooth,
        )
        self.wait(0.3)
        self.play(
            theta.animate.set_value(20 * DEGREES),
            run_time=1.0,
            rate_func=smooth,
        )
        self.wait(0.5)

        # —— Step 5: Normalization / cosine similarity hint ——
        note = Text(
            "Normalize → compare direction (cosine similarity)",
            font_size=26,
            color=GRAY,
        ).to_edge(DOWN)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(note), run_time=0.4)
        self.wait(0.3)
