from manim import *
import numpy as np


class DiTVisualization(MovingCameraScene):
    """
    Visualization of DiT (Diffusion Transformer) structure:
    - Encoder Block and Decoder Block as 3D cubes
    - 5 layers inside each block as vertical rectangles (like books on a shelf)
    - Extract first Encoder layer and transform to horizontal rectangle
    - Zoom into the extracted layer
    """
    
    def construct(self):
                # Step 1: Create Encoder and Decoder Blocks as 3D cuboids (rectangular boxes)
        # Cuboid dimensions: width, height, depth
        cuboid_width = 3.0
        cuboid_height = 2.5
        cuboid_depth = 2.0
        
        # Encoder Block (left side) - cuboid with different dimensions
        encoder_block = Cube(
            side_length=1,
            fill_opacity=0.2,
            fill_color=TEAL,
            stroke_width=2,
            stroke_color=TEAL
        )
        # Scale to create a cuboid (rectangular box) instead of a cube
        encoder_block.scale([cuboid_width, cuboid_height, cuboid_depth])
        encoder_block.move_to(LEFT * 4)
        
        # Rotate to show from slightly top-right angle for 3D volumetric feel
        # Rotate around Y-axis (to show right side) and X-axis (to show top)
        encoder_block.rotate(20 * DEGREES, axis=UP)  # Rotate around Y-axis to show right side
        encoder_block.rotate(-10 * DEGREES, axis=RIGHT)  # Rotate around X-axis to show top
        
        # Decoder Block (right side) - cuboid with different dimensions
        decoder_block = Cube(
            side_length=1,
            fill_opacity=0.2,
            fill_color=BLUE,
            stroke_width=2,
            stroke_color=BLUE
        )
        # Scale to create a cuboid (rectangular box) instead of a cube
        decoder_block.scale([cuboid_width, cuboid_height, cuboid_depth])
        decoder_block.move_to(RIGHT * 4)
        
        # Rotate to show from slightly top-right angle for 3D volumetric feel
        # Rotate around Y-axis (to show right side) and X-axis (to show top)
        decoder_block.rotate(20 * DEGREES, axis=UP)  # Rotate around Y-axis to show right side
        decoder_block.rotate(-10 * DEGREES, axis=RIGHT)  # Rotate around X-axis to show top
        
        # Add labels for blocks
        encoder_label = Tex("Encoder Block", font_size=20, color=WHITE).scale(1.5)
        encoder_label.move_to(encoder_block.get_center() + DOWN * 2)
        
        decoder_label = Tex("Decoder Block", font_size=20, color=WHITE).scale(1.5)
        decoder_label.move_to(decoder_block.get_center() + DOWN * 2)
        
        # Show blocks
        self.play(
            Create(encoder_block),
            Create(decoder_block),
            Write(encoder_label),
            Write(decoder_label),
            run_time=1.5
        )
        self.wait(1)
        
        # Step 2: Create 5 layers inside each block as 3D cubes
        # Layer cube dimensions: width, height, depth
        layer_width = 0.2
        layer_height = 1.8
        layer_depth = 1.3
        layer_spacing = 0.4  # Space between layers
        
        # Encoder layers (3D cubes inside encoder block)
        encoder_layers = VGroup()
        encoder_layer_positions = []
        # Store encoder_layers as instance variable for later access
        self.encoder_layers_ref = encoder_layers
        
        # Calculate positions for 5 layers inside encoder block
        # Arrange them horizontally
        encoder_center = encoder_block.get_center()
        total_width = 4 * layer_spacing  # 5 layers with 4 gaps
        start_x = encoder_center[0] - total_width / 2
        
        for i in range(5):
            # Create 3D cube for layer
            layer = Cube(
                side_length=1,
                fill_opacity=0.6,
                fill_color=TEAL,
                stroke_width=1.5,
                stroke_color=WHITE
            )
            # Scale to create a cuboid with specified width, height, depth
            layer.scale([layer_width, layer_height, layer_depth])
            
            # Position horizontally inside the block
            x_pos = start_x + i * layer_spacing
            layer.move_to([x_pos, encoder_center[1], encoder_center[2]])
            
            # Apply same rotations as encoder_block for consistent 3D perspective
            layer.rotate(20 * DEGREES, axis=UP)
            layer.rotate(-8 * DEGREES, axis=RIGHT)
            
            encoder_layers.add(layer)
            encoder_layer_positions.append(layer.get_center())
        
        # Decoder layers (3D cubes inside decoder block)
        decoder_layers = VGroup()
        
        # Calculate positions for 5 layers inside decoder block
        decoder_center = decoder_block.get_center()
        start_x_decoder = decoder_center[0] - total_width / 2
        
        for i in range(5):
            # Create 3D cube for layer
            layer = Cube(
                side_length=1,
                fill_opacity=0.6,
                fill_color=BLUE,
                stroke_width=1.5,
                stroke_color=WHITE
            )
            # Scale to create a cuboid with specified width, height, depth
            layer.scale([layer_width, layer_height, layer_depth])
            
            # Position horizontally inside the block
            x_pos = start_x_decoder + i * layer_spacing
            layer.move_to([x_pos, decoder_center[1], decoder_center[2]])
            
            # Apply same rotations as decoder_block for consistent 3D perspective
            layer.rotate(20 * DEGREES, axis=UP)
            layer.rotate(-8 * DEGREES, axis=RIGHT)
            
            decoder_layers.add(layer)
        
        # Show layers appearing inside blocks
        self.play(
            Create(encoder_layers),
            Create(decoder_layers),
            run_time=2.0,
            lag_ratio=0.2
        )
        self.wait(1)
        
        # Step 3: Highlight the first Encoder Layer by changing its color to red
        first_encoder_layer = encoder_layers[0]

        # Store original position and references for later return
        # Calculate original position using the same formula as layer positioning (lines 101-103)
        # For first encoder layer (i=0): x_pos = start_x + 0 * layer_spacing = start_x
        encoder_center_pos = encoder_block.get_center()
        total_width = 4 * layer_spacing  # 5 layers with 4 gaps
        start_x = encoder_center_pos[0] - total_width / 2
        x_pos_first_layer = start_x + 0 * layer_spacing  # i=0 for first layer
        self.original_layer_position = np.array([x_pos_first_layer, encoder_center_pos[1], encoder_center_pos[2]])
        self.encoder_block_ref = encoder_block
        self.encoder_center_ref = np.array(encoder_center_pos)
        self.layer_width = layer_width
        self.layer_height = layer_height
        self.layer_depth = layer_depth
        
        # Change color to red to highlight it
        self.play(
            first_encoder_layer.animate.set_color(RED),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Step 4: Move the layer to center of screen and transform to flat 2D rectangle
        # Target dimensions for flat 2D rectangle
        rectangle_width = 4.0
        rectangle_height = 2.0
        
        # Create target 2D rectangle (flat, no 3D depth)
        flat_rectangle = Rectangle(
            width=rectangle_width,
            height=rectangle_height,
            fill_opacity=0.6,
            fill_color=RED,
            stroke_width=2,
            stroke_color=WHITE
        )
        flat_rectangle.move_to(ORIGIN)  # Center of screen
        
        # Move to center and transform to flat 2D rectangle simultaneously
        self.play(
            Create(flat_rectangle),
            run_time=1.0
        )
        self.wait(1)

        # Store flat_rectangle reference for later use
        self.flat_rectangle_ref = flat_rectangle
        
        # Step 5: Zoom in on the layer to fill the screen
        # Fade out other elements first
        other_elements = VGroup(
            encoder_block,
            decoder_block,
            encoder_label,
            decoder_label,
            encoder_layers[1:],  # All encoder layers except the first one
            decoder_layers
        )
        
        # Keep other elements visible (don't fade them out) 
        # Zoom in to fill the screen
        zoom_target = flat_rectangle.get_center()
        self.play(
            self.camera.frame.animate.move_to(zoom_target).set(width=rectangle_width * 1.2),
            run_time=1.5
        )
        self.wait(1)

        # Step 6: Visualize tensor transformation process
        self.visualize_tensor_transformation()

        self.play(
            FadeOut(flat_rectangle),
            run_time=0.5
        )
        self.wait(0.5)

        # Step 7: Sequentially change the color of remaining Encoder Layers to red
        # Sequentially change each remaining layer to red
        for i in range(1, 5):  # Indices 1, 2, 3, 4 (remaining 4 layers)
            self.play(
                encoder_layers[i].animate.set_color(RED),
                run_time=0.5
            )
            self.wait(0.3)
        
        self.wait(1)
    
    def create_tensor_3d_cubes(self, S: int, B: int, D: int, 
                               position: np.ndarray, cube_size: float = 0.08,
                               color: str = BLUE, opacity: float = 0.7):
        """
        Create 3D tensor visualization as a stack of small 3D cubes.
        
        Args:
            S: Sequence/Sample dimension
            B: Batch dimension
            D: Dimension/Feature dimension
            position: Center position for the tensor
            cube_size: Size of each cube
            color: Color of cubes
            opacity: Opacity of cubes
        """
        cubes = VGroup()
        spacing = cube_size * 1.0
        
        # Arrange cubes: S × B × D
        # Visualize as a compact stack: arrange S along X, D along Y, B along Z (depth)
        for s in range(S):
            for b in range(B):
                for d in range(D):
                    # Create small 3D cube
                    cube = Cube(
                        side_length=cube_size,
                        fill_opacity=opacity,
                        fill_color=color,
                        stroke_width=0.5,
                        stroke_color=WHITE
                    )
                    # Position: S along X, D along Y, B along Z (depth)
                    x_pos = (s - (S - 1) / 2) * spacing
                    y_pos = (d - (D - 1) / 2) * spacing
                    z_pos = (b - (B - 1) / 2) * spacing * 0.5  # Depth spacing
                    cube.move_to(position + np.array([x_pos, y_pos, z_pos]))
                    cubes.add(cube)
        
        return cubes
    
    def visualize_tensor_transformation(self):
        """Visualize the tensor transformation process through 7 stages inside the zoomed-in layer."""
        # Keep the flat rectangle visible (don't fade it out)
        # The camera is already zoomed in on the flat rectangle from Step 5
        
        # Tensor shape: (S, B, D)
        S, B, D = 1, 2, 6  # Example dimensions
        
        # Define stage labels
        stage_labels = [
            "Input",
            "Multi-head\nAttention",
            "Dropout",
            "Norm",
            "Feed\nForward",
            "Dropout",
            "Norm"
        ]
        
        # Calculate positions for 7 tensors (arranged horizontally)
        # Position relative to ORIGIN (center of zoomed view)
        # Use smaller spacing to fit within zoomed view, but larger cubes
        tensor_spacing = 0.6
        start_x = -3 * tensor_spacing  # Start from left
        tensor_positions = [np.array([start_x + i * tensor_spacing, 0, 0]) for i in range(7)]
        
        # Create all 7 tensor visualizations
        tensors = VGroup()
        tensor_labels = VGroup()
        arrows = VGroup()
        
        # Colors for different stages (can be adjusted)
        stage_colors = [BLUE, YELLOW, GRAY, GREEN, PURPLE, GRAY, GREEN]
        
        for i in range(7):
            # Create tensor visualization with larger cube size for zoomed view
            tensor_cubes = self.create_tensor_3d_cubes(
                S, B, D,
                tensor_positions[i],
                cube_size=0.12,  # Increased from 0.06 for better visibility in zoomed view
                color=stage_colors[i],
                opacity=0.7
            )
            tensors.add(tensor_cubes)
            
            # Create label for each stage (smaller font to fit in zoomed view)
            label = Tex(stage_labels[i], font_size=5, color=WHITE).scale(1.5)
            label.move_to(tensor_positions[i] + DOWN * 0.55)
            tensor_labels.add(label)
            
            # Create arrow from previous tensor (if not first)
            if i > 0:
                # Calculate actual tensor width to position arrows correctly
                # Tensor has S cubes along X-axis with spacing
                cube_size = 0.12
                spacing = cube_size * 1.3
                tensor_half_width = ((S - 1) / 2) * spacing + cube_size / 2
                
                # Arrow starts from right edge of previous tensor and ends at left edge of current tensor
                arrow_start = tensor_positions[i-1] + RIGHT * tensor_half_width
                arrow_end = tensor_positions[i] + LEFT * tensor_half_width
                
                arrow = Arrow(
                    arrow_start,
                    arrow_end,
                    color=WHITE,
                    stroke_width=1,
                    buff=0.02  # Small buff for arrow tip
                )
                arrows.add(arrow)
        
        # Animate the tensor transformation process
        # Show first tensor
        self.play(
            Create(tensors[0]),
            Write(tensor_labels[0]),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Show remaining tensors and arrows sequentially
        for i in range(1, 7):
            # Show arrow first
            self.play(Create(arrows[i-1]), run_time=0.5)
            self.wait(0.2)
            
            # Show tensor and label
            self.play(
                Create(tensors[i]),
                Write(tensor_labels[i]),
                run_time=0.5
            )
            self.wait(0.5)
        
        # Final wait
        self.wait(1)

        # Transform all tensors and arrows back into a single tensor at center
        # Create the final single tensor (same shape as initial)
        final_tensor = self.create_tensor_3d_cubes(
            S, B, D,
            ORIGIN,  # Center of scene
            cube_size=0.12,
            color=BLUE,  # Back to original color
            opacity=0.7
        )
        final_tensor_text = Tex("Layer Output", font_size=6, color=WHITE).scale(1.5)
        final_tensor_text.move_to(ORIGIN + DOWN * 0.5)
        # Group all elements to transform
        all_tensor_elements = VGroup(tensors, arrows, tensor_labels)
        
        # Transform everything back into single tensor
        self.play(
            ReplacementTransform(all_tensor_elements, final_tensor),
            Write(final_tensor_text),
            run_time=1.0
        )
        self.wait(1)
        
        # Zoom out camera first to show 5full view
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Transform final tensor back to original layer position
        self.play(
            FadeOut(final_tensor),
            FadeOut(final_tensor_text),
            run_time=0.5
        )
        self.wait(0.2)


