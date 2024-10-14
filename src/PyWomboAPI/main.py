from typing import List, Tuple, Optional
from . import generation, init
from .models import Credentials, Task
import logging
import asyncio
logger = logging.getLogger(__name__)

class WomboAPI:
    def __init__(self,log_level=logging.WARNING):
        # Set up logging configuration here
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('my_package.log', mode='w')  # 'w' to overwrite log file each time
            ]
        )
        self.credentials: Optional[Credentials] = None
        self.styles: Optional[List[Tuple[int, str, bool, Optional[str]]]] = None


    def setup(self,api_key: Optional[str] = None, auth_token: Optional[str] = None) -> Credentials:
        """
        Set up the necessary authentication to be able to generate images.

        Parameters:
        ----------
        api_key (Optional[str]): Optional! self-provided API key in case you already have it (skips API key fetching)

        auth_token (Optional[str]): Optional! In case you already have an auth token (ex: premium token for premium styles)

        Returns:
        -------
        Credentials: The initialized credentials object with the API key and auth token (bearer).
        """

        credentials = init.initialize(api_key, auth_token)
        self.credentials = credentials
        return credentials

    def fetch_styles(self,include_premium=False,fetch_thumbnails=False) ->List[Tuple[int, str, bool, Optional[str]]]:
        """
        Get the list of styles to use.
        Parameters:
        ----------
        include_premium: Optional! Can be used if you want to include the premium styles (NOT supported by standard Credentials)
        fetch_thumbnails: Optional!: This will include the links to every styles' thumbnail, useful for web-apps.
        Returns:
        ----------
        A list of styles in the shape of: List[Tuple[style_id, style_name, is_premium, Optional[thumbnail_url]]]:
            """
        if include_premium:
            logger.warning("Including premium styles, these do NOT work with the automatically generated bearers!")

        self.styles = init.fetch_styles(include_premium, fetch_thumbnails)
        return self.styles

    async def start_task(self,style_id:int,prompt:str,is_premium=False) -> Task:
        """
        Start the generation of an image
        Parameters:
        ----------
        style_id: The ID of the requested style.
        prompt: Image content.
        is_premium: is this a premium style?

        Returns:
        -------
        Task: The initialized Task object with all it's data.
        """
        return await generation.start_task(self.credentials, style_id, prompt, is_premium)

    async def check_task(self,task:Task):
        return await generation.check_task(task)

    def renew_auth_token(self):
        self.credentials.auth_token = init.get_auth_token(self.credentials.api_key)


    async def create_image(self,style_id:int,prompt:str,is_premium=False) -> Task:
        try:
            image_task = await self.start_task(style_id, prompt,is_premium)
            while not image_task.completed:
                await asyncio.sleep(1)
                await self.check_task(image_task)
            return image_task
        except Exception as e:
            raise Exception(f"Generation for prompt={prompt} with style_id={style_id} failed.")

    async def create_image_batch(self, style_id: int, prompt: str, image_count: int,unsafe_custom_delay:int = None, is_premium=False,graceful=False):
        if graceful:
            logger.warning("Graceful errors are enabled, failed generations will not be critical!")
        async def generate_image(follow_ind):
            try:
                image_result = await self.create_image(style_id, prompt, is_premium)
                return image_result
            except Exception as e:
                if not graceful:
                    raise e
                else:
                    return None

        tasks = []

        for i in range(image_count):
            task = asyncio.create_task(generate_image(i))
            tasks.append(task)
            await asyncio.sleep(unsafe_custom_delay if unsafe_custom_delay is not None else 0.5)

        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                yield result