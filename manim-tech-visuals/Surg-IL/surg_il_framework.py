from manim import *

class SurgILAnimation(Scene):
    """
    Animation showing Surg-IL text transformation and VLA expansion.
    """
    
    def construct(self):
        # Step 1: Show "Surg-IL" at the center
        text1 = Text("Surg-IL", font_size=48, color=WHITE)
        text1.move_to(ORIGIN + LEFT * 2)
        
        self.play(Write(text1), run_time=1.5)
        self.wait(0.5)
        
        # Step 2: Add "≈ VLA" next to text1 (keep text1 in place)
        vla_text = Text("≈  VLA", font_size=48, color=WHITE)
        vla_text.next_to(text1, RIGHT, buff=0.2)
        # Don't move text1 - just add vla_text at its position
        
        self.play(Write(vla_text), run_time=1.5)
        self.wait(0.5)
        
        # Step 3: Split "VLA" vertically (keep text1 and "≈ " unchanged)
        # Create "≈ " text - position it next to text1 (same as vla_text position)
        approx_text = Text("≈  ", font_size=48, color=WHITE)
        approx_text.next_to(text1, RIGHT, buff=0.2)
        
        # Create individual letters V, L, A
        v_letter = Text("  V", font_size=48, color=WHITE)
        l_letter = Text("  L", font_size=48, color=WHITE)
        a_letter = Text("  A", font_size=48, color=WHITE)
        
        # Arrange V, L, A vertically with margin
        vla_vertical = VGroup(v_letter, l_letter, a_letter)
        vla_vertical.arrange(DOWN, buff=0.5)
        
        # Position vla_vertical to the right of approx_text (where VLA was)
        vla_vertical.next_to(approx_text, RIGHT, buff=0)
        
        # Transform vla_text to show split (only VLA becomes vertical, "≈ " stays at same position)
        self.play(ReplacementTransform(vla_text, VGroup(approx_text, vla_vertical)), run_time=1.0)
        self.wait(0.5)
        
        # Step 4: Add expansion text to each letter (keep letter positions unchanged)
        # Add "ision" after V
        vision_rest = Text("ision", font_size=48, color=WHITE)
        vision_rest.next_to(v_letter, RIGHT, buff=0)
        
        # Add "anguage" after L
        language_rest = Text("anguage", font_size=48, color=WHITE)
        language_rest.next_to(l_letter, RIGHT, buff=0)
        
        # Add "ction" after A
        action_rest = Text("ction", font_size=48, color=WHITE)
        action_rest.next_to(a_letter, RIGHT, buff=0)
        
        # Write all expansion texts simultaneously
        self.play(
            Write(vision_rest),
            Write(language_rest),
            Write(action_rest),
            run_time=1.0,
            lag_ratio=0.3
        )
        self.wait(0.5)
        
        # Step 5: Remove Language (keep only Vision and Action)
        self.play(
            FadeOut(l_letter),
            FadeOut(language_rest),
            run_time=0.5
        )
        self.wait(0.5)
        
        # Step 6: Emphasize Vision and Action with BLUE color
        self.play(
            v_letter.animate.set_color(BLUE),
            vision_rest.animate.set_color(BLUE),
            a_letter.animate.set_color(BLUE),
            action_rest.animate.set_color(BLUE),
            run_time=0.7
        )
        self.wait(0.5)
        
        # Step 7: Move camera perspective to the right
        # Get all visible objects to shift them (simulating camera movement)
        all_visible = VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)])
        self.play(all_visible.animate.shift(LEFT * 3), run_time=1.5)
        self.wait(0.5)
        
        # Step 8: Draw arrow with right angle from above "Vision" to rectangle
        # Create Vision text group for positioning
        vision_text = VGroup(v_letter, vision_rest)
        
        # Arrow starts above Vision, goes up, then right (no downward segment)
        arrow_start = vision_text.get_top()
        arrow_up_end = arrow_start + UP * 1.5
        arrow_right_end = arrow_up_end + RIGHT * 3.0
        
        # Create arrow segments - only the last one has arrowhead
        arrow_h_up = Line(arrow_start, arrow_up_end, color=WHITE, stroke_width=3)
        arrow_h_right = Arrow(arrow_up_end, arrow_right_end, color=WHITE, stroke_width=3, buff=0)
        
        # Create the right-angle arrow group
        right_angle_arrow = VGroup(arrow_h_up, arrow_h_right)
        
        # Draw the arrow
        self.play(Create(right_angle_arrow), run_time=1.5)
        self.wait(0.3)
        
        # Step 9: Draw rectangle next to the right angle arrow
        encoding_rect = Rectangle(
            width=3.0,
            height=1.0,
            color=PURE_RED,
            fill_opacity=0.3
        )
        # Position rectangle to the right of where the arrow ends
        encoding_rect.next_to(arrow_right_end, RIGHT, buff=0.1)
        
        self.play(Create(encoding_rect), run_time=1.0)
        self.wait(0.5)
        
        # Step 10: Write "Encoding Pipeline" in the rectangle
        encoding_text = Text("Encoding Pipeline", font_size=24, color=WHITE)
        encoding_text.move_to(encoding_rect.get_center())
        
        self.play(Write(encoding_text), run_time=1.0)
        self.wait(0.5)
        
        # Step 11: Draw five rectangles below and a bit left of encoding_rect
        sub_rect1 = Rectangle(width=1.5, height=0.6, color=WHITE, fill_opacity=0.3)
        sub_rect2 = Rectangle(width=1.5, height=0.6, color=WHITE, fill_opacity=0.3)
        sub_rect3 = Rectangle(width=1.5, height=0.6, color=WHITE, fill_opacity=0.3)
        sub_rect4 = Rectangle(width=1.5, height=0.6, color=WHITE, fill_opacity=0.3)
        sub_rect5 = Rectangle(width=1.5, height=0.6, color=WHITE, fill_opacity=0.3)
        
        # Group the five rectangles and arrange them vertically
        sub_rects = VGroup(sub_rect1, sub_rect2, sub_rect3, sub_rect4, sub_rect5)
        sub_rects.arrange(DOWN, buff=0.3)
        
        # Position the group below and a bit left of encoding_rect
        sub_rects.next_to(encoding_rect, DOWN + RIGHT * 0.3, buff=1.0)
        
        # Step 11: Draw all five rectangles simultaneously
        self.play(Create(sub_rects), run_time=1.5, lag_ratio=0)
        self.wait(0.5)
        
        # Step 12: Create right-angle arrows connecting encoding_rect to each sub-rectangle
        arrows_group = VGroup()
        sub_rect5_arrow = None  # Store reference to sub_rect5 arrow
        
        for sub_rect in [sub_rect1, sub_rect2, sub_rect3, sub_rect4, sub_rect5]:
            # Arrow starts from bottom of encoding_rect
            arrow_start = encoding_rect.get_bottom()
            # Calculate vertical position to align with sub-rectangle center
            # Create a point at the same x as arrow_start but y aligned with sub-rectangle center
            arrow_down_end = np.array([arrow_start[0], sub_rect.get_center()[1], arrow_start[2]])
            # Then go right to reach the sub-rectangle (left side)
            arrow_right_end = sub_rect.get_left()
            
            # Create right-angle arrow segments (line down, then arrow right)
            arrow_line_down = Line(arrow_start, arrow_down_end, color=WHITE, stroke_width=2)
            arrow_line_right = Line(arrow_down_end, arrow_right_end, color=WHITE, stroke_width=2, buff=0)
            
            # Group the arrow segments
            connection_arrow = VGroup(arrow_line_down, arrow_line_right)
            arrows_group.add(connection_arrow)
            
            # Store reference to sub_rect5 arrow
            if sub_rect == sub_rect5:
                sub_rect5_arrow = connection_arrow
        
        # Step 13: Draw all connection arrows simultaneously
        self.play(Create(arrows_group), run_time=1.5, lag_ratio=0)
        self.wait(0.5)
        
        # Step 14: Write text into each sub-rectangle
        sub_text1 = Text("depth", font_size=16, color=WHITE)
        sub_text1.move_to(sub_rect1.get_center())
        
        sub_text2 = Text("language", font_size=16, color=WHITE)
        sub_text2.move_to(sub_rect2.get_center())
        
        sub_text3 = Text("mutimodal", font_size=16, color=WHITE)
        sub_text3.move_to(sub_rect3.get_center())
        
        sub_text4 = Text("proprioceptive", font_size=16, color=WHITE)
        sub_text4.move_to(sub_rect4.get_center())
        
        sub_text5 = Text("rgb", font_size=16, color=WHITE)
        sub_text5.move_to(sub_rect5.get_center())
        
        # Write all texts simultaneously
        self.play(
            Write(sub_text1),
            Write(sub_text2),
            Write(sub_text3),
            Write(sub_text4),
            Write(sub_text5),
            run_time=1.5,
            lag_ratio=0
        )
        self.wait(0.5)
        
        # Step 15: Change arrow color to YELLOW for sub_rect5
        self.play(
            sub_rect5_arrow[0].animate.set_color(YELLOW),  # arrow_line_down
            sub_rect5_arrow[1].animate.set_color(YELLOW),  # arrow_line_right
            run_time=1.0
        )
        self.wait(0.5)
        
        # Step 16: Move camera perspective to the Right
        all_visible = VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)])
        self.play(all_visible.animate.shift(LEFT * 3), run_time=1.5)
        self.wait(0.5)
        
        # Step 17: Draw three sub-rectangles from sub_rect5
        cnn_rect1 = Rectangle(width=1.8, height=0.6, color=WHITE, fill_opacity=0.3)
        cnn_rect2 = Rectangle(width=1.8, height=0.6, color=WHITE, fill_opacity=0.3)
        cnn_rect3 = Rectangle(width=1.8, height=0.6, color=WHITE, fill_opacity=0.3)
        
        # Position cnn_rect2 next to sub_rect5 (to the right)
        cnn_rect2.next_to(sub_rect5, RIGHT, buff=1.0)
        # Position cnn_rect1 above cnn_rect2
        cnn_rect1.next_to(cnn_rect2, UP, buff=0.3)
        # Position cnn_rect3 below cnn_rect2
        cnn_rect3.next_to(cnn_rect2, DOWN, buff=0.3)
        
        # Draw all three rectangles simultaneously
        cnn_rects = VGroup(cnn_rect1, cnn_rect2, cnn_rect3)
        self.play(Create(cnn_rects), run_time=1.5, lag_ratio=0)
        self.wait(0.5)
        
        # Step 18: Draw arrows from sub_rect5 (right) to each cnn_rect (left)
        # Arrow 1: from sub_rect5 to cnn_rect1 (right-angle: right, then up, then left)
        arrow1_start = sub_rect5.get_right()
        arrow1_right_end = arrow1_start + RIGHT * 0.8
        arrow1_up_end = np.array([arrow1_right_end[0], cnn_rect1.get_center()[1], arrow1_right_end[2]])
        arrow1_left_end = cnn_rect1.get_left()
        
        arrow1_line_right = Line(arrow1_start, arrow1_right_end, color=WHITE, stroke_width=2)
        arrow1_line_up = Line(arrow1_right_end, arrow1_up_end, color=WHITE, stroke_width=2)
        arrow1_line_left = Arrow(arrow1_up_end, arrow1_left_end, color=WHITE, stroke_width=2, buff=0)
        arrow1_connection = VGroup(arrow1_line_right, arrow1_line_up, arrow1_line_left)
        
        # Arrow 2: from sub_rect5 to cnn_rect2 (straight line)
        arrow2_start = sub_rect5.get_right()
        arrow2_end = cnn_rect2.get_left()
        arrow2_connection = Line(arrow2_start, arrow2_end, color=WHITE, stroke_width=2, buff=0)
        
        # Arrow 3: from sub_rect5 to cnn_rect3 (right-angle: right, then down, then left)
        arrow3_start = sub_rect5.get_right()
        arrow3_right_end = arrow3_start + RIGHT * 0.8
        arrow3_down_end = np.array([arrow3_right_end[0], cnn_rect3.get_center()[1], arrow3_right_end[2]])
        arrow3_left_end = cnn_rect3.get_left()
        
        arrow3_line_right = Line(arrow3_start, arrow3_right_end, color=WHITE, stroke_width=2)
        arrow3_line_down = Line(arrow3_right_end, arrow3_down_end, color=WHITE, stroke_width=2)
        arrow3_line_left = Line(arrow3_down_end, arrow3_left_end, color=WHITE, stroke_width=2, buff=0)
        arrow3_connection = VGroup(arrow3_line_right, arrow3_line_down, arrow3_line_left)
        
        # Draw all arrows simultaneously
        cnn_arrows = VGroup(arrow1_connection, arrow2_connection, arrow3_connection)
        self.play(Create(cnn_arrows), run_time=1.0, lag_ratio=0)
        self.wait(0.5)
        
        # Step 19: Write text in each rectangle
        cnn_text1 = Text("CNN", font_size=16, color=WHITE)
        cnn_text1.move_to(cnn_rect1.get_center())
        
        cnn_text2 = Text("Conditional CNN", font_size=14, color=WHITE)
        cnn_text2.move_to(cnn_rect2.get_center())
        
        cnn_text3 = Text("ViT", font_size=16, color=WHITE)
        cnn_text3.move_to(cnn_rect3.get_center())
        
        # Write all texts simultaneously
        self.play(
            Write(cnn_text1),
            Write(cnn_text2),
            Write(cnn_text3),
            run_time=1.5,
            lag_ratio=0
        )
        self.wait(0.5)
        
        # Step 20: Change color of line from rgb (sub_rect5) to CNN (cnn_rect1) to YELLOW
        self.play(
            arrow1_connection[0].animate.set_color(YELLOW),  # arrow1_line_right
            arrow1_connection[1].animate.set_color(YELLOW),  # arrow1_line_up
            arrow1_connection[2].animate.set_color(YELLOW),  # arrow1_line_left
            run_time=1.0
        )
        self.wait(0.5)
        
        # Step 21: Move camera perspective UP
        all_visible = VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)])
        self.play(all_visible.animate.shift(UP * 4), run_time=1.5)
        self.wait(0.5)
        
        # Step 22: Draw rectangle below sub_rect5
        algorithm_rect = Rectangle(
            width=2.5,
            height=0.8,
            color=PURE_BLUE,
            fill_opacity=0.3
        )
        algorithm_rect.next_to(sub_rect5, DOWN * 3, buff=1.0)
        
        self.play(Create(algorithm_rect), run_time=1.0)
        self.wait(0.5)
        
        # Step 23: Write text "Algorithm" in the rectangle
        algorithm_text = Text("Algorithm", font_size=20, color=WHITE)
        algorithm_text.move_to(algorithm_rect.get_center())
        
        self.play(Write(algorithm_text), run_time=1.0)
        self.wait(0.5)
        
        # Step 24: Draw right-angle line from action_rest to the left of rectangle
        # action_rest is part of "Action" text, get its position
        action_text = VGroup(a_letter, action_rest)  # "Action" = "A" + "ction"
        line_start = action_text.get_bottom()
        
        # Right-angle: go down, then right to reach the left side of rectangle
        line_down_end = line_start + DOWN
        line_right_end = algorithm_rect.get_left()
        # Calculate the horizontal position where we turn right
        line_turn_point = np.array([line_down_end[0], algorithm_rect.get_left()[1], line_down_end[2]])
        
        # Create right-angle line segments
        algorithm_line_down = Line(line_start, line_turn_point, color=WHITE, stroke_width=2)
        algorithm_line_right = Line(line_turn_point, line_right_end, color=WHITE, stroke_width=2)
        
        algorithm_line = VGroup(algorithm_line_down, algorithm_line_right)
        
        self.play(Create(algorithm_line), run_time=1.0)
        self.wait(0.5)
        
        # Step 25: Draw three sub-rectangles from algorithm_rect
        algo_rect1 = Rectangle(width=1.8, height=0.6, color=WHITE, fill_opacity=0.3)
        algo_rect2 = Rectangle(width=1.8, height=0.6, color=WHITE, fill_opacity=0.3)
        algo_rect3 = Rectangle(width=1.8, height=0.6, color=WHITE, fill_opacity=0.3)
        
        # Position algo_rect2 next to algorithm_rect (to the right)
        algo_rect2.next_to(algorithm_rect, RIGHT, buff=1.0)
        # Position algo_rect1 above algo_rect2
        algo_rect1.next_to(algo_rect2, UP, buff=0.3)
        # Position algo_rect3 below algo_rect2
        algo_rect3.next_to(algo_rect2, DOWN, buff=0.3)
        
        # Draw all three rectangles simultaneously
        algo_rects = VGroup(algo_rect1, algo_rect2, algo_rect3)
        self.play(Create(algo_rects), run_time=1.5, lag_ratio=0)
        self.wait(0.5)
        
        # Step 26: Draw lines connecting from algorithm_rect (right) to each algo_rect (left)
        # Line 1: from algorithm_rect to algo_rect1 (right-angle: right, then up, then left)
        algo_line1_start = algorithm_rect.get_right()
        algo_line1_right_end = algo_line1_start + RIGHT * 0.8
        algo_line1_up_end = np.array([algo_line1_right_end[0], algo_rect1.get_center()[1], algo_line1_right_end[2]])
        algo_line1_left_end = algo_rect1.get_left()
        
        algo_line1_right = Line(algo_line1_start, algo_line1_right_end, color=WHITE, stroke_width=2)
        algo_line1_up = Line(algo_line1_right_end, algo_line1_up_end, color=WHITE, stroke_width=2)
        algo_line1_left = Line(algo_line1_up_end, algo_line1_left_end, color=WHITE, stroke_width=2)
        algo_line1_connection = VGroup(algo_line1_right, algo_line1_up, algo_line1_left)
        
        # Line 2: from algorithm_rect to algo_rect2 (straight line)
        algo_line2_start = algorithm_rect.get_right()
        algo_line2_end = algo_rect2.get_left()
        algo_line2_connection = Line(algo_line2_start, algo_line2_end, color=WHITE, stroke_width=2)
        
        # Line 3: from algorithm_rect to algo_rect3 (right-angle: right, then down, then left)
        algo_line3_start = algorithm_rect.get_right()
        algo_line3_right_end = algo_line3_start + RIGHT * 0.8
        algo_line3_down_end = np.array([algo_line3_right_end[0], algo_rect3.get_center()[1], algo_line3_right_end[2]])
        algo_line3_left_end = algo_rect3.get_left()
        
        algo_line3_right = Line(algo_line3_start, algo_line3_right_end, color=WHITE, stroke_width=2)
        algo_line3_down = Line(algo_line3_right_end, algo_line3_down_end, color=WHITE, stroke_width=2)
        algo_line3_left = Line(algo_line3_down_end, algo_line3_left_end, color=WHITE, stroke_width=2)
        algo_line3_connection = VGroup(algo_line3_right, algo_line3_down, algo_line3_left)
        
        # Draw all lines simultaneously
        algo_lines = VGroup(algo_line1_connection, algo_line2_connection, algo_line3_connection)
        self.play(Create(algo_lines), run_time=1.5, lag_ratio=0)
        self.wait(0.5)
        
        # Step 27: Write text in each rectangle
        algo_text1 = Text("BC", font_size=16, color=WHITE)
        algo_text1.move_to(algo_rect1.get_center())
        
        algo_text2 = Text("Flow Matching", font_size=14, color=WHITE)
        algo_text2.move_to(algo_rect2.get_center())
        
        algo_text3 = Text("Diffusion", font_size=16, color=WHITE)
        algo_text3.move_to(algo_rect3.get_center())
        
        # Write all texts simultaneously
        self.play(
            Write(algo_text1),
            Write(algo_text2),
            Write(algo_text3),
            run_time=1.5,
            lag_ratio=0
        )
        self.wait(0.5)
        
        # Change algo_line2 color to YELLOW
        self.play(
            algo_line2_connection.animate.set_color(YELLOW),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Step 28: Move camera perspective to the Right
        all_visible = VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)])
        self.play(all_visible.animate.shift(LEFT * 6.0), run_time=1.5)
        self.wait(0.5)
        
        # Step 29: Draw rectangle next to algo_rect1 and write "Decoder"
        decoder_rect = Rectangle(
            width=2.5,
            height=0.8,
            color=PURE_GREEN,
            fill_opacity=0.3
        )
        decoder_rect.next_to(algo_rect1, RIGHT * 1.0 + UP * 1.0, buff=1.0)
        
        self.play(Create(decoder_rect), run_time=1.0)
        self.wait(0.5)
        
        decoder_text = Text("Decoder", font_size=18, color=WHITE)
        decoder_text.move_to(decoder_rect.get_center())
        
        self.play(Write(decoder_text), run_time=1.0)
        self.wait(0.5)
        
        # Step 30: Draw right-angle lines from algo_rect2 and cnn_rect1 to Decoder rectangle (L-shaped: two lines each)
        # Line from algo_rect2 (right) to decoder_rect (bottom) - L-shape: right then up (ㄴ)
        algo2_line_start = algo_rect2.get_right()
        algo2_line_right_end = algo2_line_start + RIGHT * 0.8
        algo2_line_end = decoder_rect.get_bottom()
        
        algo2_line_right = Line(algo2_line_start, algo2_line_right_end, color=WHITE, stroke_width=2)
        algo2_line_up = Line(algo2_line_right_end, algo2_line_end, color=WHITE, stroke_width=2)
        algo2_to_decoder = VGroup(algo2_line_right, algo2_line_up)
        
        # Line from cnn_rect1 (right) to decoder_rect (top) - L-shape: right then down (ㄱ)
        cnn1_line_start = cnn_rect1.get_right()
        cnn1_line_right_end = cnn1_line_start + RIGHT * 0.8
        cnn1_line_end = decoder_rect.get_top()
        
        cnn1_line_right = Line(cnn1_line_start, cnn1_line_right_end, color=WHITE, stroke_width=2)
        cnn1_line_down = Line(cnn1_line_right_end, cnn1_line_end, color=WHITE, stroke_width=2)
        cnn1_to_decoder = VGroup(cnn1_line_right, cnn1_line_down)
        
        # Draw both lines simultaneously
        decoder_lines = VGroup(algo2_to_decoder, cnn1_to_decoder)
        self.play(Create(decoder_lines), run_time=1.5, lag_ratio=0)
        self.wait(0.5)
        
        # Step 31: Draw five sub-rectangles from decoder_rect
        decoder_sub_rect1 = Rectangle(width=2.2, height=0.6, color=WHITE, fill_opacity=0.3)
        decoder_sub_rect2 = Rectangle(width=2.2, height=0.6, color=WHITE, fill_opacity=0.3)
        decoder_sub_rect3 = Rectangle(width=2.2, height=0.6, color=WHITE, fill_opacity=0.3)
        decoder_sub_rect4 = Rectangle(width=2.2, height=0.6, color=WHITE, fill_opacity=0.3)
        decoder_sub_rect5 = Rectangle(width=2.2, height=0.6, color=WHITE, fill_opacity=0.3)
        
        # Arrange them vertically (rect3 in middle, rect1 and rect2 above, rect4 and rect5 below)
        decoder_sub_rects_group = VGroup(decoder_sub_rect1, decoder_sub_rect2, decoder_sub_rect3, decoder_sub_rect4, decoder_sub_rect5)
        decoder_sub_rects_group.arrange(DOWN, buff=0.3)
        
        # Position the group next to decoder_rect (to the right)
        decoder_sub_rects_group.next_to(decoder_rect, RIGHT, buff=1.0)
        
        # Draw all five rectangles simultaneously
        self.play(Create(decoder_sub_rects_group), run_time=1.5, lag_ratio=0)
        self.wait(0.5)
        
        # Step 32: Draw lines connecting from decoder_rect (right) to each sub-rectangle (left)
        # Line 1: from decoder_rect to decoder_sub_rect1 (right-angle: right, then up, then left)
        dec_line1_start = decoder_rect.get_right()
        dec_line1_right_end = dec_line1_start + RIGHT * 0.8
        dec_line1_up_end = np.array([dec_line1_right_end[0], decoder_sub_rect1.get_center()[1], dec_line1_right_end[2]])
        dec_line1_left_end = decoder_sub_rect1.get_left()
        
        dec_line1_right = Line(dec_line1_start, dec_line1_right_end, color=WHITE, stroke_width=2)
        dec_line1_up = Line(dec_line1_right_end, dec_line1_up_end, color=WHITE, stroke_width=2)
        dec_line1_left = Line(dec_line1_up_end, dec_line1_left_end, color=WHITE, stroke_width=2)
        dec_line1_connection = VGroup(dec_line1_right, dec_line1_up, dec_line1_left)
        
        # Line 2: from decoder_rect to decoder_sub_rect2 (right-angle: right, then up, then left)
        dec_line2_start = decoder_rect.get_right()
        dec_line2_right_end = dec_line2_start + RIGHT * 0.8
        dec_line2_up_end = np.array([dec_line2_right_end[0], decoder_sub_rect2.get_center()[1], dec_line2_right_end[2]])
        dec_line2_left_end = decoder_sub_rect2.get_left()
        
        dec_line2_right = Line(dec_line2_start, dec_line2_right_end, color=WHITE, stroke_width=2)
        dec_line2_up = Line(dec_line2_right_end, dec_line2_up_end, color=WHITE, stroke_width=2)
        dec_line2_left = Line(dec_line2_up_end, dec_line2_left_end, color=WHITE, stroke_width=2)
        dec_line2_connection = VGroup(dec_line2_right, dec_line2_up, dec_line2_left)
        
        # Line 3: from decoder_rect to decoder_sub_rect3 (straight line)
        dec_line3_start = decoder_rect.get_right()
        dec_line3_end = decoder_sub_rect3.get_left()
        dec_line3_connection = Line(dec_line3_start, dec_line3_end, color=WHITE, stroke_width=2)
        
        # Line 4: from decoder_rect to decoder_sub_rect4 (right-angle: right, then down, then left)
        dec_line4_start = decoder_rect.get_right()
        dec_line4_right_end = dec_line4_start + RIGHT * 0.8
        dec_line4_down_end = np.array([dec_line4_right_end[0], decoder_sub_rect4.get_center()[1], dec_line4_right_end[2]])
        dec_line4_left_end = decoder_sub_rect4.get_left()
        
        dec_line4_right = Line(dec_line4_start, dec_line4_right_end, color=WHITE, stroke_width=2)
        dec_line4_down = Line(dec_line4_right_end, dec_line4_down_end, color=WHITE, stroke_width=2)
        dec_line4_left = Line(dec_line4_down_end, dec_line4_left_end, color=WHITE, stroke_width=2)
        dec_line4_connection = VGroup(dec_line4_right, dec_line4_down, dec_line4_left)
        
        # Line 5: from decoder_rect to decoder_sub_rect5 (right-angle: right, then down, then left)
        dec_line5_start = decoder_rect.get_right()
        dec_line5_right_end = dec_line5_start + RIGHT * 0.8
        dec_line5_down_end = np.array([dec_line5_right_end[0], decoder_sub_rect5.get_center()[1], dec_line5_right_end[2]])
        dec_line5_left_end = decoder_sub_rect5.get_left()
        
        dec_line5_right = Line(dec_line5_start, dec_line5_right_end, color=WHITE, stroke_width=2)
        dec_line5_down = Line(dec_line5_right_end, dec_line5_down_end, color=WHITE, stroke_width=2)
        dec_line5_left = Line(dec_line5_down_end, dec_line5_left_end, color=WHITE, stroke_width=2)
        dec_line5_connection = VGroup(dec_line5_right, dec_line5_down, dec_line5_left)
        
        # Draw all lines simultaneously
        decoder_sub_lines = VGroup(dec_line1_connection, dec_line2_connection, dec_line3_connection, dec_line4_connection, dec_line5_connection)
        self.play(Create(decoder_sub_lines), run_time=1.5, lag_ratio=0)
        self.wait(0.5)
        
        # Step 33: Write text in each rectangle
        decoder_sub_text1 = Text("ACT", font_size=14, color=WHITE)
        decoder_sub_text1.move_to(decoder_sub_rect1.get_center())
        
        decoder_sub_text2 = Text("ActionTransformer", font_size=12, color=WHITE)
        decoder_sub_text2.move_to(decoder_sub_rect2.get_center())
        
        decoder_sub_text3 = Text("Conditional Unet Decoder", font_size=12, color=WHITE)
        decoder_sub_text3.move_to(decoder_sub_rect3.get_center())
        
        decoder_sub_text4 = Text("FASTDER Decoder", font_size=12, color=WHITE)
        decoder_sub_text4.move_to(decoder_sub_rect4.get_center())
        
        decoder_sub_text5 = Text("PhaseACT", font_size=14, color=WHITE)
        decoder_sub_text5.move_to(decoder_sub_rect5.get_center())
        
        # Write all texts simultaneously
        self.play(
            Write(decoder_sub_text1),
            Write(decoder_sub_text2),
            Write(decoder_sub_text3),
            Write(decoder_sub_text4),
            Write(decoder_sub_text5),
            run_time=1.5,
            lag_ratio=0
        )
        self.wait(0.5)
        
        # Change dec_line3 color to YELLOW
        self.play(
            dec_line3_connection.animate.set_color(YELLOW),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Step 34: Zoom out and move camera perspective to the left
        all_visible = VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)])
        self.play(all_visible.animate.scale(0.5).shift(DOWN * 1.5 + RIGHT * 1.5), run_time=1.5)
        self.wait(0.5)
        
        # Step 35: Draw arrow line from right of decoder_sub_rect3
        predicted_arrow_start = decoder_sub_rect3.get_right()
        predicted_arrow_end = predicted_arrow_start + RIGHT * 1.0
        predicted_arrow = Arrow(predicted_arrow_start, predicted_arrow_end, color=WHITE, stroke_width=2, buff=0)
        
        self.play(Create(predicted_arrow), run_time=1.0)
        self.wait(0.5)
        
        # Step 36: Write text "predicted action sequences" next to the arrow
        predicted_text = Text("predicted action sequences", font_size=14, color=WHITE)
        predicted_text.next_to(predicted_arrow, RIGHT, buff=0.3)
        
        self.play(Write(predicted_text), run_time=1.0)
        self.wait(0.5)
        
        # Hold the final frame for a long time so it remains visible
        # This prevents the video from ending abruptly
        self.wait(5)
        
