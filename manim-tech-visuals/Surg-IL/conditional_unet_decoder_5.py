from manim import *


class ConditionalUNetDecoderTable(Scene):
    """
    Scene displaying a rectangle divided into 5 columns and 10 rows.
    """
    
    def create_mlp(self, input_dim: int, output_dim: int, 
                    position: np.ndarray = ORIGIN,
                    node_radius: float = 0.3,
                    node_color: str = BLUE,
                    node_fill_opacity: float = 0.7,
                    layer_spacing: float = 4.0,
                    node_spacing: float = 0.8,
                    scale: float = 0.05):
        """
        Create an MLP visualization with input and output layers.
        
        Args:
            scale: Scale factor for the entire MLP (default: 1.0)
        
        Returns:
            tuple: (input_nodes, output_nodes, connections) as VGroups
        """
        # Create input layer nodes (circles)
        input_nodes = VGroup()
        for i in range(input_dim):
            node = Circle(
                radius=node_radius,
                color=node_color,
                fill_opacity=node_fill_opacity
            )
            # Position nodes vertically, centered
            y_pos = (i - (input_dim - 1) / 2) * node_spacing
            node.move_to(position + LEFT * layer_spacing / 2 + UP * y_pos)
            input_nodes.add(node)
        
        # Create output layer nodes (circles)
        output_nodes = VGroup()
        for i in range(output_dim):
            node = Circle(
                radius=node_radius,
                color=node_color,
                fill_opacity=node_fill_opacity
            )
            # Position nodes vertically, centered
            y_pos = (i - (output_dim - 1) / 2) * node_spacing
            node.move_to(position + RIGHT * layer_spacing / 2 + UP * y_pos)
            output_nodes.add(node)
        
        # Create connections between input and output layers
        connections = VGroup()
        for input_node in input_nodes:
            for output_node in output_nodes:
                connection = Line(
                    input_node.get_center(),
                    output_node.get_center(),
                    color=WHITE,
                    stroke_width=1
                )
                connections.add(connection)
        
        # Apply scale to all components
        if scale != 1.0:
            # Scale each component group around the center position
            center_point = position
            for group in [input_nodes, output_nodes, connections]:
                group.scale(scale, about_point=center_point)
        
        return input_nodes, output_nodes, connections
    
    def construct(self):
        # Define the outer rectangle dimensions
        rect_width = 8
        rect_height = 6
        
        # Create the outer rectangle
        outer_rect = Rectangle(
            width=rect_width,
            height=rect_height,
            color=WHITE,
            stroke_width=2
        )
        outer_rect.move_to(ORIGIN)
        
        # Create vertical lines to divide into 5 columns (need 4 lines)
        vertical_lines = VGroup()
        for i in range(1, 5):  # 4 vertical lines for 5 columns
            x_position = outer_rect.get_left()[0] + (rect_width / 5) * i
            line = Line(
                start=[x_position, outer_rect.get_bottom()[1], 0],
                end=[x_position, outer_rect.get_top()[1], 0],
                color=WHITE,
                stroke_width=1
            )
            vertical_lines.add(line)
        
        # Create horizontal lines to divide into 10 rows (need 9 lines)
        horizontal_lines = VGroup()
        for i in range(1, 10):  # 9 horizontal lines for 10 rows
            y_position = outer_rect.get_bottom()[1] + (rect_height / 10) * i
            line = Line(
                start=[outer_rect.get_left()[0], y_position, 0],
                end=[outer_rect.get_right()[0], y_position, 0],
                color=WHITE,
                stroke_width=1
            )
            horizontal_lines.add(line)
        
        # Group all elements together
        grid = VGroup(outer_rect, vertical_lines, horizontal_lines)
        
        # Display the grid
        self.play(Create(outer_rect), run_time=0.5)
        # Draw all vertical and horizontal lines simultaneously
        self.play(
            Create(vertical_lines),
            Create(horizontal_lines),
            run_time=0.5,
            lag_ratio=0
        )
        
        # Calculate cell dimensions
        cell_width = rect_width / 5
        cell_height = rect_height / 10
        
        # Create text labels for the first row (top row)
        row_texts = VGroup()
        text_labels = ["key[1]", "key[2]", "key[3]", ". . .", "key[i]"]
        
        for col in range(5):
            # Calculate the center position of each cell in the first row
            x_position = outer_rect.get_left()[0] + (cell_width * col) + (cell_width / 2)
            y_position = outer_rect.get_top()[1] - (cell_height / 2)
            
            # Create text
            text = Text(
                text_labels[col],
                font_size=20,
                color=WHITE
            )
            text.move_to([x_position, y_position, 0])
            row_texts.add(text)
        
        # Display the text labels
        self.play(Write(row_texts), run_time=1.0)
        
        # Create text labels for the last column (column 5) starting from row 2
        # Row 1 already has "key[i]", so we start from row 2 (index 1)
        last_col_texts = VGroup()
        # Text values for rows 2-6: value[i][1], value[i][2], value[i][3], ~, value[i][n]
        last_col_labels = [
            "value[i][1]",  # Row 2
            "value[i][2]",  # Row 3
            "value[i][3]",  # Row 4
            "value[i][4]",
            "value[i][5]",
            "value[i][6]",
            "value[i][7]",
            "~",            # Row 5 (before value[i][n])
            "value[i][n]"   # Row 6
        ]
        
        # Column 5 is the last column (index 4)
        col_index = 4
        x_position = outer_rect.get_left()[0] + (cell_width * col_index) + (cell_width / 2)
        
        # Add texts for rows 2-6 (row indices 1-5, since row 0 is the first row)
        for row in range(1, 10):  # Rows 2-9 (indices 1-8)
            # Calculate y position for each row (rows are numbered from top, so row 0 is top)
            # Row 2 is at index 1, so we need to go down from the top
            y_position = outer_rect.get_top()[1] - (cell_height * row) - (cell_height / 2)
            
            # Create text
            text = Text(
                last_col_labels[row - 1],  # row-1 because row starts at 1 but labels start at 0
                font_size=20,
                color=WHITE
            )
            text.move_to([x_position, y_position, 0])
            last_col_texts.add(text)
        
        # Display the last column text labels
        self.play(Write(last_col_texts), run_time=1.0)
        
        # Add red background to the last column to emphasize it
        last_col_rects = VGroup()
        col_index = 4  # Last column (column 5, index 4)
        x_center = outer_rect.get_left()[0] + (cell_width * col_index) + (cell_width / 2)
        
        # Create filled rectangles for all 10 rows in the last column
        for row in range(10):  # All 10 rows (indices 0-9)
            y_center = outer_rect.get_top()[1] - (cell_height * row) - (cell_height / 2)
            
            # Create a filled rectangle for each cell
            cell_rect = Rectangle(
                width=cell_width,
                height=cell_height,
                color=PURE_RED,
                fill_opacity=0.7,
                stroke_width=0  # No border, just fill
            )
            cell_rect.move_to([x_center, y_center, 0])
            last_col_rects.add(cell_rect)
        
        # Display the red background rectangles (behind the text)
        # Set z_index to ensure rectangles appear behind the text
        for rect in last_col_rects:
            rect.set_z_index(-1)
        
        # Animate the red background appearing
        self.play(FadeIn(last_col_rects), run_time=0.8)
        self.wait(1.2)
        
        # Move camera perspective to the right (shift everything left)
        all_visible = VGroup(
            outer_rect, vertical_lines, horizontal_lines, 
            row_texts, last_col_texts, last_col_rects
        )
        self.play(all_visible.animate.shift(LEFT * 7), run_time=1.5)
        self.wait(0.5)
        
        # Move last_col_rects to the right of outer_rect and rotate 90 degrees
        # Calculate target position: right of outer_rect with some spacing
        target_x = outer_rect.get_right()[0] + (rect_width / 2) + 1.0
        target_y = outer_rect.get_center()[1]
        
        # Get the current center of last_col_rects
        current_center = last_col_rects.get_center()
        
        # Animate: move to the right, rotate 90 degrees, and adjust height simultaneously
        # Adjust height by scaling vertically (you can change the scale factor as needed)
        self.play(
            last_col_rects.animate.move_to([target_x, target_y, 0])
                            .rotate(PI/2)
                            .stretch(0.5, 1),  # Stretch height by 2x (adjust as needed)
            run_time=2.0
        )
        self.wait(0.5)
        
        # Add text "ActionHead (        )" below the rotated rectangles
        action_head_text = Text(
            "ActionHead (           )",
            font_size=24,
            color=WHITE
        )
        # Position text below the rotated rectangles
        text_y = last_col_rects.get_bottom()[1] - 1.0
        action_head_text.move_to([target_x, text_y, 0])
        
        # Display the text
        self.play(Write(action_head_text), run_time=1.0)
        self.wait(0.5)
        
        # Animate: shrink all rectangles and move to center, then show combined rectangle
        self.play(
            last_col_rects.animate.scale(0.15).move_to(action_head_text.get_center() + RIGHT * 0.9),
            run_time=1.2
        )
        self.wait(0.5)
        
        # Move both last_col_rects and action_head_text up
        self.play(
            last_col_rects.animate.shift(UP * 3.5),
            action_head_text.animate.shift(UP * 3.5),
            run_time=1.2
        )
        self.wait(0.5)
        
        # Create two rectangles with dotted/dashed line 
        rect1 = Rectangle(
            width=0.8,
            height=1.2,
            color=WHITE,
            stroke_width=2
        )
        rect2 = Rectangle(
            width=0.8,
            height=1.2,
            color=WHITE,
            stroke_width=2
        )
        # Convert to dashed/dotted rectangles
        dotted_rect1 = DashedVMobject(rect1, num_dashes=15, dashed_ratio=0.5)
        dotted_rect2 = DashedVMobject(rect2, num_dashes=15, dashed_ratio=0.5)
        # Position first rectangle, then position second with 1.0 margin
        dotted_rect1.move_to(ORIGIN)
        dotted_rect2.next_to(dotted_rect1, RIGHT, buff=1.0)
        
        # Add "block" text inside each dotted rectangle
        block_text1 = Text("block", font_size=16, color=WHITE)
        block_text1.move_to(dotted_rect1.get_center())
        block_text2 = Text("block", font_size=16, color=WHITE)
        block_text2.move_to(dotted_rect2.get_center())
        
        # Add "optional" text below the two dotted rectangles
        optional_text = Text("optional", font_size=14, color=WHITE)
        optional_text.move_to((dotted_rect1.get_bottom() + dotted_rect2.get_bottom()) / 2 + DOWN * 0.5)
        
        # Display rectangles and texts
        self.play(
            Create(dotted_rect1),
            Create(dotted_rect2),
            Write(block_text1),
            Write(block_text2),
            run_time=1.0,
            lag_ratio=0
        )
        self.wait(0.3)
        self.play(Write(optional_text), run_time=0.8)
        self.wait(0.5)
        
        # Draw arrow between the two dotted rectangles
        arrow_between_rects = Arrow(
            dotted_rect1.get_right(),
            dotted_rect2.get_left(),
            color=WHITE,
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.2,  # Adjust arrowhead size (0.1 = small, 0.3 = large)
            # tip_length=0.3,  # Alternative: set absolute arrowhead length
        )
        # Adjust arrow scale (optional - uncomment and adjust value as needed)
        self.play(Create(arrow_between_rects), run_time=0.8)
        self.wait(0.3)
        
        # Example: Create and display an MLP
        # Position the MLP next to dotted_rect2
        mlp_position = dotted_rect2.get_center() + RIGHT * 2.5
        
        # Draw arrow from dotted_rect2 to MLP position
        arrow_to_mlp = Arrow(
            dotted_rect2.get_right(),
            mlp_position + LEFT * 1.0,  # Point to the left side of MLP (input layer)
            color=WHITE,
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.25,
        )
        input_nodes, output_nodes, connections = self.create_mlp(
            input_dim=5,
            output_dim=3,
            position=mlp_position,
            scale=0.35  # Adjust scale as needed (0.8 = 80% size, 1.5 = 150% size, etc.)
        )
        
        # Display the arrow to MLP before showing the MLP
        self.play(Create(arrow_to_mlp), run_time=0.8)
        self.wait(0.3)
        
        # Animate the MLP
        # Draw input and output nodes simultaneously
        self.play(
            Create(input_nodes),
            Create(output_nodes),
            run_time=1.0,
            lag_ratio=0
        )
        self.wait(0.5)
        self.play(Create(connections), run_time=1.0, lag_ratio=0.01)
        self.wait(0.5)
        
        # Group all elements together
        all_elements = VGroup(
            dotted_rect1, dotted_rect2,
            block_text1, block_text2,
            optional_text,
            arrow_between_rects,
            arrow_to_mlp,
            input_nodes, output_nodes, connections
        )
        
        # Create a rectangle that encompasses all elements
        # Get the boundaries of all elements
        left_bound = all_elements.get_left()[0]
        right_bound = all_elements.get_right()[0]
        top_bound = all_elements.get_top()[1]
        bottom_bound = all_elements.get_bottom()[1]
        
        # Calculate width and height with some padding
        padding = 0.3
        container_width = (right_bound - left_bound) + (padding * 2)
        container_height = (top_bound - bottom_bound) + (padding * 2)
        container_center = all_elements.get_center()
        
        # Create the container rectangle
        container_rect = Rectangle(
            width=container_width,
            height=container_height,
            color=WHITE,
            stroke_width=2
        )
        container_rect.move_to(container_center)
        
        # Display the container rectangle
        self.play(Create(container_rect), run_time=0.8)
        self.wait(1.5)
        
        # Draw a rectangle and divide it into 5 rectangles
        outer_rect_width = 4
        outer_rect_height = 0.8
        
        # Create the outer rectangle
        divided_outer_rect = Rectangle(
            width=outer_rect_width,
            height=outer_rect_height,
            color=WHITE,
            stroke_width=2
        )
        # Position below optional_text
        divided_outer_rect.next_to(optional_text, DOWN , buff=0.8)
        
        # Create 4 vertical lines to divide into 5 rectangles
        divided_rects = VGroup()
        cell_width = outer_rect_width / 8
        
        # Create 5 inner rectangles
        for i in range(8):
            inner_rect = Rectangle(
                width=cell_width,
                height=outer_rect_height,
                color=WHITE,
                stroke_width=1,
                fill_opacity=0.1
            )
            x_position = divided_outer_rect.get_left()[0] + (cell_width * i) + (cell_width / 2)
            y_position = divided_outer_rect.get_center()[1]
            inner_rect.move_to([x_position, y_position, 0])
            divided_rects.add(inner_rect)
        
        # Adjust scale of the entire divided rectangle group
        scale_factor = 0.5  # Change this value: 0.5 = 50%, 1.0 = 100%, 1.5 = 150%, 2.0 = 200%
        if scale_factor != 1.0:
            # Scale both outer rectangle and inner rectangles together
            divided_group = VGroup(divided_outer_rect, divided_rects)
            center_point = divided_outer_rect.get_center()
            divided_group.scale(scale_factor, about_point=center_point)
        
        # Display the outer rectangle first
        self.play(Create(divided_outer_rect), run_time=0.8)
        self.wait(0.3)
                
        # Display the divided rectangles
        self.play(Create(divided_rects), run_time=1.2, lag_ratio=0.1)
        self.wait(2)
        
        # Iterate the process for each divided rectangle
        # Process each of the 5 divided rectangles (or iterate multiple times)
        num_iterations = 2  # Number of times to iterate (one for each divided rectangle)
        
        iteration_results = []
        iteration_rects = []  # Track rectangles added next to divided_outer_rect
        iteration_divided_rects = []  # Track new_divided_rects for each iteration
        for i in range(num_iterations):
            # Use cell_rect structure (same as lines 197-205) - start from target position (lines 224-227)
            iter_rects = VGroup()
            # Use the same target position as lines 226-227 (where last_col_rects moves to before rotating)
            col_index = 4  # Last column (column 5, index 4)
            x_center = outer_rect.get_left()[0] + ((rect_width / 5) * col_index) + ((rect_width / 5) / 2)
            
            # Create filled rectangles for all 10 rows (same structure as lines 192-205)
            for row in range(10):  # All 10 rows (indices 0-9)
                # Arrange 10 rectangles vertically centered at target_y
                y_center = outer_rect.get_top()[1] - ((rect_height / 10) * row) - ((rect_height / 10) / 2)

                # Create a filled rectangle for each cell (same as lines 197-203)
                cell_rect = Rectangle(
                    width=rect_width / 5,
                    height=rect_height / 10,
                    color=PURE_RED,
                    fill_opacity=0.7,
                    stroke_width=0  # No border, just fill
                )
                cell_rect.move_to([x_center, y_center, 0])
                iter_rects.add(cell_rect)
            
            # Set z_index
            for rect in iter_rects:
                rect.set_z_index(-1)
            
            # Step 1: Display rectangles
            self.play(FadeIn(iter_rects), run_time=0.6)
            self.wait(0.3)

            # Step 2: Move, rotate, and scale the rectangles to the current location of action_head_text (lines 256-261)
            # action_head_text is at its final position after being moved up
            target_position = action_head_text.get_center() + RIGHT * 0.9
            
            self.play(
                iter_rects.animate.scale(0.15)
                                .move_to(target_position)
                                .rotate(PI/2),
                run_time=1.2
            )
            self.wait(0.5)
            
            # Add rectangle next to divided_outer_rect at each iteration (same structure as lines 364-402)
            # Create the outer rectangle
            new_outer_rect = Rectangle(
                width=outer_rect_width,
                height=outer_rect_height,
                color=WHITE,
                stroke_width=2
            )
            
            # Create inner rectangles (same as lines 378-394)
            new_divided_rects = VGroup()
            cell_width = outer_rect_width / 8
            
            # Create 8 inner rectangles
            for j in range(8):
                inner_rect = Rectangle(
                    width=cell_width,
                    height=outer_rect_height,
                    color=WHITE,
                    stroke_width=1,
                    fill_opacity=0.1
                )
                # Position will be set after outer rectangle is positioned
                new_divided_rects.add(inner_rect)
            
            # Position outer rectangle next to the LEFT of divided_outer_rect (or previous rectangle)
            # Use buff=0 to remove margin between rectangles
            if i == 0:
                # First iteration: add to the left of divided_outer_rect
                new_outer_rect.next_to(divided_outer_rect, LEFT, buff=0)
            else:
                # Subsequent iterations: add to the left of the previous new_outer_rect
                new_outer_rect.next_to(iteration_rects[i-1], LEFT, buff=0)
            
            # Position inner rectangles relative to the outer rectangle (before scaling)
            for j, inner_rect in enumerate(new_divided_rects):
                x_position = new_outer_rect.get_left()[0] + (cell_width * j) + (cell_width / 2)
                y_position = new_outer_rect.get_center()[1]
                inner_rect.move_to([x_position, y_position, 0])
            
            # Apply scale to the entire group together
            scale_factor = 0.5
            if scale_factor != 1.0:
                new_divided_group = VGroup(new_outer_rect, new_divided_rects)
                center_point = new_outer_rect.get_center()
                new_divided_group.scale(scale_factor, about_point=center_point)
                
                # After scaling, reposition the outer rectangle to ensure no margin
                # This will move the whole group since inner rectangles are positioned relative to it
                if i == 0:
                    new_outer_rect.next_to(divided_outer_rect, RIGHT, buff=0)
                else:
                    new_outer_rect.next_to(iteration_rects[i-1], RIGHT, buff=0)
                
                # Reposition inner rectangles relative to the repositioned outer rectangle
                scaled_cell_width = cell_width * scale_factor
                for j, inner_rect in enumerate(new_divided_rects):
                    x_position = new_outer_rect.get_left()[0] + (scaled_cell_width * j) + (scaled_cell_width / 2)
                    y_position = new_outer_rect.get_center()[1]
                    inner_rect.move_to([x_position, y_position, 0])
            
            # Display the outer rectangle first
            self.play(Create(new_outer_rect), run_time=0.5)
            self.wait(0.2)
            # Display the divided rectangles
            self.play(Create(new_divided_rects), run_time=0.6, lag_ratio=0.1)
            self.wait(0.3)
            
            # Store the outer rectangle and divided rects AFTER positioning and scaling
            iteration_rects.append(new_outer_rect)
            iteration_results.append(iter_rects)
            iteration_divided_rects.append(new_divided_rects)
        
        self.wait(1.0)

        # Add all three text labels at the same time
        # Create and position "position" text below divided_outer_rect
        position_text = Text("position", font_size=18, color=WHITE)
        position_text.next_to(divided_outer_rect, DOWN, buff=0.3)
        
        # Create and position "orientation" text below the first iteration_rects
        orientation_text = None
        if len(iteration_rects) > 0:
            orientation_text = Text("orientation", font_size=18, color=WHITE)
            orientation_text.next_to(iteration_rects[0], DOWN, buff=0.3)
        
        # Create and position "gripper" text below the second iteration_rects
        gripper_text = None
        if len(iteration_rects) > 1:
            gripper_text = Text("gripper", font_size=18, color=WHITE)
            gripper_text.next_to(iteration_rects[1], DOWN, buff=0.3)
        
        # Display all texts simultaneously
        texts_to_write = [position_text]
        if orientation_text:
            texts_to_write.append(orientation_text)
        if gripper_text:
            texts_to_write.append(gripper_text)
        
        self.play(*[Write(text) for text in texts_to_write], run_time=0.8, lag_ratio=0)
        self.wait(0.3)
        
        denoised_text = Text("denoised   actions  =  ", font_size=20, color=WHITE)
        denoised_text.next_to(divided_outer_rect, LEFT, buff=0.2)
        self.play(Write(denoised_text), run_time=1.0)
        self.wait(0.5)
        
        # Group all elements that will transition to the formula
        elements_to_transform = VGroup(
            denoised_text,
            position_text,
            divided_outer_rect,
            divided_rects
        )
        if orientation_text:
            elements_to_transform.add(orientation_text)
        if gripper_text:
            elements_to_transform.add(gripper_text)
        
        # Add all iteration results (iter_rects) to the group
        for iter_rects in iteration_results:
            elements_to_transform.add(iter_rects)
        
        # Add all iteration rectangles (new_outer_rect) to the group
        for iter_rect in iteration_rects:
            elements_to_transform.add(iter_rect)
        
        # Add all iteration divided rectangles (new_divided_rects) to the group
        for new_divided_rects in iteration_divided_rects:
            elements_to_transform.add(new_divided_rects)
        
        # Create LaTeX formula positioned below container_rect
        formula = MathTex(
            r"\mathcal{L}(\theta) = \left\| \mathbf{v}_\theta(t, \mathbf{x}_t) - \mathbf{u}_t \right\|_2^2",
            font_size=48,
            color=WHITE
        )
        formula[0][6:14].set_color(YELLOW)
        
        formula.next_to(container_rect, DOWN, buff=0.5)
        
        # Transition from grouped elements to formula
        self.play(ReplacementTransform(elements_to_transform, formula), run_time=1.5)        
        self.wait(1.0)
        
    

