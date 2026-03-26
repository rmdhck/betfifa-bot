import re
import requests
import os
import json
from telethon import TelegramClient, events

# 🔑 CREDENCIAIS TELEGRAM
api_id = 30577430
api_hash = 'f67713bb5d0695b0df1ddde9fce061f2'

# 🤖 TOKEN DO BOT
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 📌 ORIGENS
BOT_1 = 8101031409
BOT_2 = -1001676567497
BOT_3 = -5081763711

# 📤 DESTINO
DESTINO = -1003738269404

# 📁 ARQUIVO JSON
ARQUIVO_JSON = "mensagens.json"

client = TelegramClient('session', api_id, api_hash)


# =========================
# 📁 FUNÇÕES JSON
# =========================
def carregar_mensagens():
    try:
        with open(ARQUIVO_JSON, "r") as f:
            return json.load(f)
    except:
        return {}


def salvar_mensagens(data):
    with open(ARQUIVO_JSON, "w") as f:
        json.dump(data, f)


mensagens = carregar_mensagens()


# =========================
# 🧠 MONTA MENSAGEM PADRÃO
# =========================
def montar_msg(texto, origem):
    jogo = ""
    mercado = ""
    resultado = ""

    # BOT 1
    if origem == BOT_1:

        if "Gols 1º Tempo" not in texto:
            return None

        jogo_match = re.search(r'🏃‍(.+)', texto)
        jogo = jogo_match.group(1).strip() if jogo_match else ""

        mercado_match = re.search(r'📈(.+)', texto)
        mercado = mercado_match.group(1).split('@')[0].strip() if mercado_match else ""

    # BOT 2
    elif origem == BOT_2:

        if "Gols no 1º tempo" not in texto:
            return None

        jogo_match = re.search(r': (.+)', texto)
        jogo = jogo_match.group(1).strip() if jogo_match else ""

        mercado_match = re.search(r'📈 (.+?)@', texto)
        mercado = mercado_match.group(1).strip() if mercado_match else ""

    # BOT 3
    elif origem == BOT_3:

        if "Gols" not in texto:
            return None

        jogo_match = re.search(r'(.+vs.+)', texto)
        jogo = jogo_match.group(1).strip() if jogo_match else "Jogo não identificado"

        mercado_match = re.search(r'(Gols.+)', texto)
        mercado = mercado_match.group(1).strip() if mercado_match else "Mercado"

    # RESULTADO
    if "🔄" in texto or "Refund" in texto:
        resultado = "🔄"
    elif "Green" in texto or "✅" in texto:
        resultado = "✅"
    elif "Red" in texto or "❌" in texto:
        resultado = "❌"

    return f"""🏃🏽‍♂️‍➡️⚽️ <b>ENTRADA BETFIFA</b> ⚽️
🎮 <b>{jogo}</b>
📈 <i>{mercado}</i>
🏆 RESULTADO: {resultado}
"""


# =========================
# 🔘 BOTÕES INLINE
# =========================
def get_botoes():
    return {
        "inline_keyboard": [
            [
                {
                    "text": "📲 Siga no Instagram",
                    "url": "https://instagram.com/seuusuario"
                }
            ],
            [
                {
                    "text": "Quer mais? 💰 Acesse nosso grupo VIP",
                    "url": "https://t.me/seugrupovip"
                }
            ]
        ]
    }


# =========================
# 🆕 NOVA MENSAGEM
# =========================
@client.on(events.NewMessage)
async def new_msg(event):
    try:
        if event.chat_id not in [BOT_1, BOT_2, BOT_3]:
            return

        texto = event.raw_text
        msg = montar_msg(texto, event.chat_id)

        if not msg:
            return

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        r = requests.post(url, json={
            "chat_id": DESTINO,
            "text": msg,
            "parse_mode": "HTML",
            "reply_markup": get_botoes()
        }).json()

        msg_id = r["result"]["message_id"]

        chave = f"{event.chat_id}_{event.id}"
        mensagens[chave] = msg_id
        salvar_mensagens(mensagens)

        print("✅ Nova enviada")
        print(msg)
        print("-" * 40)

    except Exception as e:
        print("❌ Erro NEW:", e)


# =========================
# ✏️ MENSAGEM EDITADA
# =========================
@client.on(events.MessageEdited)
async def edit_msg(event):
    try:
        if event.chat_id not in [BOT_1, BOT_2, BOT_3]:
            return

        chave = f"{event.chat_id}_{event.id}"

        if chave not in mensagens:
            return

        texto = event.raw_text
        msg = montar_msg(texto, event.chat_id)

        if not msg:
            return

        msg_id = mensagens[chave]

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"

        requests.post(url, json={
            "chat_id": DESTINO,
            "message_id": msg_id,
            "text": msg,
            "parse_mode": "HTML",
            "reply_markup": get_botoes()
        })

        print("✏️ Editado")
        print(msg)
        print("-" * 40)

    except Exception as e:
        print("❌ Erro EDIT:", e)


# 🚀 START
client.start()
print("🤖 Bot rodando com JSON + edição + botões...")
client.run_until_disconnected()