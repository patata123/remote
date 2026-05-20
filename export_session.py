"""
Run this LOCALLY once to generate a SESSION_STRING for cloud use.
Copy the printed string into your cloud environment's SESSION_STRING env var.
"""
import asyncio
import os
import sys

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")


async def main():
    if not all([API_ID, API_HASH, PHONE]):
        print("Error: set API_ID, API_HASH, and PHONE in .env first")
        sys.exit(1)

    client = TelegramClient(StringSession(), int(API_ID), API_HASH)
    await client.start(phone=PHONE)

    session_string = client.session.save()
    print("\n--- SESSION_STRING (add this to your cloud env vars) ---")
    print(session_string)
    print("--------------------------------------------------------\n")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
