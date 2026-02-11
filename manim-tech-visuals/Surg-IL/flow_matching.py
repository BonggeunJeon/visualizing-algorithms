from manim import *
import numpy as np


class FlowMatching(ThreeDScene):
    """
    Flow Matching visualization with a semi-transparent 3D cube
    containing random points inside.
    """
    
    def construct(self):
        # Set up 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Create a semi-transparent 3D cube in the center
        cube_size = 3.0  # Size of the cube
        cube = Cube(
            side_length=cube_size,
            fill_opacity=0.2,  # Semi-transparent
            fill_color=BLUE,
            stroke_width=2,
            stroke_color=WHITE
        )
        cube.move_to(ORIGIN)
        
        # Create 20 random points inside the cube
        num_points = 20
        points = VGroup()
        initial_positions = []  # Store initial positions
        
        # Generate random points within the cube bounds
        # Cube is centered at origin, so points should be in range [-cube_size/2, cube_size/2]
        half_size = cube_size / 2
        
        for _ in range(num_points):
            # Generate random coordinates within the cube
            x = np.random.uniform(-half_size, half_size)
            y = np.random.uniform(-half_size, half_size)
            z = np.random.uniform(-half_size, half_size)
            
            initial_pos = np.array([x, y, z])
            initial_positions.append(initial_pos)
            
            # Create a small sphere to represent the point
            point = Sphere(
                radius=0.08,
                fill_opacity=1.0,
                fill_color=RED,
                stroke_width=0
            )
            point.move_to(initial_pos)
            points.add(point)
        
        # Animate: First show the cube
        self.play(Create(cube), run_time=1.5)
        self.wait(0.5)
        
        # Then show the points appearing one by one
        self.play(
            *[FadeIn(point) for point in points],
            run_time=2.0
        )
        self.wait(1.0)
        
        # Define a curve that goes through the cube
        # Using a parametric 3D curve (e.g., a smooth curve from one side to another)
        half_size = cube_size / 2
        
        def curve_function(t):
            """
            Parametric function for a 3D curve inside the cube.
            t ranges from 0 to 1
            """
            # Create a smooth curve that goes through the cube
            # Using a combination of sine and cosine for a smooth curved path
            x = -half_size * 0.8 + (half_size * 1.6) * t
            y = half_size * 0.6 * np.sin(np.pi * t) - half_size * 0.3
            z = half_size * 0.6 * np.cos(np.pi * t)
            return np.array([x, y, z])
        
        # Create the curve visualization (white line to show the target path)
        curve_points = np.array([curve_function(t) for t in np.linspace(0, 1, 100)])
        # Ensure points are 3D (N x 3 array)
        if curve_points.shape[1] != 3:
            curve_points = np.column_stack([curve_points, np.zeros(len(curve_points))])
        curve_path = VMobject()
        curve_path.set_points_as_corners(curve_points)
        curve_path.set_stroke(color=WHITE, width=2, opacity=0.7)
        
        # Calculate target positions for each point along the curve
        # Distribute points evenly along the curve
        target_positions = []
        for i in range(num_points):
            t = i / (num_points - 1) if num_points > 1 else 0
            target_pos = curve_function(t)
            target_positions.append(target_pos)
        
        # Show the curve path (white line)
        self.play(Create(curve_path), run_time=1.0)
        self.wait(0.5)
        
        # Create Timestep text below the cube
        timestep_tracker = ValueTracker(0.0)
        
        # Create fixed "Timestep = " part
        timestep_label = MathTex(r"\text{Timestep} = ", font_size=24, color=WHITE)
        # Create dynamic value part
        timestep_value_text = MathTex("0.0", font_size=24, color=YELLOW)
        
        # Combine them
        timestep_display = VGroup(timestep_label, timestep_value_text)
        timestep_display.arrange(RIGHT, buff=0.1)
        # Position below the cube
        timestep_display.move_to(cube.get_center() + DOWN * (cube_size / 2 + 1.0))
        
        # Store the position for the value text
        timestep_value_position = timestep_value_text.get_center()
        
        # Add both parts as fixed in frame
        self.add_fixed_in_frame_mobjects(timestep_label, timestep_value_text)
        self.wait(0.5)
        
        # Create trajectory lines (yellow) for each point
        # These will be drawn as points move
        trajectory_lines = VGroup()
        for i, initial_pos in enumerate(initial_positions):
            # Ensure initial_pos is a 3D numpy array with shape (3,)
            if isinstance(initial_pos, np.ndarray):
                initial_pos_3d = initial_pos.copy().flatten()
                if len(initial_pos_3d) == 2:
                    initial_pos_3d = np.append(initial_pos_3d, 0.0)
                elif len(initial_pos_3d) != 3:
                    initial_pos_3d = np.array([float(initial_pos_3d[0]), float(initial_pos_3d[1]), 0.0])
            else:
                initial_pos_3d = np.array([float(initial_pos[0]), float(initial_pos[1]), 0.0])
            
            # Ensure it's exactly shape (3,)
            initial_pos_3d = np.array(initial_pos_3d).reshape(3)
            
            # Create a line from initial position to current position
            # Start with zero length (same start and end) - use set_points_as_corners for 3D
            trajectory_line = VMobject()
            line_points = np.array([initial_pos_3d, initial_pos_3d])
            trajectory_line.set_points_as_corners(line_points)
            trajectory_line.set_stroke(color=YELLOW, width=1.5, opacity=0.8)
            trajectory_lines.add(trajectory_line)
        
        self.add(trajectory_lines)
        
        # Animate points moving to their positions on the curve
        # and update trajectory lines as they move
        def create_trajectory_updater(initial_pos, point):
            """Create updater function for trajectory line"""
            def updater(mob):
                current_pos = point.get_center()
                # Ensure both positions are 3D numpy arrays with shape (3,)
                if isinstance(initial_pos, np.ndarray):
                    start_pos = initial_pos.copy()
                    if start_pos.shape == (2,):
                        start_pos = np.append(start_pos, 0)
                    elif start_pos.shape != (3,):
                        start_pos = np.array([start_pos[0], start_pos[1], 0])
                else:
                    start_pos = np.array([float(initial_pos[0]), float(initial_pos[1]), 0.0])
                
                if isinstance(current_pos, np.ndarray):
                    end_pos = current_pos.copy()
                    if end_pos.shape == (2,):
                        end_pos = np.append(end_pos, 0)
                    elif end_pos.shape != (3,):
                        end_pos = np.array([end_pos[0], end_pos[1], 0])
                else:
                    end_pos = np.array([float(current_pos[0]), float(current_pos[1]), 0.0])
                
                # Ensure both are 1D arrays of length 3
                start_pos = np.array(start_pos).flatten()[:3]
                end_pos = np.array(end_pos).flatten()[:3]
                if len(start_pos) < 3:
                    start_pos = np.append(start_pos, [0] * (3 - len(start_pos)))
                if len(end_pos) < 3:
                    end_pos = np.append(end_pos, [0] * (3 - len(end_pos)))
                
                # Update line using set_points_as_corners with proper 3D coordinates
                line_points = np.array([start_pos, end_pos])
                mob.set_points_as_corners(line_points)
            return updater
        
        # Add updaters to trajectory lines
        for i, (trajectory_line, point) in enumerate(zip(trajectory_lines, points)):
            updater_func = create_trajectory_updater(initial_positions[i], point)
            trajectory_line.add_updater(updater_func)
        
        # Create updater for timestep value text
        def update_timestep_value(mob):
            """Update timestep value text with current value"""
            timestep_value = timestep_tracker.get_value()
            new_value = MathTex(f"{timestep_value:.1f}", font_size=24, color=YELLOW)
            # Keep the same position
            new_value.move_to(timestep_value_position)
            mob.become(new_value)
        
        timestep_value_text.add_updater(update_timestep_value)
        
        animations = []
        for i, point in enumerate(points):
            animations.append(
                point.animate.move_to(target_positions[i])
            )
        
        # Animate timestep from 0.0 to 1.0 simultaneously with point movement
        animations.append(
            timestep_tracker.animate.set_value(1.0)
        )
        
        self.play(*animations, run_time=5.0)
        
        # Remove updater after animation
        timestep_value_text.remove_updater(update_timestep_value)
        
        # Remove updaters after animation
        for trajectory_line in trajectory_lines:
            trajectory_line.clear_updaters()
        
        self.wait(1.0)
        
        # Optional: Rotate the camera to show the 3D structure
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(4.0)
        self.stop_ambient_camera_rotation()
        self.wait(1.0)

