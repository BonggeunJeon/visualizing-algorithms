import math
from manim import *


def make_cube_array(n=6, small_side=0.7, color=WHITE, fill_color=GREY_BROWN, fill_opacity=0.2):
    """Create an array of n small cubes in a grid (2 rows, or 1 row if n is small)."""
    cubes = Group()
    for i in range(n):
        c = Cube(
            side_length=small_side,
            fill_opacity=fill_opacity,
            fill_color=fill_color,
            stroke_width=1,
            stroke_color=color,
        )
        c.scale(0.5)
        cubes.add(c)
    rows = 2 if n > 1 else 1
    cols = math.ceil(n / rows)
    cubes.arrange_in_grid(rows=rows, cols=cols, buff=0.01)
    return cubes


class VLAStructure(ThreeDScene):
    """
    Basic VLA structure: two cubes (Vision Backbone, Language Backbone),
    RGB-style overlapping rectangles top-left, instruction text top-right.
    """

    def construct(self):
        # 1. Two cubes at center
        cube_width = 5.0
        left_cube = Cube(
            side_length=cube_width,
            fill_opacity=0.3,
            fill_color=TEAL,
            stroke_width=2,
            stroke_color=WHITE,
        )
        right_cube = Cube(
            side_length=cube_width,
            fill_opacity=0.3,
            fill_color=BLUE,
            stroke_width=2,
            stroke_color=WHITE,
        )
        left_cube.scale(0.5)
        right_cube.scale(0.5)
        left_cube.move_to(LEFT * 2.5)
        right_cube.move_to(RIGHT * 2.5)
        self.play(FadeIn(left_cube), FadeIn(right_cube), run_time=1.5)
        self.wait(0.5)

        # 2. Tex on cubes: "Vision Backbone" (left), "Language Backbone" (right)
        vision_text = Tex("Vision Backbone", font_size=28, color=WHITE)
        language_text = Tex("Language Backbone", font_size=28, color=WHITE)
        vision_text.next_to(left_cube, DOWN, buff=0.25)
        language_text.next_to(right_cube, DOWN, buff=0.25)
        self.play(FadeIn(vision_text), FadeIn(language_text), run_time=1.0)
        self.wait(0.5)

        # 3. Top left: 3 overlapping rectangles (RGB channel style)
        rect_w, rect_h = 0.8, 0.6
        offset = 0.12
        red_rect = Rectangle(
            width=rect_w,
            height=rect_h,
            fill_opacity=0.6,
            fill_color=RED,
            stroke_width=1,
            stroke_color=WHITE,
        )
        green_rect = Rectangle(
            width=rect_w,
            height=rect_h,
            fill_opacity=0.6,
            fill_color=GREEN,
            stroke_width=1,
            stroke_color=WHITE,
        )
        blue_rect = Rectangle(
            width=rect_w,
            height=rect_h,
            fill_opacity=0.6,
            fill_color=BLUE,
            stroke_width=1,
            stroke_color=WHITE,
        )
        # Overlap: shift slightly so they stack like RGB channels
        red_rect.move_to(left_cube.get_top() + UP * 0.8)
        green_rect.move_to(red_rect.get_center() + RIGHT * offset + UP * offset)
        blue_rect.move_to(green_rect.get_center() + RIGHT * offset + UP * offset)
        rgb_group = Group(red_rect, green_rect, blue_rect)
        self.play(
            FadeIn(red_rect),
            FadeIn(green_rect),
            FadeIn(blue_rect),
            run_time=1.0,
        )
        self.wait(0.5)

        # 4. Top right: "Grasp and retract bowel"
        instruction_text = Tex("Grasp and Retract bowel", font_size=24, color=WHITE)
        instruction_text.move_to(right_cube.get_top() + UP * 0.8)
        self.play(Write(instruction_text), run_time=1.0)
        self.wait(1.0)

        # 5. RGB rects sucked into left_cube and disappear
        left_center = left_cube.get_center()
        self.play(
            red_rect.animate.move_to(left_center).scale(
                0.01, about_point=left_center
            ),
            green_rect.animate.move_to(left_center).scale(
                0.01, about_point=left_center
            ),
            blue_rect.animate.move_to(left_center).scale(
                0.01, about_point=left_center
            ),
            run_time=1.2,
        )
        self.remove(red_rect, green_rect, blue_rect)
        self.wait(0.3)

        # 6. instruction_text sucked into right_cube and disappear
        right_center = right_cube.get_center()
        self.play(
            instruction_text.animate.move_to(right_center).scale(
                0.01, about_point=right_center
            ),
            run_time=1.2,
        )
        self.remove(instruction_text)
        self.wait(1.0)

        # 7. Pull camera down, then cube arrays emerge from left/right cubes (opposite of sucked-in)
        left_cube_array = make_cube_array(color=TEAL, fill_color=TEAL)
        right_cube_array = make_cube_array(color=BLUE, fill_color=BLUE)
        left_cube_array.next_to(left_cube, DOWN, buff=1.6)
        right_cube_array.next_to(right_cube, DOWN, buff=1.6)
        left_final = left_cube_array.get_center()
        right_final = right_cube_array.get_center()
        # Start state: inside each cube (tiny)
        left_cube_array.move_to(left_center).scale(0.001, about_point=left_center)
        right_cube_array.move_to(right_center).scale(0.001, about_point=right_center)
        self.add(left_cube_array, right_cube_array)

        # ThreeDScene has no camera.frame; shift scene up (same as pulling camera down)
        scene_shift = Group(
            left_cube, right_cube, vision_text, language_text,
            left_cube_array, right_cube_array,
        )
        self.play(scene_shift.animate.shift(UP * 1.8), run_time=1.2)
        self.wait(0.3)
        # Emerge from cubes: move to final position and scale up (targets shifted up too)
        shift_up = UP * 1.8
        self.play(
            left_cube_array.animate.move_to(left_final + shift_up).scale(
                1500, about_point=left_final + shift_up
            ),
            right_cube_array.animate.move_to(right_final + shift_up).scale(
                1500, about_point=right_final + shift_up
            ),
            run_time=1.2,
        )
        self.wait(1.0)

        # 7b. Tex below each cube array
        left_cube_tex = Tex("Image tokens", font_size=22, color=WHITE)
        right_cube_tex = Tex("Language tokens", font_size=22, color=WHITE)
        left_cube_tex.next_to(left_cube_array, DOWN, buff=0.25)
        right_cube_tex.next_to(right_cube_array, DOWN, buff=0.25)
        self.play(FadeIn(left_cube_tex), FadeIn(right_cube_tex), run_time=0.8)
        self.wait(0.5)

        # 8. Pull camera down again
        shift_up_2 = UP * 2.5
        scene_shift_2 = Group(
            left_cube, right_cube, vision_text, language_text,
            left_cube_array, right_cube_array,
            left_cube_tex, right_cube_tex,
        )
        self.play(scene_shift_2.animate.shift(shift_up_2), run_time=1.2)
        self.wait(0.3)

        # 9. Action Decoder Cube + Tex (FadeIn)
        action_decoder_cube = Cube(
            side_length=5.0,
            fill_opacity=0.25,
            fill_color=RED,
            stroke_width=2,
            stroke_color=WHITE,
        )
        action_decoder_cube.scale(0.5)
        arrays_center = (left_cube_array.get_center() + right_cube_array.get_center()) / 2
        action_decoder_cube.next_to(arrays_center, DOWN, buff=0.8)
        action_decoder_text = Tex("Action Decoder", font_size=28, color=WHITE)
        action_decoder_text.next_to(action_decoder_cube, DOWN, buff=0.2)
        self.add(action_decoder_cube, action_decoder_text)
        self.play(FadeIn(action_decoder_cube), FadeIn(action_decoder_text), run_time=1.0)
        self.wait(0.5)

        # 10. Group two arrays -> token_cube_array, place at top inside Action Decoder
        combined_arrays = Group(left_cube_array, right_cube_array, left_cube_tex, right_cube_tex)
        token_cube_array = make_cube_array(
            n=8, small_side=0.4, color=GOLD, fill_color=GOLD, fill_opacity=0.2
        )
        token_cube_array.move_to(
            action_decoder_cube.get_center() + UP * 0.35
        )
        token_cube_tex = Tex("Observation tokens", font_size=22, color=WHITE)
        token_cube_tex.next_to(token_cube_array, DOWN, buff=0.2)
        self.play(
            ReplacementTransform(combined_arrays, token_cube_array),
            run_time=1.5,
        )
        self.play(FadeIn(token_cube_tex), run_time=0.6)
        self.wait(3.0)
