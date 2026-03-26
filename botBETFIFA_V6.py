import re
import requests
import os
import json
import schedule
import time
import threading
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
# 📁 FUNÇÕES JSON (ORIGINAIS)
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
# 📁 FUNÇÕES JSON (NOVAS)
# =========================
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# =========================
# 📊 STATS
# =========================
def get_stats():
    stats = load_json("stats.json")
    if not stats:
        stats = {
            "entradas": 0,
            "greens": 0,
            "reds": 0,
            "push": 0,
            "sequencia": 0,
            "tipo_seq": ""
        }
    return stats

def save_stats(stats):
    save_json("stats.json", stats)

# =========================
# 📊 ATUALIZAR STATS
# =========================
def extrair_resultado(texto):
    if "🔄" in texto or "Refund" in texto:
        return "🔄"
    elif "Green" in texto or "✅" in texto:
        return "✅"
    elif "Red" in texto or "❌" in texto:
        return "❌"
    return None

def atualizar_stats(resultado):
    stats = get_stats()

    stats["entradas"] += 1

    if resultado == "✅":
        stats["greens"] += 1
        if stats["tipo_seq"] == "green":
            stats["sequencia"] += 1
        else:
            stats["sequencia"] = 1
            stats["tipo_seq"] = "green"

    elif resultado == "❌":
        stats["reds"] += 1
        if stats["tipo_seq"] == "red":
            stats["sequencia"] += 1
        else:
            stats["sequencia"] = 1
            stats["tipo_seq"] = "red"

    elif resultado == "🔄":
        stats["push"] += 1

    save_stats(stats)

# =========================
# 📊 GERAR PAINEL
# =========================
def gerar_painel():
    stats = get_stats()

    total = stats["entradas"]
    greens = stats["greens"]
    reds = stats["reds"]
    push = stats["push"]

    taxa = (greens / total * 100) if total > 0 else 0
    seq = f'{stats["sequencia"]} {stats["tipo_seq"].upper()}' if stats["tipo_seq"] else "0"

    return f"""📊 <b>PAINEL AO VIVO BETFIFA</b>

📈 Entradas: {total}
✅ Greens: {greens}
❌ Reds: {reds}
🔄 Push: {push}

📊 Assertividade: <b>{taxa:.1f}%</b>
🔥 Sequência: <b>{seq}</b>
"""

# =========================
# 📌 PAINEL FIXO
# =========================
def get_painel_id():
    return load_json("painel.json")

def salvar_painel_id(data):
    save_json("painel.json", data)

def atualizar_painel():
    painel = get_painel_id()
    texto = gerar_painel()

    if not painel.get("message_id"):
        r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
            "chat_id": DESTINO,
            "text": texto,
            "parse_mode": "HTML",
            "reply_markup": get_botoes()
        }).json()

        salvar_painel_id({"message_id": r["result"]["message_id"]})
    else:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", json={
            "chat_id": DESTINO,
            "message_id": painel["message_id"],
            "text": texto,
            "parse_mode": "HTML",
            "reply_markup": get_botoes()
        })

# =========================
# 🧾 RESUMO
# =========================
def enviar_resumo():
    texto = gerar_painel().replace("PAINEL AO VIVO", "RESUMO DO DIA")

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
        "chat_id": DESTINO,
        "text": texto,
        "parse_mode": "HTML",
        "reply_markup": get_botoes()
    })

def reset_stats():
    save_stats({
        "entradas": 0,
        "greens": 0,
        "reds": 0,
        "push": 0,
        "sequencia": 0,
        "tipo_seq": ""
    })

# =========================
# ⏰ AGENDAMENTO
# =========================
def scheduler():
    schedule.every().day.at("18:00").do(enviar_resumo)
    schedule.every().day.at("23:59").do(lambda: [enviar_resumo(), reset_stats()])

    while True:
        schedule.run_pending()
        time.sleep(30)

threading.Thread(target=scheduler).start()

# =========================
# 🧠 MONTA MENSAGEM (ORIGINAL)
# =========================
def montar_msg(texto, origem):
    jogo = ""
    mercado = ""
    resultado = ""

    if origem == BOT_1:
        if "Gols 1º Tempo" not in texto:
            return None
        jogo_match = re.search(r'🏃‍(.+)', texto)
        jogo = jogo_match.group(1).strip() if jogo_match else ""
        mercado_match = re.search(r'📈(.+)', texto)
        mercado = mercado_match.group(1).split('@')[0].strip() if mercado_match else ""

    elif origem == BOT_2:
        if "Gols no 1º tempo" not in texto:
            return None
        jogo_match = re.search(r': (.+)', texto)
        jogo = jogo_match.group(1).strip() if jogo_match else ""
        mercado_match = re.search(r'📈 (.+?)@', texto)
        mercado = mercado_match.group(1).strip() if mercado_match else ""

    elif origem == BOT_3:
        if "Gols" not in texto:
            return None
        jogo_match = re.search(r'(.+vs.+)', texto)
        jogo = jogo_match.group(1).strip() if jogo_match else "Jogo não identificado"
        mercado_match = re.search(r'(Gols.+)', texto)
        mercado = mercado_match.group(1).strip() if mercado_match else "Mercado"

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
# 🔘 BOTÕES
# =========================
def get_botoes():
    return {
        "inline_keyboard": [
            [{"text": "📲 Instagram", "url": "https://instagram.com/seuusuario"},
             {"text": "📲 Twitter", "url": "https://twitter.com/seuusuario"}],
            [{"text": "💰 Acesse o VIP", "url": "https://t.me/seugrupovip"}]
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

        r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
            "chat_id": DESTINO,
            "text": msg,
            "parse_mode": "HTML",
            "reply_markup": get_botoes()
        }).json()

        msg_id = r["result"]["message_id"]
        chave = f"{event.chat_id}_{event.id}"
        mensagens[chave] = msg_id
        salvar_mensagens(mensagens)

    except Exception as e:
        print("❌ Erro NEW:", e)

# =========================
# ✏️ EDITADO (COM PAINEL)
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

        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", json={
            "chat_id": DESTINO,
            "message_id": msg_id,
            "text": msg,
            "parse_mode": "HTML",
            "reply_markup": get_botoes()
        })

        # 🔥 ATUALIZA PAINEL
        resultado = extrair_resultado(texto)
        if resultado:
            atualizar_stats(resultado)
            atualizar_painel()

    except Exception as e:
        print("❌ Erro EDIT:", e)

# 🚀 START
client.start()
print("🤖 Bot completo com painel + resumo automático ativo...")
client.run_until_disconnected()