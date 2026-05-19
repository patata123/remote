import asyncio
import csv
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import User, Channel, Chat

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")


def format_sender(sender) -> str:
    if sender is None:
        return "Unknown"
    if isinstance(sender, User):
        name = " ".join(filter(None, [sender.first_name, sender.last_name]))
        return name or sender.username or str(sender.id)
    if isinstance(sender, (Channel, Chat)):
        return sender.title or str(sender.id)
    return str(sender.id)


async def list_chats(client: TelegramClient):
    print("\nYour chats:")
    print(f"{'#':<4} {'Type':<10} {'Name'}")
    print("-" * 50)
    dialogs = await client.get_dialogs()
    for i, dialog in enumerate(dialogs):
        chat_type = type(dialog.entity).__name__
        print(f"{i:<4} {chat_type:<10} {dialog.name}")
    return dialogs


async def extract_messages(client: TelegramClient, chat, limit: int, output_file: str):
    print(f"\nExtracting up to {limit} messages...")
    rows = []
    async for message in client.iter_messages(chat, limit=limit):
        if not message.text:
            continue
        sender = await message.get_sender()
        rows.append({
            "message_id": message.id,
            "date": message.date.strftime("%Y-%m-%d %H:%M:%S"),
            "sender_id": sender.id if sender else "",
            "sender_name": format_sender(sender),
            "text": message.text,
            "reply_to_msg_id": message.reply_to_msg_id or "",
        })

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} messages to '{output_file}'")


async def main():
    if not all([API_ID, API_HASH, PHONE]):
        print("Error: set API_ID, API_HASH, and PHONE in a .env file (see .env.example)")
        sys.exit(1)

    client = TelegramClient("session", int(API_ID), API_HASH)
    await client.start(phone=PHONE)

    dialogs = await list_chats(client)

    print("\nEnter the chat number from the list above:")
    try:
        choice = int(input("> ").strip())
        chat = dialogs[choice].entity
    except (ValueError, IndexError):
        print("Invalid choice.")
        await client.disconnect()
        return

    print("How many messages to extract? (default: 100)")
    raw = input("> ").strip()
    limit = int(raw) if raw.isdigit() else 100

    chat_name = getattr(chat, "title", None) or getattr(chat, "first_name", "chat")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in chat_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{safe_name}_{timestamp}.csv"

    await extract_messages(client, chat, limit, output_file)
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
