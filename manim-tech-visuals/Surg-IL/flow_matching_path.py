from manim import *
import numpy as np


class FlowMatchingPath(ThreeDScene):
    """
    Upper: fixed-in-frame 2D Source / Target squares.
    Lower: upright Source book → intermediate layers → Target book,
    with dots and path lines showing the continuous mapping.
    """

    # Shared layout constants (2D overlay ↔ 3D stack alignment)
    SOURCE_X = -2.6
    TARGET_X = 2.6
    OVERLAY_Y = 2.35
    BOOK_Y = -2.55
    TARGET_SHIFT = 5.2

    def construct(self):
        # ------------------------------------------------------------------
        # Camera configuration
        # Near front-on view: world Y → screen vertical, stack along X →
        # screen horizontal. Small phi keeps light depth without a diagonal.
        # ------------------------------------------------------------------
        self.set_camera_orientation(phi=12 * DEGREES, theta=-90 * DEGREES)
        self.camera.background_color = "#0b0f14"

        # World-space XYZ guide (moves with the 3D camera)
        #axis_arrows, axis_labels = self._build_axis_guide()
        #self.play(FadeIn(axis_arrows), FadeIn(axis_labels), run_time=0.5)
        # Keep X/Y/Z text readable as the camera moves
        #self.add_fixed_orientation_mobjects(*axis_labels)

        # ------------------------------------------------------------------
        # Upper 2D overlay (fixed in screen space)
        # ------------------------------------------------------------------
        overlay = self._build_upper_overlay()
        source_group = overlay["source_group"]
        target_group = overlay["target_group"]
        source_label = overlay["source_label"]
        target_label = overlay["target_label"]
        tgt_dots = overlay["tgt_dots"]
        target_positions = overlay["target_positions"]

        self.add_fixed_in_frame_mobjects(source_group, target_group)
        self.play(FadeIn(source_group), run_time=0.8)
        self.wait(0.3)

        # Rearrange Target dots while both groups still overlap
        self.play(
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(tgt_dots, target_positions)
            ],
            run_time=1.6,
            rate_func=smooth,
        )
        self.wait(0.25)

        # Slide Target square to the right
        self.play(
            target_group.animate.shift(RIGHT * self.TARGET_SHIFT),
            run_time=1.2,
        )
        target_label.next_to(target_group, DOWN, buff=0.22)

        self.add_fixed_in_frame_mobjects(source_label, target_label)
        self.play(FadeIn(source_label), FadeIn(target_label), run_time=0.6)
        self.wait(0.35)

        # ------------------------------------------------------------------
        # Lower 3D: Source book | intermediate stack | Target book
        # ------------------------------------------------------------------
        layer_data = self._build_book_stack(
            source_local=overlay["source_local"],
            target_local=overlay["target_local"],
        )
        source_book = layer_data["source_book"]
        target_book = layer_data["target_book"]
        intermediate_layers = layer_data["intermediate_layers"]
        path_lines = layer_data["path_lines"]

        # Source book appears under the 2D Source square
        self.play(FadeIn(source_book, shift=UP * 0.25), run_time=0.9)
        self.wait(0.15)

        # Target book appears under the 2D Target square
        self.play(FadeIn(target_book, shift=UP * 0.25), run_time=0.9)
        self.wait(0.15)

        # Intermediate upright layers fill the gap between the two books
        self.play(
            LaggedStart(
                *[
                    FadeIn(layer, shift=OUT * 0.1)
                    for layer in intermediate_layers
                ],
                lag_ratio=0.14,
            ),
            run_time=1.6,
        )
        self.wait(0.2)

        # Continuous Source → intermediates → Target mapping lines
        self.play(FadeIn(path_lines), run_time=1.0)
        self.wait(0.5)

        # Lift the camera a bit, then orbit once around the whole scene
        self.move_camera(phi=55 * DEGREES, theta=-90 * DEGREES, run_time=1.5)
        orbit_rate = 0.45  # rad/s
        #self.begin_ambient_camera_rotation(rate=orbit_rate)
        #self.wait(TAU / orbit_rate)  # one full revolution
        #self.stop_ambient_camera_rotation()
        self.wait(0.8)

    # ======================================================================
    # Axis guide (world X / Y / Z)
    # ======================================================================
    def _build_axis_guide(self):
        """
        Colored arrows at the origin so you can see which way each axis points
        under the current camera.
          X (red)   = left / right
          Y (green) = up / down
          Z (blue)  = in / out (depth)
        """
        axis_len = 1.6
        origin = ORIGIN + DOWN * 0.3

        x_arrow = Arrow3D(
            start=origin,
            end=origin + RIGHT * axis_len,
            color=RED,
            thickness=0.02,
        )
        y_arrow = Arrow3D(
            start=origin,
            end=origin + UP * axis_len,
            color=GREEN,
            thickness=0.02,
        )
        z_arrow = Arrow3D(
            start=origin,
            end=origin + OUT * axis_len,
            color=BLUE,
            thickness=0.02,
        )
        arrows = VGroup(x_arrow, y_arrow, z_arrow)

        labels = VGroup(
            Text("X", font_size=28, color=RED).move_to(
                origin + RIGHT * (axis_len + 0.35)
            ),
            Text("Y", font_size=28, color=GREEN).move_to(
                origin + UP * (axis_len + 0.35)
            ),
            Text("Z", font_size=28, color=BLUE).move_to(
                origin + OUT * (axis_len + 0.35)
            ),
        )
        return arrows, labels

    # ======================================================================
    # Upper 2D overlay
    # ======================================================================
    def _build_upper_overlay(self):
        rect_w, rect_h = 2.4, 2.6
        margin = 0.28
        n_dots = 7

        rng = np.random.default_rng(7)
        source_local = []
        ys = np.linspace(-rect_h / 2 + margin, rect_h / 2 - margin, n_dots)
        for y in ys:
            x = rng.uniform(-rect_w / 2 + margin, rect_w / 4)
            source_local.append(np.array([x, y, 0.0]))

        n_right = 4
        n_bottom = n_dots - n_right
        target_local = []

        right_x = rect_w / 2 - margin
        right_ys = np.linspace(rect_h / 2 - margin, -rect_h / 2 + 2 * margin, n_right)
        for y in right_ys:
            target_local.append(np.array([right_x, float(y), 0.0]))

        bottom_y = -rect_h / 2 + margin
        bottom_xs = np.linspace(-rect_w / 2 + margin, rect_w / 2 - 2 * margin, n_bottom)
        for x in bottom_xs:
            target_local.append(np.array([float(x), bottom_y, 0.0]))

        source_center = RIGHT * self.SOURCE_X + UP * self.OVERLAY_Y

        src_rect = RoundedRectangle(
            width=rect_w,
            height=rect_h,
            corner_radius=0.08,
            stroke_color=WHITE,
            stroke_width=2.5,
            fill_color=BLACK,
            fill_opacity=0.15,
        )
        src_dots = VGroup(
            *[Dot(point=p, radius=0.07, color=YELLOW_B) for p in source_local]
        )
        source_group = VGroup(src_rect, src_dots)
        source_group.move_to(source_center)

        target_group = source_group.copy()
        target_group[0].set_stroke(color=TEAL_A)
        for dot in target_group[1]:
            dot.set_color(TEAL_A)

        target_positions = [source_center + p for p in target_local]

        source_label = Text("Source", font_size=28, color=YELLOW_B)
        source_label.next_to(source_group, DOWN, buff=0.22)

        target_label = Text("Target", font_size=28, color=TEAL_A)

        return {
            "source_group": source_group,
            "target_group": target_group,
            "src_dots": source_group[1],
            "tgt_dots": target_group[1],
            "source_label": source_label,
            "target_label": target_label,
            "source_local": source_local,
            "target_local": target_local,
            "target_positions": target_positions,
        }

    # ======================================================================
    # Standing book panels + intermediate stack
    # ======================================================================
    def _make_layer(self, local_positions, colors, fill, stroke, opacity, panel_w, panel_h):
        """
        Build one upright panel + dots at the origin, then rotate the whole
        layer about ORIGIN so panel and dots stay locked together.
        Placement is handled separately via panel-center alignment.
        """
        panel = Rectangle(
            width=panel_w,
            height=panel_h,
            stroke_color=stroke,
            stroke_width=2.0,
            fill_color=fill,
            fill_opacity=opacity,
        )

        dots = VGroup(
            *[
                Dot(point=pos, radius=0.055, color=color)
                for pos, color in zip(local_positions, colors)
            ]
        )

        layer = VGroup(panel, dots)
        # Rotate about ORIGIN (not each submobject's own center) so asymmetric
        # dot layouts do not pull layers to different heights.
        layer.rotate(90 * DEGREES, axis=UP, about_point=ORIGIN)
        layer.rotate(18 * DEGREES, axis=UP, about_point=ORIGIN)
        return layer, panel, dots

    def _place_layer_on_baseline(self, layer, panel, x):
        """
        Snap the panel center onto the shared horizontal baseline.
        Only the stacking axis (x) varies; y (and z) stay fixed.
        """
        baseline_center = np.array([float(x), self.BOOK_Y, 0.0])
        layer.shift(baseline_center - panel.get_center())

    def _build_book_stack(self, source_local, target_local):
        """
        Layout on one horizontal baseline:
          [Source book] -- grey intermediates -- [Target book]
        All panel centers share the same y = BOOK_Y; only x changes.
        """
        n_intermediate = 6
        n_layers = n_intermediate + 2  # source + intermediates + target
        panel_w, panel_h = 2.1, 1.9

        source_local = [np.array(p, dtype=float) for p in source_local]
        target_local = [np.array(p, dtype=float) for p in target_local]
        scale = np.array([panel_w / 2.4, panel_h / 2.6, 1.0])
        src = [p * scale for p in source_local]
        tgt = [p * scale for p in target_local]

        # Even spacing along X only
        x_positions = np.linspace(self.SOURCE_X, self.TARGET_X, n_layers)

        all_layers = VGroup()
        all_panels = []
        all_dots = []

        for i, x in enumerate(x_positions):
            t = i / (n_layers - 1)
            positions = [(1.0 - t) * s + t * g for s, g in zip(src, tgt)]
            colors = [interpolate_color(YELLOW_B, TEAL_A, t) for _ in src]

            if i == 0:
                fill, stroke, opacity = "#F2C14E", "#F6D67A", 0.60
            elif i == n_layers - 1:
                fill, stroke, opacity = "#7BC47F", "#A8DBAB", 0.60
            else:
                fill, stroke, opacity = GREY_B, GREY_A, 0.20

            layer, panel, dots = self._make_layer(
                positions, colors, fill, stroke, opacity, panel_w, panel_h
            )
            self._place_layer_on_baseline(layer, panel, float(x))
            all_layers.add(layer)
            all_panels.append(panel)
            all_dots.append(dots)

        # Final safety pass: force every panel center onto the same y
        for panel, layer, x in zip(all_panels, all_layers, x_positions):
            self._place_layer_on_baseline(layer, panel, float(x))

        source_book = all_layers[0]
        target_book = all_layers[-1]
        intermediate_layers = VGroup(*all_layers[1:-1])

        path_lines = VGroup()
        n_points = len(all_dots[0])
        for p_idx in range(n_points):
            for layer_idx in range(n_layers - 1):
                d0 = all_dots[layer_idx][p_idx]
                d1 = all_dots[layer_idx + 1][p_idx]
                line = always_redraw(
                    lambda d0=d0, d1=d1, layer_idx=layer_idx, n_layers=n_layers: Line(
                        d0.get_center(),
                        d1.get_center(),
                        stroke_color=interpolate_color(
                            YELLOW_B,
                            TEAL_A,
                            (layer_idx + 0.5) / (n_layers - 1),
                        ),
                        stroke_width=1.6,
                        stroke_opacity=0.85,
                    )
                )
                path_lines.add(line)

        return {
            "source_book": source_book,
            "target_book": target_book,
            "intermediate_layers": intermediate_layers,
            "path_lines": path_lines,
            "all_layers": all_layers,
            "all_dots": all_dots,
        }
