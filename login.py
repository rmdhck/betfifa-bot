from telethon import TelegramClient

api_id = 30577430
api_hash = 'f67713bb5d0695b0df1ddde9fce061f2'

client = TelegramClient('session', api_id, api_hash)

client.start(phone='+5511952979975')

print("Logado com sucesso!")

client.run_until_disconnected()