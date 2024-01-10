from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image
import torch


async def classify_image(image_path: str) -> str:
    try:
        model = LlavaForConditionalGeneration.from_pretrained(
            "llava-hf/llava-1.5-7b-hf",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        ).to(0)

        processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")

        raw_image = Image.open(image_path)
        inputs = processor(
            "<image>\nUSER: Describe the following image\nASSISTANT:",
            raw_image,
            return_tensors="pt",
        ).to(0, torch.float16)

        output = model.generate(**inputs, max_new_tokens=4, do_sample=False)
        analysis_result = processor.decode(output[0][2:], skip_special_tokens=True)
        return analysis_result
    finally:
        if "model" in locals():
            del model
        if "processor" in locals():
            del processor
        torch.cuda.empty_cache()
