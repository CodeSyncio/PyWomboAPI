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

    async def generate_and_download(index):
        result = await API.create_image(style_id, prompt)
        image_url = result.url
        download_image(image_url, foldername, f"image_{index}.jpg")
        print(f"Downloaded image {index}: {image_url}")

    tasks = [generate_and_download(i) for i in range(1, image_amount + 1)]
    await asyncio.gather(*tasks)

    print("Done generating and downloading images")


if __name__ == '__main__':
    asyncio.run(main())
