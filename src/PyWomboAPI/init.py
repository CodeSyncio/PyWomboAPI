from typing import List, Tuple, Optional

import requests as r
import re
from .statics import Headers
import json
from lxml import html
from .models import Credentials
import logging

logger = logging.getLogger(__name__)
class CreatePage:
    def __init__(self):
        self.create_page = None

    def fetch(self):
        if self.create_page is None:
            try:
                self.create_page = r.get("https://dream.ai/create")
                self.create_page.raise_for_status()
            except r.RequestException as e:
                logger.error(f"An error occurred when trying to fetch https://dream.ai/create: {e}")
                self.create_page = None
        return self.create_page

CREATE_PAGE= CreatePage()


def _get_api_key() -> str:
    """Fetches the API key from the create page on the Dream AI site."""
    try:
        create_page = CREATE_PAGE.fetch()

        js_paths = re.findall(r'/_next/static/chunks/pages/_app-\S*\.js', create_page.text)

        if not js_paths:
            logger.error("Could not find the JS file path on https://dream.ai/create.")
            raise ValueError("No matching JS path found.")

        js_path = js_paths[0]

        js_file_url = f"https://dream.ai{js_path}"
        js_file = r.get(js_file_url)
        js_file.raise_for_status()

        api_keys = re.findall(r'Ie={apiKey:"(.*?)",', js_file.text)

        if not api_keys:
            logger.error("Could not find the API key in the JS file at %s", js_file_url)
            raise ValueError("API key not found in JS file.")

        return api_keys[0]

    except r.RequestException as e:
        logger.error("Request failed: %s", e)
        raise
    except Exception as e:
        logger.error("An unexpected error occurred while trying to get the API key: %s", e)
        raise

def get_auth_token(api_key) -> str:
    """Request an auth token (bearer).
    TODO: add TTL"""
    try:
        auth_req = r.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}",
            headers=Headers.identity_headers)
        auth_req.raise_for_status()
        auth_json = auth_req.json()
        if "idToken" not in auth_json:
            raise ValueError("Response JSON does not contain 'idToken'.")

        return auth_json["idToken"]

    except r.RequestException as e:
        logger.error("Request failed: %s", e)
        raise
    except r.JSONDecodeError as e:
        logger.error("Failed to decode JSON data while trying to obtain a bearer token: %s", e)
        raise
    except Exception as e:
        logger.error("An unexpected error occurred while trying to obtain a bearer token", e)
        raise


def initialize(api_key=None,auth_token=None) -> Credentials:
    if api_key is not None:
        logger.warning("User provided their own key: %s", api_key)
    if auth_token is not None:
        logger.warning("User provided their own bearer, this may cause issues!")
    try:
        if api_key is None:
            logger.info("API key not set, fetching it automatically...")
            api_key = _get_api_key()
            if not api_key:
                raise ValueError("Failed to fetch the API key.")

        if auth_token is None:
            logger.info("Auth token not provided, Generating one...")
            auth_token = get_auth_token(api_key)
            if not auth_token:
                raise ValueError("Failed to generate a valid auth token.")

        credentials = Credentials(api_key, auth_token)

        logger.info(f"Credentials: {credentials}")

        return credentials

    except ValueError as e:
        logger.error("ValueError: %s", e)
        raise
    except Exception as e:
        logger.error("An unknown error occured while creating the credentials object: %s",e)


def fetch_styles(include_premium: bool = False, fetch_thumbnails: bool = False) -> List[Tuple[int, str, bool, Optional[str]]]:
    """Fetches styles from the create page and returns a list of styles."""
    try:
        create_page = CREATE_PAGE.fetch()
        create_page.raise_for_status()

        tree = html.fromstring(create_page.content)
        styles_script = tree.xpath('//script[@id="__NEXT_DATA__"]')

        if not styles_script:
            raise ValueError("Could not find the script with the ID '__NEXT_DATA__' in the HTML content.")

        _ = json.loads(styles_script[0].text)
        styles = []
        styles_json = _["props"]["pageProps"]["artStyles"]
        if not styles_json:
            raise ValueError("No 'artStyles' found in the JSON response.")

        for style in  styles_json:
            try:
                style_id = int(style.get("id", -1))
                name = str(style.get("name", "Unknown"))
                is_premium = bool(style.get("is_premium", False))

                if is_premium and not include_premium:
                    continue
                thumbnail_url = str(style.get("photo_url")) if fetch_thumbnails else None
                styles.append((style_id, name, is_premium, thumbnail_url))

            except (ValueError, TypeError) as e:
                logger.warning(f"Skipping style due to error: {e}")

        logger.info(f"Fetched {len(styles)} styles successfully.")
        return styles

    except r.RequestException as e:
        logger.error(f"Failed to fetch the create page: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from the styles script: {e}")
        raise
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise