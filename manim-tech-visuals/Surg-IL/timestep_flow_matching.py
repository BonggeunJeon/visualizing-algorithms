from manim import *
import numpy as np
from PIL import Image


class TimestepFlowMatching(ThreeDScene):
    """
    Visualization showing a hexahedron with width representing timestep (0-1),
    and a rectangle moving along the width axis to show the changing timestep value.
    """
    
    def construct(self):
        # Define dimensions
        width = 10  # Represents timestep range 0 to 1
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

        # Calculate initial position at front face (timestep 0.0)
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
        
        # Create timestep text that will update
        timestep_tracker = ValueTracker(0.0)
        timestep_text = Text(f"timestep = {timestep_tracker.get_value():.3f}", font_size=18, color=YELLOW)
        # Position text next to hexahedron_group (to the right)
        timestep_text.move_to(hexahedron_group.get_center() + RIGHT * 3)
        
        self.add(hexahedron_group)
        self.add_fixed_in_frame_mobjects(timestep_text)
        self.wait(1)
        
        # Update text content based on timestep_tracker
        def update_text(mob):
            t = timestep_tracker.get_value()
            # Update text content, keep position fixed
            new_text = Text(f"timestep = {t:.3f}", font_size=18, color=YELLOW)
            new_text.move_to(hexahedron_group.get_center() + RIGHT * 3)
            mob.become(new_text)
        
        def update_rectangle(mob):
            t = timestep_tracker.get_value()
            # Calculate position along width axis in local coordinates
            # t=0.0 -> front face at -width/2, t=1.0 -> end face at +width/2
            # The Y and Z offsets (-0.85, 0.15) will be rotated along with the X position
            # Use linear interpolation from left face to right face
            x_local = -width/2 + t * width  # When t=0: -width/2 (left), when t=1: +width/2 (right)
            local_pos = np.array([x_local, -0.85, 0.15])
        
            # Apply same rotations as hexahedron (pitch, roll, yaw in reverse order)
            # This rotates the entire local_pos vector including the offsets
            rotated_pos = Ry @ Rz @ Rx @ local_pos
            # Add upward movement as rectangle travels (adjust this value to move up more/less)
            vertical_movement = t * 1.7  # Moves up 1.7 units as it goes from start to end
            vertical_offset = np.array([0, vertical_movement, 0])  # Move up in world Y-axis
            # Use hexahedron's shifted center (after group shift)
            hexahedron_center = np.array(hexahedron.get_center())
            new_position = hexahedron_center + rotated_pos + vertical_offset
            mob.move_to(new_position)
         
        rectangle.add_updater(update_rectangle)
        timestep_text.add_updater(update_text)
        
        # Animate from front (0.0) to end (1.0)
        self.play(
            timestep_tracker.animate.set_value(1.0),
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
            run_time=1.5
        )
        self.wait(1)

        # Write formula 
        # x_t = timestep_text X original + (1-timestep_text) X noise (Latex)
        formula = MathTex(r"x_t = t \cdot x_1 + (1-t) \cdot x_0")
        # Position formula above the objects using screen coordinates
        formula.move_to(UP * 2.5 + RIGHT * 3)
        # Add formula as fixed-in-frame so it stays in 2D and isn't affected by 3D orientation
        #self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(1)
        
        # Replace timestep_text and formula with new formula that includes actual timestep value
        current_timestep = timestep_tracker.get_value()
        timestep_str = f"{current_timestep:.3f}"
        
        # Create formula with separate parts so we can update only the timestep values
        # Build formula: x_t = [t_str] \cdot x_1 + (1-[t_str]) \cdot x_0
        formula_left = MathTex(r"x_t = ")
        formula_t1 = MathTex(timestep_str, color=YELLOW)  # First timestep value
        formula_mid = MathTex(r" \cdot x_1 + (1-")
        formula_t2 = MathTex(timestep_str, color=YELLOW)  # Second timestep value (same value)
        formula_right = MathTex(r") \cdot x_0")
        
        # Arrange formula parts horizontally
        new_formula = VGroup(formula_left, formula_t1, formula_mid, formula_t2, formula_right)
        new_formula.arrange(RIGHT, buff=0.05)
        # Position new formula at the same location as old formula
        new_formula.move_to(UP * 2.5 + RIGHT * 3)
        
        # Group timestep_text and formula, then transform into new formula
        old_elements = VGroup(timestep_text, formula)
        #self.add_fixed_in_frame_mobjects(new_formula)
        self.play(
            ReplacementTransform(old_elements, new_formula),
            run_time=1.5
        )
        self.wait(1)

        # Add image of timestep flow matching - show process of adding noise synchronized with timestep
        # Load original image once
        image_path = "media/images/timestep_flow_matching/dog.jpg"
        original_image = Image.open(image_path)
        original_img_array = np.array(original_image)
        
        # Set random seed for consistent noise generation (optional)
        np.random.seed(42)
        
        # Generate noise pattern with much higher intensity
        # Use a multiplier to make noise much stronger
        noise_multiplier = 10.0  # Multiply noise intensity (higher = more noise)
        max_noise_intensity = 255 * noise_multiplier  # Maximum noise intensity at t=1.0
        noise_pattern = np.random.randint(-255, 255, size=original_img_array.shape, dtype=np.int16)
        
        # Create initial image (no noise at t=0.0) - but since timestep_tracker is at 1.0, show full noise initially
        initial_t = timestep_tracker.get_value()  # Should be 1.0 at this point
        scaled_noise_initial = (noise_pattern * initial_t * noise_multiplier).astype(np.int16)
        initial_img_array = np.clip(original_img_array.astype(np.int16) + scaled_noise_initial, 0, 255).astype(np.uint8)
        initial_image = Image.fromarray(initial_img_array)
        temp_initial_path = "media/images/timestep_flow_matching/dog_initial.jpg"
        initial_image.save(temp_initial_path)
        
        # Create ImageMobject with initial image (noisy since t=1.0)
        timestep_flow_matching_image = ImageMobject(temp_initial_path)
        timestep_flow_matching_image.scale(0.5)
        # Position image below new_formula
        timestep_flow_matching_image.move_to(new_formula.get_center() + DOWN * 1.5)
        
        # Create text showing Data/Noise percentage that will update
        initial_t = timestep_tracker.get_value()  # Should be 1.0
        n_percent = int((1.0 - initial_t) * 100)  # n = (1-t)*100, so t=1.0 -> n=0%, t=0.0 -> n=100%
        noise_percent = 100 - n_percent
        # Create text with n_percent and noise_percent in yellow color
        text_part1 = Text(f"{n_percent}%", font_size=20, color=YELLOW)
        text_part2 = Text(f" Data + ", font_size=20, color=WHITE)
        text_part3 = Text(f"{noise_percent}%", font_size=20, color=YELLOW)
        text_part4 = Text(f" Noise", font_size=20, color=WHITE)
        data_noise_text = VGroup(text_part1, text_part2, text_part3, text_part4)
        data_noise_text.arrange(RIGHT, buff=0)
        # Position text below the image
        data_noise_text.move_to(timestep_flow_matching_image.get_center() + DOWN * 0.8)
        
        self.add_fixed_in_frame_mobjects(timestep_flow_matching_image, data_noise_text)
        self.wait(0.5)
        
        # Function to update image with noise based on timestep
        # As timestep goes from 1.0 to 0.0, noise decreases (image becomes cleaner)
        def update_image_with_noise(mob):
            t = timestep_tracker.get_value()
            # Calculate noise intensity based on timestep (0.0 = no noise, 1.0 = full noise)
            # Use noise_multiplier to make noise much stronger
            scaled_noise = (noise_pattern * t * noise_multiplier).astype(np.int16)
            noisy_img_array = np.clip(original_img_array.astype(np.int16) + scaled_noise, 0, 255).astype(np.uint8)
            
            # Convert to PIL Image and save temporarily
            noisy_image = Image.fromarray(noisy_img_array)
            temp_path = "media/images/timestep_flow_matching/dog_temp.jpg"
            noisy_image.save(temp_path)
            
            # Update the ImageMobject
            new_image = ImageMobject(temp_path)
            new_image.scale(0.5)
            new_image.move_to(new_formula.get_center() + DOWN * 1.5)
            mob.become(new_image)
        
        # Function to update text showing Data/Noise percentage
        def update_data_noise_text(mob):
            t = timestep_tracker.get_value()
            # n = (1-t)*100, so when t=1.0 -> n=0%, when t=0.0 -> n=100%
            n_percent = int((1.0 - t) * 100)
            noise_percent = 100 - n_percent
            # Create text with n_percent and noise_percent in yellow color
            text_part1 = Text(f"{n_percent}%", font_size=20, color=YELLOW)
            text_part2 = Text(f" Data + ", font_size=20, color=WHITE)
            text_part3 = Text(f"{noise_percent}%", font_size=20, color=YELLOW)
            text_part4 = Text(f" Noise", font_size=20, color=WHITE)
            # Combine the text parts
            new_text = VGroup(text_part1, text_part2, text_part3, text_part4)
            new_text.arrange(RIGHT, buff=0)
            # Keep same position (below image)
            new_text.move_to(timestep_flow_matching_image.get_center() + DOWN * 0.8)
            mob.become(new_text)
        
        # Add updaters so they update during reverse animation
        timestep_flow_matching_image.add_updater(update_image_with_noise)
        data_noise_text.add_updater(update_data_noise_text)
        
        # Animate rectangle moving back from end to front with formula update
        def update_formula(mob):
            t = timestep_tracker.get_value()
            t_str = f"{t:.3f}"
            # Update only the timestep value parts (mob[1] and mob[3])
            # Create new timestep parts with updated value
            new_t1 = MathTex(t_str, color=YELLOW)
            new_t2 = MathTex(t_str, color=YELLOW)
            # Match font size and preserve positions
            new_t1.scale(mob[1].get_height() / new_t1.get_height())
            new_t2.scale(mob[3].get_height() / new_t2.get_height())
            new_t1.move_to(mob[1].get_center())
            new_t2.move_to(mob[3].get_center())
            # Replace only the timestep parts using become()
            mob[1].become(new_t1)
            mob[3].become(new_t2)
        
        # Add updater to new_formula
        new_formula.add_updater(update_formula)
        
        # Create separate update function for reverse rectangle movement (end to front)
        def update_rectangle_reverse(mob):
            t = timestep_tracker.get_value()
            # Calculate position along width axis in local coordinates
            # Account for scale_factor applied to hexahedron_group
            # The effective width is now width * scale_factor
            scaled_width = width * scale_factor
            # t=0.0 -> front face at -scaled_width/2, t=1.0 -> end face at +scaled_width/2
            # The Y and Z offsets also need to be scaled
            x_local = -scaled_width/2 + t * scaled_width  # When t=0: -scaled_width/2 (left), when t=1: +scaled_width/2 (right)
            local_pos = np.array([x_local, -0.85 * scale_factor, 0.15 * scale_factor])
            
            # Apply same rotations as hexahedron (pitch, roll, yaw in reverse order)
            # This rotates the entire local_pos vector including the offsets
            rotated_pos = Ry @ Rz @ Rx @ local_pos
            # Add upward movement as rectangle travels (adjust this value to move up more/less)
            # Scale the vertical movement as well
            vertical_movement = t * 1.7 * scale_factor  # Adjust if needed for reverse movement
            vertical_offset = np.array([0, vertical_movement, 0])  # Move up in world Y-axis
            # Use hexahedron's shifted center (after group shift and scale)
            # The center already accounts for the left_offset shift
            hexahedron_center = np.array(hexahedron.get_center())
            new_position = hexahedron_center + rotated_pos + vertical_offset
            mob.move_to(new_position)
        
        # Re-add rectangle updater with reverse function
        rectangle.add_updater(update_rectangle_reverse)
        
        # Animate timestep from 1.0 back to 0.0 (moving rectangle from end to front)
        self.play(
            timestep_tracker.animate.set_value(0.0),
            run_time=5
        )
        
        # Remove updaters
        rectangle.remove_updater(update_rectangle_reverse)
        new_formula.remove_updater(update_formula)
        timestep_flow_matching_image.remove_updater(update_image_with_noise)
        data_noise_text.remove_updater(update_data_noise_text)
        self.wait(1)
        
        # Add LaTeX formula below data_noise_text
        u_formula = MathTex(r"u_t = x_1 - x_0")
        # Position formula below data_noise_text
        u_formula.move_to(data_noise_text.get_center() + DOWN * 0.6)
        self.add_fixed_in_frame_mobjects(u_formula)
        self.play(Write(u_formula))
        self.wait(1)
        
        # Add LaTeX text below u_formula, separated to add yellow color to 0.0000001
        # First line: x_t + 0.0000001
        line1_part1 = MathTex(r"x_t + ")
        line1_value = MathTex(r"0.0000001", color=YELLOW)  # First value in yellow
        line1 = VGroup(line1_part1, line1_value)
        line1.arrange(RIGHT, buff=0)
        
        # Second line: t + 0.0000001
        line2_part1 = MathTex(r"t + ")
        line2_value = MathTex(r"0.0000001", color=YELLOW)  # Second value in yellow
        line2 = VGroup(line2_part1, line2_value)
        line2.arrange(RIGHT, buff=0)
        
        # Combine both lines vertically
        additional_text = VGroup(line1, line2)
        additional_text.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        # Position text below u_formula
        additional_text.move_to(u_formula.get_center() + DOWN * 1.2 + LEFT * 0.5)
        self.play(Write(additional_text))
        self.wait(1)
        
        # Replace additional_text with fraction formula using ReplacementTransform
        fraction_formula = MathTex(r"\frac{\Delta x_t}{\Delta t}")
        # Position at the same location as additional_text
        fraction_formula.move_to(additional_text.get_center())
        self.play(ReplacementTransform(additional_text, fraction_formula))
        self.wait(1)
        
        # Add LaTeX text to the right of fraction_formula
        approx_text = MathTex(r"\approx u_{t}")
        # Position to the right of fraction_formula
        approx_text.next_to(fraction_formula, RIGHT, buff=0.3)
        self.play(Write(approx_text))
        self.wait(1)