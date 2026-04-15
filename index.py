from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

app = Flask(__name__)

# 🔌 conexão com banco
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL não definida!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 🗄️ modelo
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    message = Column(String)
    author = Column(String)

# cria tabela
Base.metadata.create_all(bind=engine)


# 📩 salvar mensagem
@app.route("/api/message", methods=["PUT"])
def update_message():
    data = request.get_json()
    db = SessionLocal()

    new_message = Message(
        action=data["action"],
        message=data["message"],
        author=data["author"]
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    db.close()

    return jsonify({
        "status": "saved",
        "data": {
            "id": new_message.id,
            "action": new_message.action,
            "message": new_message.message,
            "author": new_message.author
        }
    }), 200


# 📥 buscar última mensagem
@app.route("/api/messagem", methods=["GET"])
def get_message():
    db = SessionLocal()

    message = db.query(Message).order_by(Message.id.desc()).first()
    db.close()

    if not message:
        return jsonify({"error": "Nenhuma mensagem encontrada"}), 404

    return jsonify({
        "id": message.id,
        "action": message.action,
        "message": message.message,
        "author": message.author
    }), 200


# 🚀 rodar local / produção
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)