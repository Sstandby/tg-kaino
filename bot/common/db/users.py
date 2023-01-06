import datetime
import jwt
import json
from bot import kaino_pass
from bot.common.db import db
from prisma.types import UserInclude

async def register_wallet(binance: str, secret: str, username: str, password: str, update: bool) -> bool:
    """Register user with its respective password"""
    try:
        api_key = jwt.encode({"token": binance}, password, algorithm="HS256")
        api_secret = jwt.encode({"secret": secret}, password, algorithm="HS256")
        password = jwt.encode({"password": password}, kaino_pass, algorithm="HS256")
        wallet = await get_wallet_info(username)
        user  = await existing_user(username)
        if update == False:
            if wallet.binance_token != None: return False
            await db.connect()
            await db.wallet.update(
                where={
                    'username': username,
                    },
                data={
                    'binance_token': api_key,
                    'binance_secret': api_secret,
                    'password': password,
                    },
                )
            return True
        else:
            if user:
                await db.connect()
                await db.user.update(
                        where={
                            'username': username,
                            },
                        data={
                            'binance_token': binance,
                            'username': username,
                            'password': password,
                            }
                        )
                return True
            return False
    finally:
        if db.is_connected():
            await db.disconnect()

async def register_deriv(api_access: str, username: str, password: str, update: bool) -> bool:
    """Register deriv """
    try:
        # apiDeriv = jwt.encode({"api": apiDeriv}, kaino_pass, algorithm="HS256")
        api = jwt.encode({"token": api_access}, kaino_pass, algorithm="HS256")
        password = jwt.encode({"password": password}, kaino_pass, algorithm="HS256")
        user = await existing_user(username)
        wallet = await get_wallet_info(username)
        if update == False:
            if wallet.id_access != None: return False
            await db.connect()
            await db.wallet.update(
                    where={
                        'username': username,
                        },
                    data={
                        'id_access': api  ,
                        'encrypted_pass': password,
                        # 'deriv_api': apiDeriv,
                        }
                )
            return True
        else:
            if user:
                await db.connect()
                await db.wallet.update(
                        where={
                            'username': username,
                            },
                        data={
                            'id_access': api,
                            'encrypted_pass': password,
                            'deriv_api': apiDeriv,
                            }
                        )
                return True
            return False
    finally:
        if db.is_connected():
            await db.disconnect()


async def register_user(fullname: str, country: str, phone: str, email: str, username: str, update: bool) -> bool:
    """Registering user for kaino"""
    try:
        user = await existing_user(username)
        if update == False:
            if user: return False
            await db.connect()
            await db.user.create(
                data={
                    'fullname': fullname,
                    'country': country,
                    'username': username,
                    'phone': phone,
                    'email': email,
                    },
                )
            await db.wallet.create(
                data = {
                    'username': username,
                    },
                )
            await db.membership.create(
                data = {
                    'username': username,
                    },
                )
            return True
        else:
            if user:
                await db.connect()
                await db.user.update(
                        where={
                            'username': username,
                            },
                        data={
                            'fullname': fullname,
                            'country': country,
                            'phone': phone,
                            'email': email,
                            }
                        )
                return True
            return False
    finally:
        if db.is_connected():
            await db.disconnect()

async def get_user_info(username: str):
    """provide all user information"""
    try:
        await db.connect()
        user = await db.user.find_unique(
            where={
                'username': username,
                },
            )
        return user
    finally:
        if db.is_connected():
            await db.disconnect()

async def get_wallet_info(username: str):
    """provide all wallet information"""
    try:
        await db.connect()
        user = await db.wallet.find_unique(
            where={
                'username': username,
                },
            )
        return user
    finally:
        if db.is_connected():
            await db.disconnect()

async def get_membership_info(username: str):
    """provide all membership information"""
    try:
        await db.connect()
        user = await db.membership.find_unique(
            where={
                'username': username,
                },
            )
        return user
    finally:
        if db.is_connected():
            await db.disconnect()

async def get_api_key(username: str):
    """extract and decompile api key from db"""
    try:
        user = await get_user_info(username)
        password = user.password
        binance_token = user.binance_token
        secret = jwt.decode(password, kaino_pass, algorithms=["HS256"])
        api_key = jwt.decode(binance_token, secret['password'], algorithms=["HS256"])
        return api_key['token']
    except Exception as es:
        pass

async def get_api_secret(username: str):
    """extract and decompile api secret from db"""
    try:
        user = await get_user_info(username)
        password = user.password
        binance_secret = user.binance_secret
        secret = jwt.decode(password, kaino_pass, algorithms=["HS256"])
        api_secret = jwt.decode(binance_secret, secret['password'], algorithms=["HS256"])
        return api_secret['secret']
    except Exception as es:
        pass

async def get_deriv_pass(username: str):
    """extract and decompile pass from db"""
    try:
        user = await get_wallet_info(username)
        password = user.encrypted_pass
        api_secret = jwt.decode(password, kaino_pass, algorithms=["HS256"])
        return api_secret['password']
    except Exception as es:
        pass

async def get_deriv_user(username: str):
    """extract and decompile id acces from db"""
    try:
        user = await get_wallet_info(username)
        access = user.id_access
        api_secret = jwt.decode(access, kaino_pass, algorithms=["HS256"])
        return api_secret['token']
    except Exception as es:
        pass

async def existing_user(user: str) -> bool:
    """detect if the telegram user is an existing user in the db"""
    try:
        await db.connect()
        user = await db.user.find_unique(
            where={
                'username': user,
                }
            )
        if user: return True
        return False
    finally:
        if db.is_connected():
            await db.disconnect()


async def membership(user: str) -> bool:
    """detect if membership is activated"""
    try:
        await db.connect()
        membership = await db.membership.find_unique(
            where={
                'username': user,
                }
            )
        if membership.active: return True
        return False
    finally:
        if db.is_connected():
            await db.disconnect()


async def membership_update(username: str, membership: bool) -> bool:
    try:
        await db.connect()
        user = await db.membership.update(
            where={
                'username': username,
                },
            data={
                'active': membership,
                'created_at': datetime.datetime.now()
                }
            )
        if user: return True
        return False
    finally:
        if db.is_connected():
            await db.disconnect()

async def identifiership_update(user: str, item: str) -> bool:
    try:
        await db.connect()
        user = await db.membership.update(
            where={
                'username': user,
                },
            data={
                'identifiership': item,
                }
            )
        if user: return True
        return False
    finally:
        if db.is_connected():
            await db.disconnect()
