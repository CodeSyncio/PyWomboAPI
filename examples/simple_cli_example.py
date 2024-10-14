import os
import asyncio
import requests
from PyWomboAPI import WomboAPI


def download_image(url, foldername, name):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    with open(os.path.join(foldername, name), 'wb') as file:
        file.write(requests.get(url).content)

async def main() -> None:
    API = WomboAPI()
    API.setup()
    styles = API.fetch_styles()

    for style in styles:
        print(f"{style[0]}: {style[1]}")

    style_id = int(input("Choose a style (enter ID!): ").strip())
    prompt = input("Prompt: ").strip()
    image_amount = int(input("How many images should be generated?: ").strip())

    foldername = prompt.replace(' ', '_')

    # Use create_image_batch to generate multiple images
    async for result in API.create_image_batch(style_id, prompt, image_amount):
        image_url = result.url
        download_image(image_url, foldername,
                       f"image_{result.id}.jpg")
        print(f"Downloaded image: {image_url}")

    print("Done generating and downloading images")


if __name__ == '__main__':
    asyncio.run(main())
