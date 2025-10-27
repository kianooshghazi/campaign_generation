from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import os
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

class ImageGenerator:
    def generate(self, prompt, width, height):
        pipe = StableDiffusionPipeline.from_pretrained(
                "CompVis/stable-diffusion-v1-4",
                dtype=torch.float32,
                use_auth_token=True
            )
        pipe = pipe.to("cpu")
        image = pipe(prompt, num_inference_steps=50).images[0]

        if (image.width, image.height) != (width, height):
            image = image.resize((width, height))
        return image
