from manim import *
import numpy as np


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
        
        # Re-add rectangle and text updaters (using same update functions)
        rectangle.add_updater(update_rectangle)
        timestep_text.add_updater(update_text)
        
        # Animate timestep from 1.0 back to 0.0 (moving rectangle from end to front)
        self.play(
            timestep_tracker.animate.set_value(0.0),
            run_time=5
        )
        
        # Remove updaters
        rectangle.remove_updater(update_rectangle)
        timestep_text.remove_updater(update_text)
        self.wait(1)
        
        # Re-add updaters for random sampling animation
        rectangle.add_updater(update_rectangle)
        timestep_text.add_updater(update_text)
        
        # Create noise level text (will be updated for each interval)
        noise_text = None
        # Store base position for noise text (relative to hexahedron_group)
        noise_text_base_position = hexahedron_group.get_center() + RIGHT * 3 + DOWN * 0.8
        
        # Random sampling in three intervals
        # Interval 1: 0.001 to 0.399 for 4 seconds (white color)
        num_samples_1 = 8  # Number of random samples in first interval
        # Change rectangle color to white for first interval
        self.play(rectangle.animate.set_fill(WHITE), run_time=0.3)
        # Create and show "High Noise" text
        if noise_text is not None:
            self.play(FadeOut(noise_text), run_time=0.2)
        noise_text = Tex("High Noise", font_size=36, color=WHITE)
        noise_text.move_to(noise_text_base_position)
        self.add_fixed_in_frame_mobjects(noise_text)
        self.play(FadeIn(noise_text), run_time=0.3)
        for _ in range(num_samples_1):
            random_value = np.random.uniform(0.001, 0.399)
            self.play(
                timestep_tracker.animate.set_value(random_value),
                run_time=8.0 / num_samples_1
            )
        
        # Interval 2: 0.401 to 0.599 for 2.5 seconds (green color)
        num_samples_2 = 5  # Number of random samples in second interval
        # Change rectangle color to green for second interval
        self.play(rectangle.animate.set_fill(GREEN), run_time=0.3)
        # Replace with "Middle Noise" text
        self.play(FadeOut(noise_text), run_time=0.2)
        noise_text = Tex("Middle Noise", font_size=36, color=WHITE)
        noise_text.move_to(noise_text_base_position)
        self.add_fixed_in_frame_mobjects(noise_text)
        self.play(FadeIn(noise_text), run_time=0.3)
        for _ in range(num_samples_2):
            random_value = np.random.uniform(0.401, 0.599)
            self.play(
                timestep_tracker.animate.set_value(random_value),
                run_time=5.0 / num_samples_2
            )
        
        # Interval 3: 0.601 to 0.999 for 1.5 seconds (yellow color)
        num_samples_3 = 3  # Number of random samples in third interval
        # Change rectangle color to yellow for third interval
        self.play(rectangle.animate.set_fill(YELLOW), run_time=0.3)
        # Replace with "Low Noise" text
        self.play(FadeOut(noise_text), run_time=0.2)
        noise_text = Tex("Low Noise", font_size=36, color=WHITE)
        noise_text.move_to(noise_text_base_position)
        self.add_fixed_in_frame_mobjects(noise_text)
        self.play(FadeIn(noise_text), run_time=0.3)
        for _ in range(num_samples_3):
            random_value = np.random.uniform(0.601, 0.999)
            self.play(
                timestep_tracker.animate.set_value(random_value),
                run_time=3.0 / num_samples_3
            )
        
        # Remove updaters
        rectangle.remove_updater(update_rectangle)
        timestep_text.remove_updater(update_text)
        self.wait(1)