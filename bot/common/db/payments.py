import datetime
from bot.common.db import db
from prisma.types import UserInclude

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

async def txn_link(user: str, link: str):
    try:
        await db.connect()
        await db.membership.update(
            where={
                'username': user,
                },
            data={
                'txnLink': link,
                }
            )
    finally:
        if db.is_connected():
            await db.disconnect()

async def cancel_link(user: str):
    try:
        await db.connect()
        await db.membership.update(
            where={
                'username': user,
                },
            data={
                'txnLink': None,
                }
            )
    finally:
        if db.is_connected():
            await db.disconnect()

async def get_txn_link(user: str) -> str:
    try:
        await db.connect()
        link = await db.membership.find_unique(
            where={
                'username': user,
                },
            )
        return link.txnLink
    finally:
        if db.is_connected():
            await db.disconnect()

async def check_txn_link(user: str) -> bool:
    """detect if the telegram user is an existing txn in the db"""
    try:
        await db.connect()
        membership = await db.membership.find_unique(
            where={
                'username': user,
                }
            )
        if membership.txnLink: return True
        return False
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
