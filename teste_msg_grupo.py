from telethon import TelegramClient

api_id = 30577430
api_hash = 'f67713bb5d0695b0df1ddde9fce061f2'

client = TelegramClient('session', api_id, api_hash)

DESTINO = -1003738269404

async def main():
    await client.send_message(DESTINO, "🚀 teste bot entrada")

with client:
    client.loop.run_until_complete(main())