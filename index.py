from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

app = Flask(__name__)

# 🔌 conexão com banco
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL não definida!")

# 🔥 ajuste importante (Railway/Postgres)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# 🗄️ tabela
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    message = Column(String)
    author = Column(String)


# cria tabela
Base.metadata.create_all(bind=engine)


# ✅ POST → salvar mensagem
@app.route("/message", methods=["POST"])
def update_message():
    data = request.get_json(force=True)

    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    db = SessionLocal()

    new_message = Message(
        action=data.get("action"),
        message=data.get("message"),
        author=data.get("author")
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
    }), 201


# ✅ GET → pegar última mensagem
@app.route("/message", methods=["GET"])
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


# 🔥 health check (IMPORTANTE)
@app.route("/")
def home():
    return "API com PostgreSQL funcionando", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)