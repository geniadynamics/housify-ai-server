import requests
from PIL import Image, ImageOps
import torch
from diffusers import (
    StableDiffusionInstructPix2PixPipeline,
    EulerAncestralDiscreteScheduler,
)


async def edit_image(url: str, prompt: str):
    try:
        pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
            "timbrooks/instruct-pix2pix", torch_dtype=torch.float16, safety_checker=None
        )
        pipe.to("cuda")
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
            pipe.scheduler.config
        )

        def load_image(file_path: str) -> Image.Image:
            image = Image.open(file_path)
            image = ImageOps.exif_transpose(image)
            return image.convert("RGB")

        image = load_image(url)
        edited_image = pipe(
            prompt, image=image, num_inference_steps=10, image_guidance_scale=1
        ).images[0]

        return edited_image

    finally:
        if "pipe" in locals():
            del pipe
        torch.cuda.empty_cache()
