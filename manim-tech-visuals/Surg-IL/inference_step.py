from manim import *
import numpy as np


class InferenceStep(Scene):
    """
    Animation showing Timestep value changing from 0.0 to 1.0
    based on inference step count.
    """
    
    def construct(self):
        # Set inference step (change this value: 10, 25, or 50)
        inference_step = 10
        
        # Create fixed "Timestep = " part
        timestep_label = MathTex(r"\text{Timestep} = ", font_size=36, color=WHITE)
        # Create dynamic value part (starts at 0.0)
        timestep_value_text = MathTex("0.0", font_size=36, color=YELLOW)
        
        # Combine them
        timestep_display = VGroup(timestep_label, timestep_value_text)
        timestep_display.arrange(RIGHT, buff=0.15)
        timestep_display.move_to(ORIGIN)
        
        # Store the position for the value text
        timestep_value_position = timestep_value_text.get_center()
        
        # Show initial text
        self.play(FadeIn(timestep_display), run_time=1.0)
        self.wait(0.5)
        
        # Calculate step size: 1.0 / inference_step
        step_size = 1.0 / inference_step
        
        # Determine decimal places based on inference_step
        # 10 -> 1 decimal place (0.1), 25/50 -> 2 decimal places (0.04, 0.02)
        if inference_step == 10:
            decimal_places = 1
        else:  # 25 or 50
            decimal_places = 2
        
        # Animate timestep value from 0.0 to 1.0 in steps
        for step in range(1, inference_step + 1):
            current_value = step * step_size
            
            # Create new value text with appropriate decimal places
            format_str = f"{{:.{decimal_places}f}}"
            new_value = MathTex(format_str.format(current_value), font_size=36, color=YELLOW)
            new_value.move_to(timestep_value_position)
            
            # Transform to new value
            self.play(
                Transform(timestep_value_text, new_value),
                run_time=0.3
            )
        
        self.wait(1.0)

