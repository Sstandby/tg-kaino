import jwt
from bot.common.db import db

async def register(binance: str, username: str, password: str, update: bool) -> bool:
    """Register binance token with its respective password"""
    try:
        binance = jwt.encode({"token": binance}, password, algorithm="HS256")
        await db.connect()
        if get_user_info(username):
            if update:
                await db.user.create(
                    data={
                        'binance_token': binance,
                        'username': username,
                        },
                    )
            else:
                await db.user.update(
                    where={
                        'username': username,
                        },
                    data={
                        'binance_token': binance,
                        'username': username,
                        }
                    )
            return True
        return False

    finally:
        if db.is_connected():
            await db.disconnect()

async def get_user_info(user: str) -> bool:
    """search for existing user token"""
    user = await db.user.find_unique(
            where={
                'username': user,
                }
            )
    if user: return True
    return False
