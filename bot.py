import re
from telethon import TelegramClient, events

api_id = 30577430
api_hash = 'f67713bb5d0695b0df1ddde9fce061f2'

client = TelegramClient('session', api_id, api_hash)

BOT_1 = 8101031409  # green365
BOT_2 = -1001676567497  # segundo bot

DESTINO = -5112774547  # seu grupo

@client.on(events.NewMessage)
async def handler(event):
    texto = event.raw_text

    # =========================
    # 🔥 BOT 1 (green365)
    # =========================
    if event.chat_id == BOT_1:

        if "Gols 1º Tempo" not in texto:
            return

        try:
            jogo = re.search(r'🏃‍(.+)', texto)
            jogo = jogo.group(1) if jogo else ""

            mercado = re.search(r'📈(.+)', texto)
            mercado = mercado.group(1).split('@')[0].strip()

            resultado = "✅" if "✅" in texto else "❌" if "❌" in texto else ""

            msg = f"""Entrada BETFIFA ⚽️⚽️⚽️
🎮 {jogo}
📈 {mercado}
🏆 Resultado tip {resultado}
"""

            await client.send_message(DESTINO, msg)

        except Exception as e:
            print("Erro BOT 1:", e)

    # =========================
    # 🔥 BOT 2 (novo padrão)
    # =========================
    elif event.chat_id == BOT_2:

        try:
            # 🎮 JOGO (linha principal)
            jogo = re.search(r': (.+)', texto)
            jogo = jogo.group(1) if jogo else ""

            # 📈 MERCADO
            mercado = re.search(r'📈 (.+?)@', texto)
            mercado = mercado.group(1).strip() if mercado else ""

            # 🏆 RESULTADO
            if "Green" in texto or "WIN" in texto:
                resultado = "✅"
            elif "Red" in texto or "LOSS" in texto:
                resultado = "❌"
            elif "Refund" in texto:
                resultado = "⚪️"
            else:
                resultado = ""

            msg = f"""Entrada BETFIFA ⚽️⚽️⚽️
🎮 {jogo}
📈 {mercado}
🏆 Resultado tip {resultado}
"""

            await client.send_message(DESTINO, msg)

        except Exception as e:
            print("Erro BOT 2:", e)


client.start()
print("Rodando multi-bot...")
client.run_until_disconnected()