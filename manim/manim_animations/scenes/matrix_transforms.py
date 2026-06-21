"""
Matrix transforms space — Part 3 GIF (Building ML Intuition – Part 3).
3D axes; only the vector is transformed: rotate → stretch → shear.
Each transform (including shear) applies to one vector: A multiplies x.
Shows A in the corner; vector coordinates in 3D next to the vector, oriented along z so they rotate with the scene.
Black bg, white/gray, blue accent.
"""

from manim import *
import numpy as np


def integer_matrix_3x3(M):
    """Turn a 3×3 array into an IntegerMatrix mobject (whole numbers)."""
    rows = [
        [int(round(float(M[i][j]))) for j in range(3)]
        for i in range(3)
    ]
    return IntegerMatrix(rows).scale(0.6).set_color(WHITE)


class MatrixTransformsGIF(ThreeDScene):
    """Matrix (with numbers) and vector (with numbers) update as we apply transforms."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.9,
        )

        # —— Step 1: 3D axes with no numbers/labels ——
        no_numbers = {"include_numbers": False}
        axes = ThreeDAxes(
            x_range=[-3, 3, 0.5],
            y_range=[-3, 3, 0.5],
            z_range=[-2, 3, 0.5],
            x_length=5,
            y_length=5,
            z_length=4,
            axis_config={"color": GRAY, **no_numbers},
            x_axis_config=no_numbers,
            y_axis_config=no_numbers,
            z_axis_config=no_numbers,
        )
        for axis in axes.get_axes():
            if hasattr(axis, "numbers") and axis.numbers is not None:
                axis.remove(axis.numbers)

        x0 = np.array([2.0, 1.0, 2.0])  # original vector; we reset to this before each transform
        v = Arrow3D(
            start=np.array([0.0, 0.0, 0.0]),
            end=x0.copy(),
            color=BLUE,
            thickness=0.03,
            resolution=8,
        )

        step = MathTex(r"\text{Rotate}").scale(0.85).set_color(GRAY).to_corner(UR, buff=0.6)

        # Step label for "Stretch" uses "Scale" to avoid font ligature hiding the first "t"
        STEP_LABELS = {"Rotate": r"\text{Rotate}", "Stretch": r"\text{Scale}", "Shear": r"\text{Shear}"}

        # —— Matrices and vector check (applied in order: rotate → scale → shear) ——
        # Initial vector:  x0 = [2, 1, 2]
        #
        # R3 (60° about z):  cos60°=0.5, sin60°≈0.866
        #   [ 0.5  -0.87  0 ]     After R3 @ x0:  x1 ≈ [0.13, 2.23, 2]
        #   [ 0.87  0.5   0 ]
        #   [ 0     0     1 ]
        #
        # S3 (scale):      After S3 @ x1:  x2 ≈ [0.24, 1.12, 2]
        #   [ 1.8  0    0 ]
        #   [ 0    0.5  0 ]
        #   [ 0    0    1 ]
        #
        # H3 (shear y+=1.2*z):   After H3 @ x2:  x3 ≈ [0.24, 3.52, 2]
        #   [ 1  0    0   ]
        #   [ 0  1    1.2 ]
        #   [ 0  0    1   ]
        theta = 60 * DEGREES
        c, s = np.cos(theta), np.sin(theta)
        R3 = np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1],
        ])
        # Scale: stretch x by 1.8, y by 0.5, z unchanged
        #   S @ [x,y,z] = [1.8*x, 0.5*y, z]
        S3 = np.array([
            [1.8, 0, 0],
            [0, 0.5, 0],
            [0, 0, 1.0],
        ])
        # Shear: "slide" one axis along another (no rotation, no uniform scale).
        #   Here: add 1.2*z to y so the vector lifts in y; result clearly different from start.
        #   H @ [x,y,z] = [x, y + 1.2*z, z]
        H3 = np.array([
            [1.0, 0, 0],
            [0, 1.0, 1.2],
            [0, 0, 1.0],
        ])

        # A*x formula above the 3D axes (fixed in frame)
        formula_ax = MathTex(r"\mathbf{A}\mathbf{x}").scale(1.0).set_color(WHITE)
        formula_ax.move_to(ORIGIN + UP * 2.8)

        # A = (3×3 matrix) in corner only; no x under A
        A_label = MathTex(r"\mathbf{A} =").scale(0.75).set_color(WHITE)
        matrix_display = integer_matrix_3x3(R3)
        matrix_group = (
            VGroup(A_label, matrix_display)
            .arrange(RIGHT, buff=0.25)
            .to_edge(LEFT, buff=0.55)
            .to_edge(UP, buff=0.4)
        )

        # Vector coordinates in 3D next to the vector (1 decimal so changes are visible)
        def make_vec_label_3d():
            end = v.get_end()
            x0, x1, x2 = round(end[0], 1), round(end[1], 1), round(end[2], 1)
            label = MathTex(r"\begin{pmatrix}" + str(x0) + r" \\ " + str(x1) + r" \\ " + str(x2) + r"\end{pmatrix}")
            label.scale(0.5).set_color(WHITE)
            # Place at vector tip, offset along +x and slightly up (z) so it sits beside the vector
            tip = end + 0.4 * np.array([1.0, 0.0, 0.0]) + 0.2 * np.array([0.0, 0.0, 1.0])
            label.move_to(tip)
            # Orient vertically: rotate so label is in xz-plane (stands up along z), not flat in xy
            label.rotate(90 * DEGREES, axis=RIGHT, about_point=label.get_center())
            return label

        vec_label_3d = always_redraw(make_vec_label_3d)

        punch = Text(
            "Neural nets = stacks of transforms",
            font_size=26,
            color=GRAY,
        ).to_edge(DOWN, buff=0.35)

        self.add(axes)
        self.add(vec_label_3d)
        self.add_fixed_in_frame_mobjects(formula_ax, step, matrix_group, punch)
        self.play(Create(v), run_time=1.0)
        self.wait(0.5)

        def apply_3x3_to_vector(M3, label, reset_after=True):
            step_tex = STEP_LABELS.get(label, r"\text{" + label + "}")
            new_step = MathTex(step_tex).scale(0.85).set_color(GRAY).to_corner(UR, buff=0.6)
            new_matrix = integer_matrix_3x3(M3).move_to(matrix_display.get_center())
            self.play(
                Transform(step, new_step),
                Transform(matrix_display, new_matrix),
                run_time=0.3,
            )
            # Vector is always at x0 at the start of each step; apply A @ x0
            end2 = M3 @ x0
            v_new = Arrow3D(
                start=np.array([0.0, 0.0, 0.0]),
                end=end2,
                color=BLUE,
                thickness=0.03,
                resolution=8,
            )
            self.play(Transform(v, v_new), run_time=1.0, rate_func=smooth)
            self.wait(0.3)
            if reset_after:
                v_back = Arrow3D(
                    start=np.array([0.0, 0.0, 0.0]),
                    end=x0.copy(),
                    color=BLUE,
                    thickness=0.03,
                    resolution=8,
                )
                self.play(Transform(v, v_back), run_time=0.6, rate_func=smooth)
                self.wait(0.2)

        # —— Each step: start from [2,1,2], apply transform, then reset to [2,1,2] for next ——
        apply_3x3_to_vector(R3, "Rotate", reset_after=True)
        apply_3x3_to_vector(S3, "Stretch", reset_after=True)
        apply_3x3_to_vector(H3, "Shear", reset_after=False)

        self.wait(1.0)
