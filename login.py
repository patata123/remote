import asyncio
import os
import sys

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")


async def main():
    code = sys.argv[1] if len(sys.argv) > 1 else None
    client = TelegramClient("session", API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        if code is None:
            await client.send_code_request(PHONE)
            print("CODE_SENT")
        else:
            await client.sign_in(PHONE, code)
            me = await client.get_me()
            print(f"Logged in as: {me.first_name} (@{me.username})")
    else:
        me = await client.get_me()
        print(f"Already logged in as: {me.first_name} (@{me.username})")

    await client.disconnect()


asyncio.run(main())
