from telethon import TelegramClient

api_id = 12345678
api_hash = 'SEU_API_HASH'

client = TelegramClient('session', api_id, api_hash)

async def main():
    msgs = await client.get_messages(-1001676567497, limit=1)
    for m in msgs:
        print(m.text)

with client:
    client.loop.run_until_complete(main())