import re
import requests
import os
from telethon import TelegramClient, events

# 🔑 SUAS CREDENCIAIS
api_id = 30577430
api_hash = 'f67713bb5d0695b0df1ddde9fce061f2'

# 🤖 BOT TOKEN (Railway depois)
BOT_TOKEN = os.getenv("BOT_TOKEN")

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

        jogo = ""
        mercado = ""
        resultado = ""

        # =========================
        # BOT 1
        # =========================
        if event.chat_id == BOT_1:

            if "Gols 1º Tempo" not in texto:
                return

            # 🎮 JOGO
            jogo_match = re.search(r'🏃‍(.+)', texto)
            jogo = jogo_match.group(1).strip() if jogo_match else ""

            # 📈 MERCADO
            mercado_match = re.search(r'📈(.+)', texto)
            mercado = mercado_match.group(1).split('@')[0].strip() if mercado_match else ""

            # 🏆 RESULTADO
            if "Green" in texto or "✅" in texto:
                resultado = "✅"
            elif "Red" in texto or "❌" in texto:
                resultado = "❌"
            elif "Refund" in texto:
                resultado = "⚪️"

        # =========================
        # CANAL (CAVEIRA TIPS)
        # =========================
        elif event.chat_id == BOT_2:

            if "Gols no 1º tempo" not in texto:
                return

            # 🎮 JOGO
            jogo_match = re.search(r': (.+)', texto)
            jogo = jogo_match.group(1).strip() if jogo_match else ""

            # 📈 MERCADO
            mercado_match = re.search(r'📈 (.+?)@', texto)
            mercado = mercado_match.group(1).strip() if mercado_match else ""

            # 🏆 RESULTADO
            if "Green" in texto:
                resultado = "✅"
            elif "Red" in texto:
                resultado = "❌"
            elif "Refund" in texto:
                resultado = "⚪️"

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

        # =========================
        # 📤 ENVIO VIA BOT (OFICIAL)
        # =========================
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": DESTINO,
            "text": msg
        }

        requests.post(url, data=data)

        print("✅ Enviado pelo BOT:")
        print(msg)
        print("-" * 40)

    except Exception as e:
        print("❌ Erro:", e)


# 🚀 START
client.start()
print("🤖 Bot rodando 24h...")
client.run_until_disconnected()