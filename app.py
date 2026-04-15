from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

# ------------------ DADOS ------------------

def carregar_dados():
    with open("dados.json", "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open("dados.json", "w") as f:
        json.dump(dados, f, indent=4)

# ------------------ FUNÇÕES ------------------

def menu():
    return (
        "👋 Fala Renan!\n\n"
        "Escolha uma opção:\n"
        "1 - Financeiro 💰\n"
        "2 - Notícias 📰\n"
        "3 - Combustível ⛽"
    )

def tratar_financeiro(msg, dados):
    if "entrada" in msg:
        valor = float(msg.split(" ")[1])
        dados["saldo"] += valor
        dados["transacoes"].append({"tipo": "entrada", "valor": valor})

        salvar_dados(dados)
        return f"💰 Entrada: R${valor}\nSaldo: R${dados['saldo']}"

    elif "saida" in msg:
        valor = float(msg.split(" ")[1])
        dados["saldo"] -= valor
        dados["transacoes"].append({"tipo": "saida", "valor": valor})

        salvar_dados(dados)
        return f"💸 Saída: R${valor}\nSaldo: R${dados['saldo']}"

    elif msg == "saldo":
        return f"📊 Saldo atual: R${dados['saldo']}"

def tratar_combustivel(msg):
    try:
        partes = msg.split(" ")
        gasolina = float(partes[1])
        alcool = float(partes[2])

        relacao = alcool / gasolina

        if relacao < 0.7:
            resultado = "✅ Álcool compensa mais!"
        else:
            resultado = "⛽ Gasolina compensa mais!"

        return (
            f"📊 Combustível:\n"
            f"Gasolina: R${gasolina}\n"
            f"Álcool: R${alcool}\n"
            f"Proporção: {relacao:.2f}\n"
            f"{resultado}"
        )

    except:
        return "Use: combustivel 5.59 3.89"

# ------------------ ROTA ------------------

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body", "").lower()
    response = MessagingResponse()
    reply = response.message()

    dados = carregar_dados()

    if msg == "oi":
        resposta = menu()

    elif "entrada" in msg or "saida" in msg or msg == "saldo":
        resposta = tratar_financeiro(msg, dados)

    elif "combustivel" in msg:
        resposta = tratar_combustivel(msg)

    else:
        resposta = (
            "Comandos:\n"
            "- entrada 100\n"
            "- saida 50\n"
            "- saldo\n"
            "- combustivel 5.59 3.89"
        )

    reply.body(resposta)
    return str(response)

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(port=5000, debug=True)
