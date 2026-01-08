from manim import *
import numpy as np


class TimestepDiffusion(ThreeDScene):
    """
    Visualization showing diffusion timestep process with hexahedron and formulas.
    Timestep range is 0 to 100 (not 0.0 to 1.0).
    """
    
    def construct(self):
        # Define dimensions
        width = 10  # Represents timestep range 0 to 100
        height = 2
        depth = 2
        
        # Create hexahedron (3D box) using Cube and scale it
        hexahedron = Cube(side_length=1, fill_opacity=0.2, fill_color=BLUE, stroke_width=2)
        hexahedron.scale([width, height, depth])
        
        # Rotate hexahedron 
        hexahedron.rotate_about_origin(1 * DEGREES, axis=[0, 0, 1])
        hexahedron.rotate_about_origin(75 * DEGREES, axis=[0, 1, 0])
        hexahedron.rotate_about_origin(10 * DEGREES, axis=[1, 0, 0])
        
        # Create a rectangle that will move along the width axis
        # Fit rectangle to hexahedron dimensions (height x depth)
        rectangle = Cube(side_length=1, fill_opacity=0.6, fill_color=RED, stroke_width=2, stroke_color=YELLOW)
        rectangle.scale([0.001, height, depth])  # Scale to match hexahedron's depth and height
        
        # Rotate rectangle same as hexahedron
        rectangle.rotate_about_origin(1 * DEGREES, axis=[0, 0, 1])
        rectangle.rotate_about_origin(75 * DEGREES, axis=[0, 1, 0])
        rectangle.rotate_about_origin(10 * DEGREES, axis=[1, 0, 0])
        
        # Define rotation angles for position calculation
        roll_angle = 1 * DEGREES
        yaw_angle = 75 * DEGREES
        pitch_angle = 10 * DEGREES

        # Calculate initial position at front face (timestep 0)
        # Front face is at LEFT * width/2 in local coordinates
        initial_local_pos = np.array([-width/2, -0.85, 0.15])  # LEFT direction
            
        # Apply rotations to get world position
        # Rotation matrices (applied in reverse order: pitch, roll, yaw)
        pitch_rad = np.radians(10)
        roll_rad = np.radians(1)
        yaw_rad = np.radians(75)
        
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(pitch_rad), -np.sin(pitch_rad)],
            [0, np.sin(pitch_rad), np.cos(pitch_rad)]
        ])
        
        Rz = np.array([
            [np.cos(roll_rad), -np.sin(roll_rad), 0],
            [np.sin(roll_rad), np.cos(roll_rad), 0],
            [0, 0, 1]
        ])
        
        Ry = np.array([
            [np.cos(yaw_rad), 0, np.sin(yaw_rad)],
            [0, 1, 0],
            [-np.sin(yaw_rad), 0, np.cos(yaw_rad)]
        ])
            
        # Apply rotations: Ry @ Rz @ Rx
        initial_rotated_pos = Ry @ Rz @ Rx @ initial_local_pos
        # Hexahedron is centered at origin (before rotation), so use ORIGIN as reference
        initial_position = ORIGIN + initial_rotated_pos
        rectangle.move_to(initial_position)

        # Group hexahedron and rectangle together
        hexahedron_group = VGroup(hexahedron, rectangle)
        
        # Move the entire group up
        group_up_offset = 1.0  # Adjust this value to move up more/less
        hexahedron_group.shift(UP * group_up_offset)
        
        # Create timestep text that will update (range 0 to 100)
        timestep_tracker = ValueTracker(0.0)
        timestep_text = Text(f"timestep = {int(timestep_tracker.get_value())}", font_size=18, color=YELLOW)
        # Position text next to hexahedron_group (to the right)
        timestep_text.move_to(hexahedron_group.get_center() + RIGHT * 3)
        
        self.add(hexahedron_group)
        self.add_fixed_in_frame_mobjects(timestep_text)
        self.wait(1)
        
        # Update text content based on timestep_tracker (0 to 100)
        def update_text(mob):
            t = timestep_tracker.get_value()
            # Update text content, keep position fixed
            new_text = Text(f"timestep = {int(t)}", font_size=18, color=YELLOW)
            new_text.move_to(hexahedron_group.get_center() + RIGHT * 3)
            mob.become(new_text)
        
        def update_rectangle(mob):
            t = timestep_tracker.get_value()
            # Calculate position along width axis in local coordinates
            # t=0 -> front face at -width/2, t=100 -> end face at +width/2
            # Normalize t from 0-100 to 0-1 for position calculation
            t_normalized = t / 100.0
            x_local = -width/2 + t_normalized * width
            local_pos = np.array([x_local, -0.85, 0.15])
        
            # Apply same rotations as hexahedron (pitch, roll, yaw in reverse order)
            rotated_pos = Ry @ Rz @ Rx @ local_pos
            # Add upward movement as rectangle travels
            vertical_movement = t_normalized * 1.7
            vertical_offset = np.array([0, vertical_movement, 0])
            # Use hexahedron's shifted center (after group shift)
            hexahedron_center = np.array(hexahedron.get_center())
            new_position = hexahedron_center + rotated_pos + vertical_offset
            mob.move_to(new_position)
         
        rectangle.add_updater(update_rectangle)
        timestep_text.add_updater(update_text)
        
        # Animate from front (0) to end (100)
        self.play(
            timestep_tracker.animate.set_value(100.0),
            run_time=5
        )
        
        rectangle.remove_updater(update_rectangle)
        timestep_text.remove_updater(update_text)
        self.wait(2)

        # Scale down and move hexahedron_group and timestep_text to the left
        scale_factor = 0.6  # Adjust this value: smaller = more scaled down
        left_offset = LEFT * 3.5  # Adjust this value: larger = move more to the left
        
        # Animate scaling down and moving left
        self.play(
            hexahedron_group.animate.scale(scale_factor).shift(left_offset), 
            timestep_text.animate.scale(scale_factor).shift(left_offset),
            FadeOut(timestep_text),
            run_time=1.5
        )
        self.wait(1)

        # 4.1 Write text beta_t = beta_start + (beta_end - beta_start) * (t / num_train_timesteps)
        beta_formula = MathTex(r"\beta_t = \beta_{\text{start}} + (\beta_{\text{end}} - \beta_{\text{start}}) \cdot \frac{t}{\text{num\_train\_timesteps}}", font_size=30)
        beta_formula.move_to(UP * 2.5 + RIGHT * 3)
        self.play(Write(beta_formula))
        self.wait(1)
        
        # 4.2.1 Write text with example values (with yellow numbers)
        example_text = VGroup(
            Text("num_train_timesteps = ", font_size=16, color=WHITE),
            Text("100", font_size=16, color=YELLOW),
            Text(", beta_start = ", font_size=16, color=WHITE),
            Text("0.0001", font_size=16, color=YELLOW),
            Text(", beta_end = ", font_size=16, color=WHITE),
            Text("0.02", font_size=16, color=YELLOW)
        )
        example_text.arrange(RIGHT, buff=0.1)
        example_text.move_to(beta_formula.get_center() + DOWN * 0.6)
        self.play(Write(example_text))
        self.wait(1)
        
        # 4.2.2 Replace with beta_t = 0.0001 + (0.02 - 0.0001) * (t / 100)
        beta_formula_substituted = MathTex(r"\beta_t = 0.0001 + (0.02 - 0.0001) \cdot \frac{t}{100}", font_size=30)
        beta_formula_substituted.move_to(beta_formula.get_center())
        self.play(
            ReplacementTransform(VGroup(beta_formula, example_text), beta_formula_substituted),
            run_time=1.5
        )
        self.wait(1)
        
        # 4.2.3 Write examples step by step, moving rectangle to each timestep first
        # Create update function for rectangle that accounts for scale and shift
        def update_rectangle_scaled(mob):
            t = timestep_tracker.get_value()
            # Normalize t from 0-100 to 0-1 for position calculation
            t_normalized = t / 100.0
            # Account for scale_factor applied to hexahedron_group
            scaled_width = width * scale_factor
            x_local = -scaled_width/2 + t_normalized * scaled_width
            local_pos = np.array([x_local, -0.85 * scale_factor, 0.15 * scale_factor])
            
            # Apply same rotations as hexahedron
            rotated_pos = Ry @ Rz @ Rx @ local_pos
            # Scale the vertical movement
            vertical_movement = t_normalized * 1.7 * scale_factor
            vertical_offset = np.array([0, vertical_movement, 0])
            # Use hexahedron's shifted center (after group shift and scale)
            hexahedron_center = np.array(hexahedron.get_center())
            new_position = hexahedron_center + rotated_pos + vertical_offset
            mob.move_to(new_position)
        
        # Add updater to rectangle
        rectangle.add_updater(update_rectangle_scaled)
        
        # Define timestep values and their corresponding example texts
        timestep_data = [
            (0, "Timestep 0:  beta_0 = 0.0001 + 0.0199 * (0/100) = ", " 0.0001"),
            (23, "Timestep 23: beta_23 = 0.0001 + 0.0199 * (23/100) = ", " 0.004677"),
            (45, "Timestep 45: beta_45 = 0.0001 + 0.0199 * (45/100) = ", " 0.009055"),
            (87, "Timestep 87: beta_87 = 0.0001 + 0.0199 * (87/100) = ", " 0.017413"),
            (12, "Timestep 12: beta_12 = 0.0001 + 0.0199 * (12/100) = ", " 0.002488")
        ]
        
        # Create container for all examples
        examples_beta = VGroup()
        example_y_position = beta_formula_substituted.get_center() + DOWN * 1.8
        
        # Iterate through each timestep: move rectangle, then write example
        for idx, (timestep_val, text_part, result_part) in enumerate(timestep_data):
            # 1. Move rectangle to the timestep
            self.play(
                timestep_tracker.animate.set_value(float(timestep_val)),
                run_time=0.8
            )
            self.wait(0.3)  # Hold at the position
            
            # 2. Create and write the example for this timestep
            example_text = VGroup(
                Text(text_part, font_size=16, color=WHITE),
                Text(result_part, font_size=16, color=YELLOW)
            )
            example_text.arrange(RIGHT, buff=0.1)
            # Position this example in the list (calculate y position based on index)
            example_text.move_to(example_y_position + DOWN * (idx * 0.4))
            examples_beta.add(example_text)
            
            # 3. Write the example
            self.play(Write(example_text), run_time=0.8)
            self.wait(0.3)
        
        # Remove updater
        rectangle.remove_updater(update_rectangle_scaled)
        self.wait(2)
        
        # 4.2.4 Fade out examples and beta_formula_substituted
        self.play(
            FadeOut(examples_beta),
        )
        self.wait(1)
        
        # 4.3.1 Write text "alpha_t = 1 - beta_t"
        alpha_formula = MathTex(r"\alpha_t = 1 - \beta_t", font_size=30)
        alpha_formula.move_to(beta_formula.get_center() + DOWN * 0.8)
        self.play(Write(alpha_formula))
        self.wait(1)
        
        # 4.3.2 Write examples (with yellow final results)
        examples_alpha = VGroup(
            VGroup(
                Text("Timestep 0:  alpha_0 = 1 - 0.0001 = ", font_size=16, color=WHITE),
                Text(" 0.9999", font_size=16, color=YELLOW)
            ).arrange(RIGHT, buff=0.1),
            VGroup( 
                Text("Timestep 23: alpha_23 = 1 - 0.004677 = ", font_size=16, color=WHITE),
                Text(" 0.995323", font_size=16, color=YELLOW)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("Timestep 45: alpha_45 = 1 - 0.009055 = ", font_size=16, color=WHITE),
                Text(" 0.990945", font_size=16, color=YELLOW)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("Timestep 87: alpha_87 = 1 - 0.017413 = ", font_size=16, color=WHITE),
                Text(" 0.982587", font_size=16, color=YELLOW)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("Timestep 12: alpha_12 = 1 - 0.002488 = ", font_size=16, color=WHITE),
                Text(" 0.997512", font_size=16, color=YELLOW)
            ).arrange(RIGHT, buff=0)
        )
        examples_alpha.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        examples_alpha.move_to(alpha_formula.get_center() + DOWN * 1.8)
        self.play(Write(examples_alpha))
        self.wait(2)
        
        # 4.3.3 Fade out only the examples
        self.play(FadeOut(examples_alpha))
        self.wait(1)
        
        # 4.4.1 Write text alpha_bar_t = alpha_0 * alpha_1 * alpha_2 * ... * alpha_t
        alpha_bar_formula = MathTex(r"\bar{\alpha}_t = \alpha_0 \cdot \alpha_1 \cdot \alpha_2 \cdot \ldots \cdot \alpha_t", font_size=30)
        alpha_bar_formula.move_to(alpha_formula.get_center() + DOWN * 0.8)
        self.play(Write(alpha_bar_formula))
        self.wait(1)
        
        # 4.4.2 Write examples (with yellow final results)
        examples_alpha_bar = VGroup(
            Text("Timestep 23:", font_size=16, color=WHITE),
            VGroup(
                Text("alpha_bar_23 = alpha_0 * alpha_1 * ... * alpha_23 ≈ ", font_size=16, color=WHITE),
                Text(" 0.895", font_size=16, color=YELLOW)
            ).arrange(RIGHT, buff=0.1),
            Text("Timestep 87:", font_size=16, color=WHITE),
            VGroup(
                Text("alpha_bar_87 = alpha_0 * alpha_1 * ... * alpha_87 ≈ ", font_size=16, color=WHITE),
                Text(" 0.260", font_size=16, color=YELLOW)
            ).arrange(RIGHT, buff=0.1),
            Text("Timestep 12:", font_size=16, color=WHITE),
            VGroup(
                Text("alpha_bar_12 = alpha_0 * alpha_1 * ... * alpha_12 ≈ ", font_size=16, color=WHITE),
                Text(" 0.970", font_size=16, color=YELLOW)
            ).arrange(RIGHT, buff=0.1),
            Text("Timestep 45:", font_size=16, color=WHITE),
            VGroup(
                Text("alpha_bar_45 = alpha_0 * alpha_1 * ... * alpha_45 ≈ ", font_size=16, color=WHITE),
                Text(" 0.640", font_size=16, color=YELLOW)
            ).arrange(RIGHT, buff=0.1)
        )
        examples_alpha_bar.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        examples_alpha_bar.move_to(alpha_bar_formula.get_center() + DOWN * 1.8)
        self.play(Write(examples_alpha_bar))
        self.wait(2)
        
        # 4.4.3 Fade out the examples
        self.play(FadeOut(examples_alpha_bar))
        self.wait(1)
        
        # 4.4.1 (second one) Write text "x_t = sqrt(alpha_bar_t) * data + sqrt(1-alpha_bar_t) * noise"
        x_t_formula = MathTex(r"x_t = \sqrt{\bar{\alpha}_t} \cdot \text{data} + \sqrt{1-\bar{\alpha}_t} \cdot \text{noise}", font_size=30)
        x_t_formula.move_to(alpha_bar_formula.get_center() + DOWN * 0.8)
        self.play(Write(x_t_formula))
        self.wait(1)
        
        # 4.4.2 Write examples (with yellow floating numbers)
        examples_x_t = VGroup(
            VGroup(
                Text("x_23 = ", font_size=16, color=WHITE),
                Text("0.946", font_size=16, color=YELLOW),
                Text(" * action + ", font_size=16, color=WHITE),
                Text("0.324", font_size=16, color=YELLOW),
                Text(" * noise", font_size=16, color=WHITE)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("x_87 = ", font_size=16, color=WHITE),
                Text("0.510", font_size=16, color=YELLOW),
                Text(" * action + ", font_size=16, color=WHITE),
                Text("0.860", font_size=16, color=YELLOW),
                Text(" * noise", font_size=16, color=WHITE)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("x_12 = ", font_size=16, color=WHITE),
                Text("0.985", font_size=16, color=YELLOW),
                Text(" * action + ", font_size=16, color=WHITE),
                Text("0.173", font_size=16, color=YELLOW),
                Text(" * noise", font_size=16, color=WHITE)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("x_45 = ", font_size=16, color=WHITE),
                Text("0.800", font_size=16, color=YELLOW),
                Text(" * action + ", font_size=16, color=WHITE),
                Text("0.600", font_size=16, color=YELLOW),
                Text(" * noise", font_size=16, color=WHITE)
            ).arrange(RIGHT, buff=0.1)
        )
        examples_x_t.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        examples_x_t.move_to(x_t_formula.get_center() + DOWN * 1.3)
        self.play(Write(examples_x_t))
        self.wait(2)
        
