from manim import *
import numpy as np

class ThreeRectanglesExtended(Scene):
    """
    Example showing three rectangles at the center of the screen.
    """
    
    def construct(self):
        # Create three rectangles (increased height to fit text)
        rect1 = Rectangle(
            width=2.5,
            height=2.0,
            color=DARKER_GREY,
            fill_opacity=0.3
        )
        
        rect2 = Rectangle(
            width=2.5,
            height=2.0,
            color=DARK_GRAY,
            fill_opacity=0.3
        )
        
        rect3 = Rectangle(
            width=2.5,
            height=2.0,
            color=GRAY_E,
            fill_opacity=0.3
        )
        
        # Arrange them horizontally at the center
        rectangles = VGroup(rect1, rect2, rect3)
        rectangles.arrange(RIGHT, buff=3.0)  # Arrange horizontally with spacing
        rectangles.move_to(ORIGIN + UP * 1.5)  # Center on screen
        
        # Step 1: Create initial "declare_parameter" text inside each rectangle
        declare_text1 = Text("declare parameter", font_size=14, color=WHITE)
        declare_text1.move_to(rect1.get_center())
        
        declare_text2 = Text("declare parameter", font_size=14, color=WHITE)
        declare_text2.move_to(rect2.get_center())
        
        declare_text3 = Text("declare parameter", font_size=14, color=WHITE)
        declare_text3.move_to(rect3.get_center())
        
        # Step 2: Create target parameter texts for conversion
        # Rectangle 1: param_1 and param_2 (2 lines)
        text1_line1 = Text("param_1 = tip_pose", font_size=18, color=WHITE)
        text1_line2 = Text("param_2 = 0.5", font_size=18, color=WHITE)
        text1_group = VGroup(text1_line1, text1_line2)
        text1_group.arrange(DOWN, buff=0.3)
        text1_group.move_to(rect1.get_center())
        
        # Rectangle 2: param_3, param_4, param_5 (3 lines)
        text2_line1 = Text("param_3 = 0.05", font_size=18, color=WHITE)
        text2_line2 = Text("param_4 = 0.005", font_size=18, color=WHITE)
        text2_line3 = Text("param_5 = 5", font_size=18, color=WHITE)
        text2_group = VGroup(text2_line1, text2_line2, text2_line3)
        text2_group.arrange(DOWN, buff=0.3)
        text2_group.move_to(rect2.get_center())
        
        # Rectangle 3: param6 (1 line)
        text3 = Text("param_6 = [5, 5, 5]", font_size=18, color=WHITE)
        text3.move_to(rect3.get_center())
        
        # Create initial "get parameter" text labels below the rectangles
        text4 = Text("get parameter", font_size=18, color=WHITE)
        text4.next_to(rect1, DOWN, buff=0.5)
        
        text5 = Text("get parameter", font_size=18, color=WHITE)
        text5.next_to(rect2, DOWN, buff=0.5)
        
        text6 = Text("get parameter", font_size=18, color=WHITE)
        text6.next_to(rect3, DOWN, buff=0.5)
        
        # Create target text strings for conversion from "get parameter"
        # Rectangle 1: var_1 = param_1, var_2 = param_2 (2 lines)
        text4_target_line1 = Text("var_1 = get_parameter(param_1)", font_size=15, color=WHITE)
        text4_target_line2 = Text("var_2 = get_parameter(param_2)", font_size=15, color=WHITE)
        text4_target = VGroup(text4_target_line1, text4_target_line2)
        text4_target.arrange(DOWN, buff=0.3)
        text4_target.next_to(rect1, DOWN, buff=0.5)
        
        # Rectangle 2: var_3 = param_3, var_4 = param_4, var_5 = param_5 (3 lines)
        text5_target_line1 = Text("var_3 = get_parameter(param_3)", font_size=15, color=WHITE)
        text5_target_line2 = Text("var_4 = get_parameter(param_4)", font_size=15, color=WHITE)
        text5_target_line3 = Text("var_5 = get_parameter(param_5)", font_size=15, color=WHITE)
        text5_target_line4 = Text("-", font_size=15, color=WHITE)
        text5_target = VGroup(text5_target_line1, text5_target_line2, text5_target_line3, text5_target_line4)
        text5_target.arrange(DOWN, buff=0.3)
        text5_target.next_to(rect2, DOWN, buff=0.5)
        
        # Rectangle 3: var_6 = param6 (1 line)
        text6_target_line1 = Text("var_6 = get_parameter(param_6)", font_size=15, color=WHITE)
        text6_target_line2 = Text("-", font_size=15, color=WHITE)
        text6_target = VGroup(text6_target_line1, text6_target_line2)
        text6_target.arrange(DOWN, buff=0.3)
        text6_target.next_to(rect3, DOWN, buff=0.5)
        
        # Group texts together
        declare_texts = VGroup(declare_text1, declare_text2, declare_text3)
        param_texts = VGroup(text1_group, text2_group, text3)
        texts2 = VGroup(text4, text5, text6)
        texts2_target = VGroup(text4_target, text5_target, text6_target)
        
        # Animate: Create rectangles first
        self.play(Create(rectangles), run_time=2.0)
        
        # Show "declare_parameter" text in each rectangle
        self.play(Write(declare_texts), run_time=2.0, lag_ratio=0)
        self.wait(0.5)
        
        # Convert "declare_parameter" to parameter lists
        self.play(
            ReplacementTransform(declare_text1, text1_group),
            ReplacementTransform(declare_text2, text2_group),
            ReplacementTransform(declare_text3, text3),
            run_time=2.0
        )
        self.wait(0.5)
        
        # Show "get parameter" texts below
        self.play(Write(texts2), run_time=2.0, lag_ratio=0)
        self.wait(0.5)
        
        # Convert "get parameter" to parameter-specific strings
        self.play(
            ReplacementTransform(text4, text4_target),
            ReplacementTransform(text5, text5_target),
            ReplacementTransform(text6, text6_target),
            run_time=2.0
        )
        self.wait(0.5)
        
        # Create curved arrows connecting parameters to variables
        # Arrow 1: from text1_line1 (param_1 in rect1) to text5_target_line3 (var_5 below rect2)
        arrow1_start = text1_line1.get_right() + RIGHT * 0.2
        arrow1_end = text5_target_line4.get_left()
        # Create curved arrow using ArcBetweenPoints and add arrow tip
        arc1 = ArcBetweenPoints(arrow1_start, arrow1_end, angle=PI/2, color=GRAY_A, stroke_width=2)
        arrow1 = arc1.add_tip(at_start=False)
        
        # Arrow 2: from text2_line2 (param_4 in rect2) to text6_target (var_6 below rect3)
        arrow2_start = text2_line2.get_right() + RIGHT * 0.2
        arrow2_end = text6_target_line2.get_left()
        arc2 = ArcBetweenPoints(arrow2_start, arrow2_end, angle=PI/2, color=GRAY_A, stroke_width=2)
        arrow2 = arc2.add_tip(at_start=False)
        
        # Create text labels above arrows
        ros_text1 = Text("ROS Service", font_size=14, color=WHITE)
        ros_text1.next_to(arrow1_end, DOWN, buff=0.3)
        
        ros_text2 = Text("ROS Service", font_size=14, color=WHITE)
        ros_text2.next_to(arrow2_end, DOWN, buff=0.3)
        
        # Animate arrows appearing
        self.play(Create(arrow1), Create(arrow2), run_time=1.5)
        # Animate text labels appearing
        self.play(Write(ros_text1), Write(ros_text2), run_time=1.0)
        self.wait(1)
        
        # Remove arrows and ROS Service labels
        self.play(
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(ros_text1),
            FadeOut(ros_text2),
            FadeOut(text4_target),
            FadeOut(text5_target),
            FadeOut(text6_target),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Rearrange rectangles with closer spacing (buff=1.5)
        # Save current positions
        rect1_start = rect1.get_center()
        rect2_start = rect2.get_center()
        rect3_start = rect3.get_center()
        
        # Calculate target positions with buff=1.5
        rectangles.arrange(RIGHT, buff=1.5)
        rectangles.move_to(ORIGIN + UP * 1.5)
        
        # Get final positions
        rect1_final = rect1.get_center()
        rect2_final = rect2.get_center()
        rect3_final = rect3.get_center()
        
        # Reset to original positions for animation
        rectangles.arrange(RIGHT, buff=3.0)
        rect1.move_to(rect1_start)
        rect2.move_to(rect2_start)
        rect3.move_to(rect3_start)
        rectangles.move_to(ORIGIN + UP * 1.5)
        
        # Animate to new positions
        self.play(
            rect1.animate.move_to(rect1_final),
            rect2.animate.move_to(rect2_final),
            rect3.animate.move_to(rect3_final),
            text1_group.animate.move_to(rect1_final),
            text2_group.animate.move_to(rect2_final),
            text3.animate.move_to(rect3_final),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Zoom out to show more space in the screen by scaling all objects down
        # Also move camera perspective to the left and up (shift objects right and down)
        # Filter only VMobjects for VGroup
        vmobjects = [mob for mob in self.mobjects if isinstance(mob, VMobject)]
        if vmobjects:
            all_visible = VGroup(*vmobjects)
            # Shift right and down to move camera left and up
            camera_shift = RIGHT * 2 + DOWN * 2
            self.play(
                all_visible.animate.scale(0.7).shift(camera_shift),
                run_time=1.5
            )
        self.wait(0.5)
        
        # Create a new rectangle to the left and up next to rect1
        new_rect = Rectangle(
            width=2.5,
            height=2.5,
            color=GRAY_D,
            fill_opacity=0.3
        )
        # Position it to the left and up from rect1
        new_rect.next_to(rect1, LEFT, buff=1.0)
        # Move it down a bit more from center
        new_rect.shift(DOWN * 0.5)
        
        # Create "YAML" text above the rectangle
        yaml_text = Text("YAML", font_size=16, color=WHITE)
        yaml_text.next_to(new_rect, UP, buff=0.3)
        
        # Create the rectangle and text
        self.play(Create(new_rect), Write(yaml_text), run_time=1.5)
        self.wait(0.5)
        
        # Move text groups into the new rectangle (arranged vertically)
        self.play(
            text1_group.animate.move_to(new_rect.get_center() + UP * 0.8),
            text2_group.animate.move_to(new_rect.get_center()),
            text3.animate.move_to(new_rect.get_center() + DOWN * 0.6),
            run_time=2.0
        )
        self.wait(0.5)

        # Before creating the rectangle, please move the camera up a bit.
        # Shift all objects down to simulate camera moving up
        vmobjects = [mob for mob in self.mobjects if isinstance(mob, VMobject)]
        if vmobjects:
            all_visible = VGroup(*vmobjects)
            # Shift down to move camera up
            self.play(all_visible.animate.shift(UP * 1.0), run_time=1.5)
        self.wait(0.5)
        
        # Create another rectangle below new_rect
        param_retriever_rect = Rectangle(
            width=2.5,
            height=1.0,
            color=YELLOW,
            fill_opacity=0.3
        )
        # Position it below new_rect
        param_retriever_rect.next_to(new_rect, DOWN, buff=0.5)
        
        # Add text "parameter_retriever" inside the rectangle
        param_retriever_text = Text("Parameter Retriever", font_size=16, color=WHITE)
        param_retriever_text.move_to(param_retriever_rect.get_center())
        
        # Create and show the rectangle and text
        self.play(Create(param_retriever_rect), Write(param_retriever_text), run_time=1.5)
        self.wait(0.5)
        
        # Connect param_retriever_rect with rect1, rect2, and rect3 using right-angle arrows
        # Arrow 1: horizontal then vertical (90 degree turn)
        arrow1_start = param_retriever_rect.get_right()
        arrow1_mid = np.array([rect1.get_bottom()[0], arrow1_start[1], 0])
        arrow1_end = rect1.get_bottom()
        arrow1_horizontal = Line(arrow1_start, arrow1_mid, color=WHITE, stroke_width=2)
        arrow1_vertical = Arrow(arrow1_mid, arrow1_end, color=WHITE, stroke_width=2, buff=0)
        arrow_to_rect1 = VGroup(arrow1_horizontal, arrow1_vertical)
        
        # Arrow 2: horizontal then vertical (90 degree turn)
        arrow2_start = param_retriever_rect.get_right()
        arrow2_mid = np.array([rect2.get_bottom()[0], arrow2_start[1], 0])
        arrow2_end = rect2.get_bottom()
        arrow2_horizontal = Line(arrow2_start, arrow2_mid, color=WHITE, stroke_width=2)
        arrow2_vertical = Arrow(arrow2_mid, arrow2_end, color=WHITE, stroke_width=2, buff=0)
        arrow_to_rect2 = VGroup(arrow2_horizontal, arrow2_vertical)
        
        # Arrow 3: horizontal then vertical (90 degree turn)
        arrow3_start = param_retriever_rect.get_right()
        arrow3_mid = np.array([rect3.get_bottom()[0], arrow3_start[1], 0])
        arrow3_end = rect3.get_bottom()
        arrow3_horizontal = Line(arrow3_start, arrow3_mid, color=WHITE, stroke_width=2)
        arrow3_vertical = Arrow(arrow3_mid, arrow3_end, color=WHITE, stroke_width=2, buff=0)
        arrow_to_rect3 = VGroup(arrow3_horizontal, arrow3_vertical)
        
        # Animate arrows appearing
        self.play(
            Create(arrow_to_rect1),
            Create(arrow_to_rect2),
            Create(arrow_to_rect3),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Move text groups down a little bit
        self.play(
            text1_group.animate.shift(DOWN * 0.3),
            text2_group.animate.shift(DOWN * 0.3),
            text3.animate.shift(DOWN * 0.3),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Add "namespace" text in new_rect at top and left
        namespace_text = Text("namespace", font_size=14, color=WHITE)
        namespace_text.move_to(new_rect.get_corner(UL) + RIGHT * 0.7 + DOWN * 0.35)
        self.play(Write(namespace_text), run_time=1.0)
        self.wait(0.5)
        
        # Add "retriever_parameter" text above rect1, rect2, and rect3
        retriever_text1 = Text("retriever_parameter", font_size=14, color=WHITE)
        retriever_text1.next_to(rect1, UP, buff=0.3)
        
        retriever_text2 = Text("retriever_parameter", font_size=14, color=WHITE)
        retriever_text2.next_to(rect2, UP, buff=0.3)
        
        retriever_text3 = Text("retriever_parameter", font_size=14, color=WHITE)
        retriever_text3.next_to(rect3, UP, buff=0.3)
        
        self.play(
            Write(retriever_text1),
            Write(retriever_text2),
            Write(retriever_text3),
            run_time=1.5,
            lag_ratio=0
        )
        self.wait(0.5)
        
        # Copy text1_group, text2_group, text3 and place copies in rect1, rect2, and rect3
        # Create copies of the text groups
        text1_group_copy = text1_group.copy()
        text2_group_copy = text2_group.copy()
        text3_copy = text3.copy()
        
        # Add the copies to the scene (they'll start at the same position as originals)
        self.add(text1_group_copy, text2_group_copy, text3_copy)
        
        
        # Animate copies moving to their respective rectangles (originals stay in new_rect)
        self.play(
            text1_group_copy.animate.move_to(rect1.get_center()),
            text2_group_copy.animate.move_to(rect2.get_center()),
            text3_copy.animate.move_to(rect3.get_center()),
            run_time=2.0
        )
        self.wait(1)

        # Add "default_value" text above retriever_text3
        default_value_text = Text("default_value", font_size=12, color=RED)
        default_value_text.next_to(retriever_text3, UP, buff=0.2)
        self.play(Write(default_value_text), run_time=1.0)
        self.wait(0.5)
        
        # Move "default_value" next to retriever_text3 (to the right)
        self.play(
            default_value_text.animate.next_to(retriever_text3, RIGHT + UP * 0.2, buff=0.3),
            text3_copy.animate.next_to(retriever_text3, RIGHT, buff=0.3),
            run_time=1.0
        )
        self.wait(0.3)
        
        # Fade out both texts
        self.play(
            FadeOut(default_value_text),
            FadeOut(text3_copy),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Change text3_copy to "var_6" and set color to RED
        text3_copy_new = Text("var_6", font_size=16, color=WHITE)
        text3_copy_new.move_to(rect3.get_center())
        
        # Add and show text3_copy_new in rect3
        self.play(Write(text3_copy_new), run_time=1.0)
        self.wait(0.5)
        
        # Transform text1_group_copy and text2_group_copy into variable names
        # Create new text groups with variable names
        # text1_group_copy: param_1, param_2 -> var_1, var_2
        var1_line1 = Text("var_1", font_size=16, color=WHITE)
        var1_line2 = Text("var_2", font_size=16, color=WHITE)
        text1_group_copy_new = VGroup(var1_line1, var1_line2)
        text1_group_copy_new.arrange(DOWN, buff=0.3)
        text1_group_copy_new.move_to(text1_group_copy.get_center())
        
        # text2_group_copy: param_3, param_4, param_5 -> var_3, var_4, var_5
        var2_line1 = Text("var_3", font_size=16, color=WHITE)
        var2_line2 = Text("var_4", font_size=16, color=WHITE)
        var2_line3 = Text("var_5", font_size=16, color=WHITE)
        text2_group_copy_new = VGroup(var2_line1, var2_line2, var2_line3)
        text2_group_copy_new.arrange(DOWN, buff=0.3)
        text2_group_copy_new.move_to(text2_group_copy.get_center())
        
        # Transform the text groups
        self.play(
            ReplacementTransform(text1_group_copy, text1_group_copy_new),
            ReplacementTransform(text2_group_copy, text2_group_copy_new),
            run_time=2.0
        )
        self.wait(0.5)
        
        # Zoom out to make more space and move camera right and down
        # Shift objects left and up to simulate camera moving right and down
        vmobjects = [mob for mob in self.mobjects if isinstance(mob, VMobject)]
        if vmobjects:
            all_visible = VGroup(*vmobjects)
            camera_shift = LEFT * 3.5 + UP * 2
            self.play(
                all_visible.animate.scale(0.5).shift(camera_shift),
                run_time=1.5
            )
        self.wait(0.5)
        
        
        
        
        # new_rect2: below, contains param_2, param_3, param_4, param_5
        new_rect2 = Rectangle(
            width=2.5,
            height=2.5,
            color=PURE_BLUE,
            fill_opacity=0.3
        )
        new_rect2.next_to(new_rect, DOWN , buff=1.0)
        
        
        # new_rect3: bottom right, contains param_6
        new_rect3 = Rectangle(
            width=2.5,
            height=2.5,
            color=PURE_GREEN,
            fill_opacity=0.3
        )
        new_rect3.next_to(new_rect2, RIGHT * 4, buff=1.0)

        # Create new rectangles with parameter texts
        # new_rect1: to the right, contains param_1
        new_rect1 = Rectangle(
            width=2.5,
            height=2.5,
            color=PURE_RED,
            fill_opacity=0.3
        )
        new_rect1.next_to(new_rect3, UP + DOWN *0.07, buff=1.0)
        
        # Apply the same shift that new_rect received (DOWN * 0.5 after first zoom)
        # Since new_rect was shifted DOWN * 0.5 after 0.7 scale, then scaled by 0.5 in the second zoom,
        # the visual shift in the final coordinate system is DOWN * 0.5 * 0.5 = DOWN * 0.25
        # However, since new_rect1, new_rect2, new_rect3 are created after the second zoom,
        # we need to apply the shift in the current coordinate system
        # The shift should be DOWN * 0.5 to match new_rect's original shift amount
        new_rect1.shift(DOWN * 0.5)
        new_rect2.shift(DOWN * 0.5)
        new_rect3.shift(DOWN * 0.5)
        
        # Scale the new rectangles to match the current scale of rect1, rect2, rect3
        new_rect1.scale(0.5)
        new_rect2.scale(0.5)
        new_rect3.scale(0.5)
        
        # Create "YAML 1", "YAML 2", "YAML 3" text above each rectangle
        yaml_text1 = Text("YAML 1", font_size=24, color=WHITE)
        yaml_text1.next_to(new_rect1, UP, buff=0.1)
        yaml_text1.scale(0.5)  # Scale to match the rectangles
        
        yaml_text2 = Text("YAML 2", font_size=24, color=WHITE)
        yaml_text2.next_to(new_rect2, UP, buff=0.1)
        yaml_text2.scale(0.5)  # Scale to match the rectangles
        
        yaml_text3 = Text("YAML 3", font_size=24, color=WHITE)
        yaml_text3.next_to(new_rect3, UP, buff=0.1)
        yaml_text3.scale(0.5)  # Scale to match the rectangles
        
        # Draw all three rectangles and their texts simultaneously
        self.play(
            Create(new_rect1),
            Create(new_rect2),
            Create(new_rect3),
            Write(yaml_text1),
            Write(yaml_text2),
            Write(yaml_text3),
            run_time=2.0,
            lag_ratio=0
        )
        self.wait(0.5)
        
        # Draw three rectangles next to each new_rect, similar to rect1, rect2, rect3 next to new_rect
        
        # Three rectangles next to new_rect1 (match scale of rect1)
        new_rect1_group1 = Rectangle(width=2.5, height=2.0, color=LOGO_BLUE, fill_opacity=0.3)
        new_rect1_group2 = Rectangle(width=2.5, height=2.0, color=LOGO_BLUE, fill_opacity=0.3)
        new_rect1_group3 = Rectangle(width=2.5, height=2.0, color=RED_D, fill_opacity=0.3)
        new_rect1_rects = VGroup(new_rect1_group1, new_rect1_group2, new_rect1_group3)
        new_rect1_rects.arrange(RIGHT, buff=1.5)  # Original buff value (same as rectangles)
        new_rect1_rects.scale(0.35)  # Scale to match rect1's current scale
        new_rect1_rects.next_to(rectangles, RIGHT * 6, buff=1.0 * 0.5)  # Scale the buff too
        
        # Three rectangles next to new_rect2 (match scale of rect2)
        new_rect2_group1 = Rectangle(width=2.5, height=2.0, color=RED_D, fill_opacity=0.3)
        new_rect2_group2 = Rectangle(width=2.5, height=2.0, color=RED_D, fill_opacity=0.3)
        new_rect2_group3 = Rectangle(width=2.5, height=2.0, color=PURPLE_D, fill_opacity=0.3)
        new_rect2_rects = VGroup(new_rect2_group1, new_rect2_group2, new_rect2_group3)
        new_rect2_rects.arrange(RIGHT, buff=1.5)  # Original buff value (same as rectangles)
        new_rect2_rects.scale(0.35)  # Scale to match rect2's current scale
        new_rect2_rects.next_to(rectangles, DOWN * 5.3, buff=1.0 * 0.5)  # Scale the buff too
        
        # Three rectangles next to new_rect3 (match scale of rect3)
        new_rect3_group1 = Rectangle(width=2.5, height=2.0, color=RED_D, fill_opacity=0.3)
        new_rect3_group2 = Rectangle(width=2.5, height=2.0, color=LOGO_BLUE, fill_opacity=0.3)
        new_rect3_group3 = Rectangle(width=2.5, height=2.0, color=PURPLE_D, fill_opacity=0.3)
        new_rect3_rects = VGroup(new_rect3_group1, new_rect3_group2, new_rect3_group3)
        new_rect3_rects.arrange(RIGHT, buff=1.5)  # Original buff value (same as rectangles)
        new_rect3_rects.scale(0.35)  # Scale to match rect3's current scale
        new_rect3_rects.next_to(new_rect2_rects, RIGHT * 6, buff=1.0 * 0.5)  # Scale the buff too
        
        # Draw all three groups of rectangles simultaneously
        self.play(
            Create(new_rect1_rects),
            Create(new_rect2_rects),
            Create(new_rect3_rects),
            run_time=2.0,
            lag_ratio=0
        )
        self.wait(0.5)
        
        param_retriever_rect1 = Rectangle(
            width=2.5,
            height=1.0,
            color=YELLOW,
            fill_opacity=0.3
        )
        # Since new_rect1 is already scaled, and we'll scale param_retriever_rect1 too,
        # use buff = original_param_buff / scale_factor to get correct visual spacing
        param_retriever_rect1.next_to(new_rect1, DOWN, buff=0.05)
        param_retriever_rect1.scale(0.5)
        param_retriever_text1 = Text("parameter_retriever", font_size=16, color=WHITE)
        param_retriever_text1.scale(0.5)
        param_retriever_text1.move_to(param_retriever_rect1.get_center())
        
        # param_retriever_rect2 below new_rect2 (match original buff and scale)
        param_retriever_rect2 = Rectangle(
            width=2.5,
            height=1.0,
            color=YELLOW,
            fill_opacity=0.3
        )
        param_retriever_rect2.next_to(new_rect2, DOWN, buff=0.05)
        param_retriever_rect2.scale(0.5)
        param_retriever_text2 = Text("parameter_retriever", font_size=16, color=WHITE)
        param_retriever_text2.scale(0.5)
        param_retriever_text2.move_to(param_retriever_rect2.get_center())
        
        # param_retriever_rect3 below new_rect3 (match original buff and scale)
        param_retriever_rect3 = Rectangle(
            width=2.5,
            height=1.0,
            color=YELLOW,
            fill_opacity=0.3 
        )
        param_retriever_rect3.next_to(new_rect3, DOWN, buff=0.05)
        param_retriever_rect3.scale(0.5)
        param_retriever_text3 = Text("parameter_retriever", font_size=16, color=WHITE)
        param_retriever_text3.scale(0.5)
        param_retriever_text3.move_to(param_retriever_rect3.get_center())
        
        # Create and show all param_retriever rectangles and texts
        self.play(
            Create(param_retriever_rect1),
            Create(param_retriever_rect2),
            Create(param_retriever_rect3),
            Write(param_retriever_text1),
            Write(param_retriever_text2),
            Write(param_retriever_text3),
            run_time=1.5,
            lag_ratio=0
        )

        self.wait(0.5)
        
        # Connect each param_retriever_rect to its three rectangles using right-angle arrows
        # Connections for param_retriever_rect1
        pr1_arrow1_start = param_retriever_rect1.get_right()
        pr1_arrow1_mid = np.array([new_rect1_group1.get_bottom()[0], pr1_arrow1_start[1], 0])
        pr1_arrow1_end = new_rect1_group1.get_bottom()
        pr1_arrow1_h = Line(pr1_arrow1_start, pr1_arrow1_mid, color=WHITE, stroke_width=2)
        pr1_arrow1_v = Arrow(pr1_arrow1_mid, pr1_arrow1_end, color=WHITE, stroke_width=2, buff=0)
        pr1_arrow_to_group1 = VGroup(pr1_arrow1_h, pr1_arrow1_v)
        
        pr1_arrow2_start = param_retriever_rect1.get_right()
        pr1_arrow2_mid = np.array([new_rect1_group2.get_bottom()[0], pr1_arrow2_start[1], 0])
        pr1_arrow2_end = new_rect1_group2.get_bottom()
        pr1_arrow2_h = Line(pr1_arrow2_start, pr1_arrow2_mid, color=WHITE, stroke_width=2)
        pr1_arrow2_v = Arrow(pr1_arrow2_mid, pr1_arrow2_end, color=WHITE, stroke_width=2, buff=0)
        pr1_arrow_to_group2 = VGroup(pr1_arrow2_h, pr1_arrow2_v)
        
        pr1_arrow3_start = param_retriever_rect1.get_right()
        pr1_arrow3_mid = np.array([new_rect1_group3.get_bottom()[0], pr1_arrow3_start[1], 0])
        pr1_arrow3_end = new_rect1_group3.get_bottom()
        pr1_arrow3_h = Line(pr1_arrow3_start, pr1_arrow3_mid, color=WHITE, stroke_width=2)
        pr1_arrow3_v = Arrow(pr1_arrow3_mid, pr1_arrow3_end, color=WHITE, stroke_width=2, buff=0)
        pr1_arrow_to_group3 = VGroup(pr1_arrow3_h, pr1_arrow3_v)
        
        # Connections for param_retriever_rect2
        pr2_arrow1_start = param_retriever_rect2.get_right()
        pr2_arrow1_mid = np.array([new_rect2_group1.get_bottom()[0], pr2_arrow1_start[1], 0])
        pr2_arrow1_end = new_rect2_group1.get_bottom()
        pr2_arrow1_h = Line(pr2_arrow1_start, pr2_arrow1_mid, color=WHITE, stroke_width=2)
        pr2_arrow1_v = Arrow(pr2_arrow1_mid, pr2_arrow1_end, color=WHITE, stroke_width=2, buff=0)
        pr2_arrow_to_group1 = VGroup(pr2_arrow1_h, pr2_arrow1_v)
        
        pr2_arrow2_start = param_retriever_rect2.get_right()
        pr2_arrow2_mid = np.array([new_rect2_group2.get_bottom()[0], pr2_arrow2_start[1], 0])
        pr2_arrow2_end = new_rect2_group2.get_bottom()
        pr2_arrow2_h = Line(pr2_arrow2_start, pr2_arrow2_mid, color=WHITE, stroke_width=2)
        pr2_arrow2_v = Arrow(pr2_arrow2_mid, pr2_arrow2_end, color=WHITE, stroke_width=2, buff=0)
        pr2_arrow_to_group2 = VGroup(pr2_arrow2_h, pr2_arrow2_v)
        
        pr2_arrow3_start = param_retriever_rect2.get_right()
        pr2_arrow3_mid = np.array([new_rect2_group3.get_bottom()[0], pr2_arrow3_start[1], 0])
        pr2_arrow3_end = new_rect2_group3.get_bottom()
        pr2_arrow3_h = Line(pr2_arrow3_start, pr2_arrow3_mid, color=WHITE, stroke_width=2)
        pr2_arrow3_v = Arrow(pr2_arrow3_mid, pr2_arrow3_end, color=WHITE, stroke_width=2, buff=0)
        pr2_arrow_to_group3 = VGroup(pr2_arrow3_h, pr2_arrow3_v)
        
        # Connections for param_retriever_rect3
        pr3_arrow1_start = param_retriever_rect3.get_right()
        pr3_arrow1_mid = np.array([new_rect3_group1.get_bottom()[0], pr3_arrow1_start[1], 0])
        pr3_arrow1_end = new_rect3_group1.get_bottom()
        pr3_arrow1_h = Line(pr3_arrow1_start, pr3_arrow1_mid, color=WHITE, stroke_width=2)
        pr3_arrow1_v = Arrow(pr3_arrow1_mid, pr3_arrow1_end, color=WHITE, stroke_width=2, buff=0)
        pr3_arrow_to_group1 = VGroup(pr3_arrow1_h, pr3_arrow1_v)
        
        pr3_arrow2_start = param_retriever_rect3.get_right()
        pr3_arrow2_mid = np.array([new_rect3_group2.get_bottom()[0], pr3_arrow2_start[1], 0])
        pr3_arrow2_end = new_rect3_group2.get_bottom()
        pr3_arrow2_h = Line(pr3_arrow2_start, pr3_arrow2_mid, color=WHITE, stroke_width=2)
        pr3_arrow2_v = Arrow(pr3_arrow2_mid, pr3_arrow2_end, color=WHITE, stroke_width=2, buff=0)
        pr3_arrow_to_group2 = VGroup(pr3_arrow2_h, pr3_arrow2_v)
        
        pr3_arrow3_start = param_retriever_rect3.get_right()
        pr3_arrow3_mid = np.array([new_rect3_group3.get_bottom()[0], pr3_arrow3_start[1], 0])
        pr3_arrow3_end = new_rect3_group3.get_bottom()
        pr3_arrow3_h = Line(pr3_arrow3_start, pr3_arrow3_mid, color=WHITE, stroke_width=2)
        pr3_arrow3_v = Arrow(pr3_arrow3_mid, pr3_arrow3_end, color=WHITE, stroke_width=2, buff=0)
        pr3_arrow_to_group3 = VGroup(pr3_arrow3_h, pr3_arrow3_v)
        
        # Animate all arrows appearing simultaneously
        self.play(
            Create(pr1_arrow_to_group1),
            Create(pr1_arrow_to_group2),
            Create(pr1_arrow_to_group3),
            Create(pr2_arrow_to_group1),
            Create(pr2_arrow_to_group2),
            Create(pr2_arrow_to_group3),
            Create(pr3_arrow_to_group1),
            Create(pr3_arrow_to_group2),
            Create(pr3_arrow_to_group3),
            run_time=2.0,
            lag_ratio=0
        )
        self.wait(1)
        
        # Add text labels to the center of each rectangle
        # new_rect1 groups
        text1_group1 = Text("A", font_size=32, color=WHITE)
        text1_group1.move_to(new_rect1_group1.get_center())
        text1_group1.scale(0.35)  # Scale to match the rectangles
        
        text1_group2 = Text("A", font_size=32, color=WHITE)
        text1_group2.move_to(new_rect1_group2.get_center())
        text1_group2.scale(0.35)
        
        text1_group3 = Text("B", font_size=32, color=WHITE)
        text1_group3.move_to(new_rect1_group3.get_center())
        text1_group3.scale(0.35)
        
        # new_rect2 groups
        text2_group1 = Text("B", font_size=32, color=WHITE)
        text2_group1.move_to(new_rect2_group1.get_center())
        text2_group1.scale(0.35)
        
        text2_group2 = Text("B", font_size=32, color=WHITE)
        text2_group2.move_to(new_rect2_group2.get_center())
        text2_group2.scale(0.35)
        
        text2_group3 = Text("C", font_size=32, color=WHITE)
        text2_group3.move_to(new_rect2_group3.get_center())
        text2_group3.scale(0.35)
        
        # new_rect3 groups
        text3_group1 = Text("B", font_size=32, color=WHITE)
        text3_group1.move_to(new_rect3_group1.get_center())
        text3_group1.scale(0.35)
        
        text3_group2 = Text("A", font_size=32, color=WHITE)
        text3_group2.move_to(new_rect3_group2.get_center())
        text3_group2.scale(0.35)
        
        text3_group3 = Text("C", font_size=32, color=WHITE)
        text3_group3.move_to(new_rect3_group3.get_center())
        text3_group3.scale(0.35)
        
        # Write all texts simultaneously
        self.play(
            Write(text1_group1),
            Write(text1_group2),
            Write(text1_group3),
            Write(text2_group1),
            Write(text2_group2),
            Write(text2_group3),
            Write(text3_group1),
            Write(text3_group2),
            Write(text3_group3),
            run_time=1.5,
            lag_ratio=0
        )
        self.wait(0.5)
        
        # Hold the final frame for a long time so it remains visible
        # This prevents the video from ending abruptly
        self.wait(5)

        