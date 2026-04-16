from flask import Flask, request, jsonify

app = Flask(__name__)

data_msm = {}

# ✅ POST → salvar mensagem
@app.route("/message", methods=["POST"])
def update_message():
    data = request.get_json(force=True)

    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    data_msm["message"] = {
        "action": data.get("action"),
        "message": data.get("message"),
        "author": data.get("author")
    }

    return jsonify({
        "status": "saved",
        "data": data_msm["message"]
    }), 200


# ✅ GET → recuperar mensagem
@app.route("/message", methods=["GET"])
def get_message():
    if "message" not in data_msm:
        return jsonify({"error": "Nenhuma mensagem encontrada"}), 404

    return jsonify(data_msm["message"]), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)