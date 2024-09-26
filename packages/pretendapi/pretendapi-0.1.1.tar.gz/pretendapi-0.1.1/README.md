```markdown
# PretendAPI

PretendAPI is an asynchronous wrapper for the Pretend API, designed to simplify 
the process of fetching user information from the official Pretend API.

## Features

- Asynchronous requests using `aiohttp`
- Dot notation access to JSON responses
- Rate limiting support
- Handles exceptions gracefully

## Installation

You can install the package via pip:

```bash
pip install pretend-api
```

## Methods

### `get_userinfo(user_id: int)`
Fetches user information about a Discord user.

- **Parameters**: 
  - `user_id` (int): The user ID of the user.
- **Returns**: User information with dot notation access.

### `get_tiktok_user(username: str)`
Fetches information about a TikTok user.

- **Parameters**: 
  - `username` (str): The TikTok username.
- **Returns**: TikTok user information with dot notation access.

### `get_instagram_user(username: str)`
Fetches information about an Instagram user.

- **Parameters**: 
  - `username` (str): The Instagram username.
- **Returns**: Instagram user information with dot notation access.

### `get_twitter_user(username: str)`
Fetches information about a Twitter user.

- **Parameters**: 
  - `username` (str): The Twitter username.
- **Returns**: Twitter user information with dot notation access.

### `get_roblox_user(username: str)`
Fetches information about a Roblox user.

- **Parameters**: 
  - `username` (str): The Roblox username.
- **Returns**: Roblox user information with dot notation access.

### `get_signed_biolink(username: str)`
Fetches information about a signed.bio user.

- **Parameters**: 
  - `username` (str): The signed.bio username.
- **Returns**: signed.bio user information with dot notation access.

## Usage

Here's a basic example of how to use the `PretendAPI`:

```python
import asyncio
from pretend_api import PretendAPI

async def main():
    api_wrapper = PretendAPI(api_key="YOUR_API_KEY")
    
    
    user_info = await api_wrapper.get_userinfo(user_id=123456789)
    
    
    print(user_info.username)  

asyncio.run(main())
```



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```