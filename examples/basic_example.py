import asyncio
import logging
from PyWomboAPI import WomboAPI

async def main() -> None:
    api = WomboAPI(log_level=logging.INFO)  #log level set to INFO to see what's going on
    api.setup() #requesting all the data needed
    image = await api.create_image(140, "flying car")   #starting image generation
    print(image.url)

if __name__ == '__main__':
    asyncio.run(main())
