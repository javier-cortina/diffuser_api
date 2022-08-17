from fastapi import APIRouter
from fastapi.responses import FileResponse
from diffusers import DiffusionPipeline
import os
from datetime import datetime

router = APIRouter(
    prefix="/generate",
    tags=["generate"]
)

# load model and scheduler
print("Loading Model...")
model_id = "CompVis/ldm-text2im-large-256"
ldm = DiffusionPipeline.from_pretrained(model_id)
print("Done!")

# Endpoint
@router.get("/")
def generate(prompt: str, num_inference_steps=50, eta=0.3, guidance_scale=6):    
    # run pipeline in inference (sample random noise and denoise)
    image = ldm(
        [prompt], 
        num_inference_steps=num_inference_steps, 
        eta=eta, 
        guidance_scale=guidance_scale
    )["sample"][0]
    
    # save image
    previous_images = os.listdir("generated_images\\images")
    last_image_number = max([int(i.split("_")[1].split(".")[0]) for i in previous_images])
    new_img_directory = f"generated_images\\images\\img_{str(last_image_number+1).zfill(6)}.png"
    image.save(new_img_directory)

    # log prompt
    log_file = open("generated_images\\_prompts.log", "a")
    log_file.write(f"\n{str(last_image_number+1).zfill(6)},{datetime.now()},{prompt}")
    log_file.close()

    return FileResponse(new_img_directory)