from manim import *
from pathlib import Path

# Paths: images in same folder as this script (project root)
SCRIPT_DIR = Path(__file__).resolve().parent
IMAGES_DIR = SCRIPT_DIR


class Intro(MovingCameraScene):
    """
    Intro scene: Attention.png at center, then Transformer to its right,
    Vision_Backbone to the right of Transformer, then Cube and NLP/VLM/VLA labels.
    """

    def construct(self):
        # Zoom out and keep camera zoomed out for the whole scene
        self.camera.frame.scale(1.5)

        # 1. Show Attention.png at center
        attention_path = IMAGES_DIR / "Attention.png"
        attention_img = ImageMobject(str(attention_path))
        # Scale so that three images in a row fit the frame
        attention_img.scale_to_fit_width(config.frame_width * 0.44)
        attention_img.move_to(ORIGIN)
        self.add(attention_img)
        self.wait(2)

        # 2. Move camera right so Transformer is at center, then FadeIn Transformer_full_architecture.png
        transformer_path = IMAGES_DIR / "Transformer_full_architecture.png"
        transformer_img = ImageMobject(str(transformer_path))
        transformer_img.scale_to_fit_height(attention_img.get_height())
        transformer_img.next_to(attention_img, RIGHT * 4.5, buff=0.4)
        #transformer_img.set_opacity(0)
        self.add(transformer_img)
        self.play(
            self.camera.frame.animate.move_to(transformer_img.get_center()),
            FadeIn(transformer_img),
            run_time=1.5,
        )
        self.wait(0.5)

        # 3. SurroundingRectangle around Transformer image + "NLP" below (FadeIn)
        transformer_rect = SurroundingRectangle(
            transformer_img, color=WHITE, buff=0.15
        )
        nlp_text = Tex("NLP", font_size=28, color=WHITE)
        nlp_text.next_to(transformer_rect, DOWN, buff=0.2)
        self.play(FadeIn(transformer_rect), FadeIn(nlp_text), run_time=1.0)
        self.wait(0.5)

        # 4. Move camera right so Vision_Backbone is at center, then FadeIn Vision_Backbone.png
        vision_path = IMAGES_DIR / "Vision_Backbone.png"
        vision_img = ImageMobject(str(vision_path))
        vision_img.scale_to_fit_height(transformer_img.get_height())
        vision_img.next_to(transformer_img, RIGHT * 4.5, buff=0.4)
        vision_backbone_text = Tex("Vision Backbone", font_size=28, color=WHITE)
        vision_backbone_text.next_to(vision_img, DOWN, buff=0.2)
        #vision_img.set_opacity(0)
        self.add(vision_img, vision_backbone_text)
        self.play(
            self.camera.frame.animate.move_to(vision_img.get_center()),
            FadeIn(vision_img),
            FadeIn(vision_backbone_text),
            run_time=1.0,
        )
        self.wait(0.5)

        # SurroundingRectangle around the two images only, "VLM" below
        vlm_group = Group(transformer_img, vision_img, vision_backbone_text, nlp_text)
        vlm_rect = SurroundingRectangle(vlm_group, color=BLUE, buff=0.25)
        vlm_text = Tex("VLM", font_size=28, color=WHITE)
        vlm_text.next_to(vlm_rect, DOWN, buff=0.2)
        self.play(FadeIn(vlm_rect), FadeIn(vlm_text), run_time=1.0)
        self.wait(0.5)

        # 5. RoundedRectangle to the right of Vision_Backbone + "Action Decoder" Tex
        cube = RoundedRectangle(corner_radius=0.5, height=vision_img.get_height())
        cube.set_fill(color=TEAL, opacity=0.3)
        cube.set_stroke(color=WHITE, width=2)
        cube.next_to(vision_img, RIGHT * 2.5, buff=0.8)
        #cube.set_opacity(0)
        action_decoder_text = Tex("Action Decoder", font_size=30, color=WHITE)
        action_decoder_text.next_to(cube, DOWN, buff=0.15)
        #action_decoder_text.set_opacity(0)
        self.add(cube, action_decoder_text)
        self.play(FadeIn(cube), FadeIn(action_decoder_text), run_time=1.0)
        self.wait(0.5)

        # 6. SurroundingRectangle around Transformer, Vision_Backbone, Cube + "VLA" below
        vla_group = Group(
            transformer_img,
            transformer_rect,
            nlp_text,
            vlm_text,
            vision_img,
            vision_backbone_text,
            cube,
            vlm_rect,
            action_decoder_text,
        )
        vla_rect = SurroundingRectangle(vla_group, color=YELLOW, buff=0.35)
        vla_text = Tex("VLA", font_size=40, color=YELLOW)
        vla_text.next_to(vla_rect, DOWN, buff=0.25)
        #vla_text.set_opacity(0)
        self.add(vla_rect, vla_text)
        self.play(FadeIn(vla_rect), FadeIn(vla_text), run_time=1.0)
        self.wait(2)

