from flask import Flask, request, jsonify

app = Flask(__name__)

# armazenamento em memória
messages = []
current_id = 1


# ✅ Criar mensagem
@app.route("/api/messages", methods=["POST"])
def create_message():
    global current_id

    data = request.get_json(force=True)

    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    if not data.get("message") or not data.get("author"):
        return jsonify({"error": "Campos obrigatórios: message, author"}), 400

    new_message = {
        "id": current_id,
        "action": data.get("action", "create"),
        "message": data["message"],
        "author": data["author"]
    }

    messages.append(new_message)
    current_id += 1

    return jsonify(new_message), 201


# ✅ Listar todas
@app.route("/api/messages", methods=["GET"])
def get_messages():
    return jsonify(messages), 200


# ✅ Buscar por ID
@app.route("/api/messages/<int:msg_id>", methods=["GET"])
def get_message(msg_id):
    for msg in messages:
        if msg["id"] == msg_id:
            return jsonify(msg), 200

    return jsonify({"error": "Mensagem não encontrada"}), 404


# ✅ Atualizar
@app.route("/api/messages/<int:msg_id>", methods=["PUT"])
def update_message(msg_id):
    data = request.get_json(force=True)

    for msg in messages:
        if msg["id"] == msg_id:
            msg["message"] = data.get("message", msg["message"])
            msg["author"] = data.get("author", msg["author"])
            msg["action"] = data.get("action", msg["action"])

            return jsonify(msg), 200

    return jsonify({"error": "Mensagem não encontrada"}), 404


# ✅ Deletar
@app.route("/api/messages/<int:msg_id>", methods=["DELETE"])
def delete_message(msg_id):
    global messages

    messages = [msg for msg in messages if msg["id"] != msg_id]

    return jsonify({"status": "deleted"}), 200


# 🚀 health check (IMPORTANTE PRA RAILWAY)
@app.route("/")
def home():
    return jsonify({"status": "API online"}), 200


# 🚀 rodar local (Railway usa gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)