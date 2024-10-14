

![PyWomboAPI](WomboLogo.svg) <!-- Replace with your actual image path -->
# PyWomboAPI
**PyWomboAPI** is an unofficial Python library designed to generate images from Wombo's [dream.ai](https://dream.ai/). This library aims to make generating images easy and fast. 

***Please remember that this is a personal project I started to learn new things, so expect bugs!***

---

## Features

- **No API keys required**: The API can automatically generate authentication tokens.
- **Simple and Intuitive**: Easy methods for generating images.
- **Regular Updates**: I try to maintain and keep the code working efficiently.

---

## Installation

You can easily install **PyWomboAPI** via pip:

```bash
pip install PyWomboAPI
```

---

## Usage

Here’s a quick example of how to use **PyWomboAPI** to make a request to the Wombo AI API:

```python
import asyncio
import logging
from PyWomboAPI import WomboAPI

async def main() -> None:
    api = WomboAPI(log_level=logging.INFO)  # Set log level to INFO to see what's going on
    api.setup()  # Requesting all the necessary data
    image = await api.create_image(140, "flying car")  # Starting image generation
    print(image.url)

if __name__ == '__main__':
    asyncio.run(main())
```

This will generate an image:

```
2024-... - PyWomboAPI.init - INFO - API key not set, fetching it automatically...
2024-... - PyWomboAPI.init - INFO - Auth token not provided, generating one...
2024-... - PyWomboAPI.init - INFO - Credentials: Credentials(api_key='AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw', auth_token='...')
2024-... - PyWomboAPI.generation - INFO - Constructed POST data for start_task request: {'is_premium': False, 'input_spec': {'aspect_ratio': 'old_vertical_ratio', 'prompt': 'flying car', 'style': 140, 'display_freq': 10}}
2024-... - PyWomboAPI.generation - INFO - Received task data: {'id': '87e7cd9d-af3a-4e71-93ce-58b31b072fb9', ...}
2024-... - PyWomboAPI.generation - INFO - Task 87e7cd9d-af3a-4e71-93ce-58b31b072fb9 completed successfully: https://images.wombo.art/generated/.../final.jpg?Expires=...&Signature=...&Key-Pair-Id=...
```

*More examples can be found [here](/examples).*

---

## To-Do List

- [ ] **Add Support for Proxies**
- [ ] **Better Error Handling**
- [ ] **Improve Documentation**
- [ ] **Implement Tests**

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

