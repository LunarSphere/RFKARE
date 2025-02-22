# Note: In order to run the program, the line "import cached_download" must be deleted in the file dynamic_modules_utils.py within the diffusers library. Don't ask why.
import torch
from diffusers import DiffusionPipeline
from transformers import pipeline
from PIL import Image

def generateText(role, prompt):
    messages = [{"role": role, "content": prompt}]
    deepseek = pipeline("text-generation", model="deepseek-ai/deepseek-llm-7b-base")
    return deepseek(messages)

def generateImage(prompt):
    diffusion = DiffusionPipeline.from_pretrained("OFA-Sys/small-stable-diffusion-v0", torch_dtype=torch.float16)
    images = diffusion(prompt)
    return images.images[0]

def overlayImage(base, overlay, pos):
    return base.paste(overlay, base, pos)

def main():
    #img = generateImage("A football stadium")
    text = generateText("User", "Hello, this is a test message.")
    print(text)
    #img.save("C:/Users/wyatt/OneDrive/Desktop/hacklytics/test.jpg")

if __name__ == "__main__":
    main()