from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

app = Flask(__name__)

# 🔌 conexão com banco (Vercel usa variável de ambiente)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 🗄️ modelo da tabela
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    message = Column(String)
    author = Column(String)

# cria tabela automaticamente (na primeira execução)
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

    if not message:
        return jsonify({"error": "Nenhuma mensagem encontrada"}), 404

    return jsonify({
        "id": message.id,
        "action": message.action,
        "message": message.message,
        "author": message.author
    }), 200


# 🔥 handler para Vercel
handler = app