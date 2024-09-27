import aiohttp
import asyncio
import logging
import time
from functools import wraps
from quart import Quart, jsonify, request
from quart_cors import cors

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DISCORD_API_URL = "https://discord.com/api/v10"
MAX_RETRIES = 5
RETRY_BACKOFF = 2  # seconds

def get_discord_headers(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }

async def request_with_retries(url, headers, max_retries=MAX_RETRIES, retry_backoff=RETRY_BACKOFF):
    for attempt in range(max_retries):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:  # Rate limited
                    retry_after = int(response.headers.get('Retry-After', retry_backoff))
                    logger.warning(f"Rate limited. Retrying after {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    logger.error(f"Request failed: {response.status} {await response.text()}")
                    break
    return None

async def get_user_guilds(token: str):
    url = f"{DISCORD_API_URL}/users/@me/guilds"
    headers = get_discord_headers(token)
    response = await request_with_retries(url, headers)
    return response

def has_manage_server_or_admin(permissions: int):
    MANAGE_SERVER = 0x20
    ADMINISTRATOR = 0x8
    return (permissions & MANAGE_SERVER) == MANAGE_SERVER or (permissions & ADMINISTRATOR) == ADMINISTRATOR

async def verify_token(token: str, guild_id: int):
    guilds = await get_user_guilds(token)
    if not guilds:
        logger.warning("Failed to fetch user guilds")
        return None
    
    guild = next((g for g in guilds if g['id'] == str(guild_id)), None)
    if not guild:
        logger.warning("Guild not found")
        return None
    
    if 'permissions' in guild:
        permissions = int(guild['permissions'])
        if has_manage_server_or_admin(permissions):
            logger.info(f"User has the necessary permissions for guild {guild_id}")
            return guild
    logger.warning(f"User does not have the necessary permissions for guild {guild_id}")
    return None

def require_permissions(func):
    @wraps(func)
    async def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.warning("Authorization header is missing")
            return jsonify({'error': 'Authorization header is missing'}), 401
        
        token = auth_header.split(' ')[1]
        guild_id = kwargs.get('guild_id')
        if not guild_id:
            logger.warning("guild_id parameter is missing")
            return jsonify({'error': 'guild_id parameter is missing'}), 400

        user_info = await verify_token(token, int(guild_id))
        if not user_info:
            return jsonify({'error': 'Invalid token or insufficient permissions'}), 403
        
        request.user_info = user_info
        return await func(*args, **kwargs)
    return decorated_function
