# Note: In order to run the program, the line "import cached_download" must be deleted in the file dynamic_modules_utils.py within the diffusers library. Don't ask why.
import torch
from diffusers import DiffusionPipeline
from transformers import pipeline
from PIL import Image

"""
Use the following prompt to generate an effective summary:

    f"You are part of a project to find the optimal spot to build an 
    NFL stadium in the city of {city}. Our model has predicted that the optimal location 
    will involving replacing land with a value of ${landCost} to build a stadium with {seatCount} 
    seats. The image provided is the optimal spot for the stadium. 
    Create a short and straightforward report promoting the stadium product, 
    mentioning both how it will positively impact the city and bring in income for 
    the city through various events. Explain why the location in the top down view provided 
    is a good location to build a stadium. Include detailed financial projections based on 
    the number of seats and invested cost. Make sure to include a team name inspired by the city. 
    Respond with the report itself rather than a chatbot response."

Model: https://huggingface.co/ibm-granite/granite-vision-3.1-2b-preview
"""
def generateSummary(imageUrl, prompt):
    formattedPrompt = [
    {"role": "programmer", "content": [
        {"type": "image", "url": imageUrl}, 
        {"type": "text", "text": prompt}]},
    ]
    summarizer = pipeline("image-text-to-text", model="ibm-granite/granite-vision-3.1-2b-preview")
    return summarizer(formattedPrompt)

# Will be replaced with OpenAI
def generateText(prompt):
    llama = pipeline("text-generation", model="unsloth/Llama-3.2-1B")
    response = llama(prompt)[0]
    return response

# Will be replaced with OpenAI
def generateImage(prompt):
    diffusion = DiffusionPipeline.from_pretrained("lambdalabs/miniSD-diffusers")
    images = diffusion(prompt)
    return images.images[0]

def overlayImage(base, overlay, pos):
    return base.paste(overlay, base, pos)

def main():
    print("This is a main function for testing purposes")
    image = generateImage("A football team known as the Tusla Tornadoes winning the Super Bowl")
    image.save("tuslaSuperBowl.jpg")
    print("Main complete")

if __name__ == "__main__":
    main()