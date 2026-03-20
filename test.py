from telethon import TelegramClient

api_id = 30577430
api_hash = 'SEU_API_HASHf67713bb5d0695b0df1ddde9fce061f2'

client = TelegramClient('session', api_id, api_hash)

async def main():
    await client.send_message("me", "teste funcionando 🚀")

with client:
    client.loop.run_until_complete(main())