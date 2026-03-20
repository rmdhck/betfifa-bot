from telethon import TelegramClient

api_id = 30577430
api_hash = 'f67713bb5d0695b0df1ddde9fce061f2'

client = TelegramClient('session', api_id, api_hash)

DESTINO = -1003738269404  # seu grupo

async def main():
    msgs = await client.get_messages(DESTINO, limit=1)

    for m in msgs:
        print("Última mensagem:")
        print(m.text)

with client:
    client.loop.run_until_complete(main())