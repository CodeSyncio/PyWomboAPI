import logging
import aiohttp
from .statics import generation_headers
from .models import Task, Credentials
logger = logging.getLogger(__name__)

async def start_task(credentials: Credentials, style_id: int, prompt: str, is_premium=False) -> Task:
    try:
        headers = generation_headers(credentials.auth_token)
    except Exception as e:
        logger.error(f"Unknown error occurred while trying to generate the request headers for bearer {credentials.auth_token}: {e}")
        raise

    post_data = {
        "is_premium": is_premium,
        "input_spec": {
            "aspect_ratio": "old_vertical_ratio",
            "prompt": prompt,
            "style": style_id,
            "display_freq": 10
        }
    }
    logger.info("Consructed POST data for start_task request: %s",post_data)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://paint.api.wombo.ai/api/v2/tasks", json=post_data, headers=headers) as response:
                response.raise_for_status()

                response_json = await response.json()
                logger.info("Received task data: %s", response_json)

                task_id = response_json["id"]
                state = response_json["state"]
                if task_id is None or state is None:
                    raise ValueError("Task does not have an id / state, probably a broken task.")
                task = Task(task_id, state, False, bearer=credentials.auth_token)
                logger.info("Constructed Task data: %s",task)
                return task

    except aiohttp.ClientResponseError as e:
        logger.error(f"HTTP error occurred during the start_task request: {e.status} {e.message}")
        raise
    except aiohttp.ClientError as e:
        logger.error(f"Client error occurred during the start_task request: {e}")
        raise
    except ValueError as e:
        logger.error(f"Unknown ValueError: {e}")
        raise
    except Exception as e:
        logger.error(f"An Unknown error occurred during the start_task request: {e}")
        raise

async def check_task(task: Task) -> Task:
    try:
        headers = generation_headers(task.bearer)
    except Exception as e:
        logger.error(
            f"Unknown error occurred while trying to generate the request headers for bearer {task.bearer}: {e}")
        raise

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://paint.api.wombo.ai/api/v2/tasks/{task.id}', headers=headers) as response:
                response.raise_for_status()

                response_json = await response.json()
                if "state" not in response_json:
                    raise ValueError("Response JSON does not contain 'state', checking status is impossible.")

                new_state = response_json["state"]
                task.state = new_state
                if new_state == "completed":
                    if response_json["result"]["final"] is not None:
                        task.url = response_json["result"]["final"]
                        task.completed = True
                        logger.info(f"Task {task.id} completed successfully: {task.url}")
                    else:
                        logger.warning("Task was marked as completed, but no image URL could be found.")
                return task


    except aiohttp.ClientResponseError as e:
        logger.error(f"HTTP error occurred during the start_task request: {e.status} {e.message}")
        raise
    except aiohttp.ClientError as e:
        logger.error(f"Client error occurred during the start_task request: {e}")
        raise
    except ValueError as e:
        logger.error(f"Unknown ValueError: {e}")
        raise
    except Exception as e:
        logger.error(f"An Unknown error occurred during the start_task request: {e}")
        raise