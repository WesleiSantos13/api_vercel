from flask import Flask, request, jsonify

app = Flask(__name__)

data_msm = {}

@app.route("/api/message", methods=["PUT"])
def update_message():
    data = request.get_json()

    data_msm["message"] = {
        "action": data["action"],
        "message": data["message"],
        "author": data["author"]
    }

    return jsonify({
        "status": "saved",
        "data": data_msm["message"]
    }), 200


@app.route("/api/message", methods=["GET"])
def get_message():
    if "message" not in data_msm:
        return jsonify({"error": "Nenhuma mensagem encontrada"}), 404

    return jsonify(data_msm["message"]), 200