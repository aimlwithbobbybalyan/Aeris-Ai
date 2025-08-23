import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Ensure the Data folder exists
os.makedirs("Data", exist_ok=True)

def open_image(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")


API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}


async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Image generated. Size: {len(response.content)} bytes")
            return response.content
        else:
            print(f"API Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None


async def generate_images(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            path = fr"Data\{prompt.replace(' ', '_')}{i+1}.jpg"
            with open(path, "wb") as f:
                f.write(image_bytes)
            print(f"Saved: {path}")
        else:
            print(f"Image {i+1} generation failed. Skipping save.")


def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_image(prompt)


# Main loop for checking generation requests
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            data: str = f.read()

        Prompt, Status = data.strip().split(",")

        if Status == "True":
            print("Generating Images...")
            GenerateImages(prompt=Prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
        else:
            sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        sleep(1)
