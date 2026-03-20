import re
from telethon import TelegramClient, events

# 🔑 SUAS CREDENCIAIS
api_id = 30577430
api_hash = 'f67713bb5d0695b0df1ddde9fce061f2'

# 📌 ORIGENS
BOT_1 = 8101031409  # ID do primeiro bot
BOT_2 = -1001676567497  # Canal Caveira Tips

# 📤 DESTINO (SEU GRUPO)
DESTINO = -1003738269404

client = TelegramClient('session', api_id, api_hash)


@client.on(events.NewMessage)
async def handler(event):
    try:
        texto = event.raw_text

        # =========================
        # BOT 1
        # =========================
        if event.chat_id == BOT_1:

            if "Gols 1º Tempo" not in texto:
                return

            # 🎮 JOGO
            jogo = re.search(r'🏃‍(.+)', texto)
            jogo = jogo.group(1) if jogo else ""

            # 📈 MERCADO
            mercado = re.search(r'📈(.+)', texto)
            mercado = mercado.group(1).split('@')[0].strip() if mercado else ""

            # 🏆 RESULTADO
            if "Green" in texto or "✅" in texto:
                resultado = "✅"
            elif "Red" in texto or "❌" in texto:
                resultado = "❌"
            elif "Refund" in texto:
                resultado = "⚪️"
            else:
                resultado = ""

        # =========================
        # CANAL (CAVEIRA TIPS)
        # =========================
        elif event.chat_id == BOT_2:

            if "Gols no 1º tempo" not in texto:
                return

            # 🎮 JOGO
            jogo = re.search(r': (.+)', texto)
            jogo = jogo.group(1) if jogo else ""

            # 📈 MERCADO
            mercado = re.search(r'📈 (.+?)@', texto)
            mercado = mercado.group(1).strip() if mercado else ""

            # 🏆 RESULTADO
            if "Green" in texto:
                resultado = "✅"
            elif "Red" in texto:
                resultado = "❌"
            elif "Refund" in texto:
                resultado = "⚪️"
            else:
                resultado = ""

        else:
            return

        # =========================
        # 🧾 MENSAGEM FINAL
        # =========================
        msg = f"""Entrada BETFIFA ⚽️⚽️⚽️
🎮 {jogo}
📈 {mercado}
🏆 Resultado tip {resultado}
"""

        # 📤 ENVIO PARA GRUPO
        await client.send_message(DESTINO, msg)

        print("✅ Enviado:")
        print(msg)
        print("-" * 40)

    except Exception as e:
        print("❌ Erro:", e)


# 🚀 START
client.start()
print("🤖 Bot rodando 24h...")
client.run_until_disconnected()