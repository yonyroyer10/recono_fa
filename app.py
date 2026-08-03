import os
from flask import Flask, jsonify, request, send_from_directory

from database.connection import init_db
from core.reporting import generate_and_send_report

app = Flask(__name__)

init_db()


@app.get("/")
def index():
    return send_from_directory(app.root_path, "index.html")


@app.get("/student-app")
def student_app():
    return send_from_directory(app.root_path, "student_app.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/reportes/enviar")
def send_report():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if not bot_token or not chat_id:
        return jsonify({"ok": False, "error": "Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID"}), 400

    title = None
    if request.is_json:
        title = (request.get_json(silent=True) or {}).get("title")
    if not title:
        title = "Reporte REC"

    try:
        result = generate_and_send_report(title=title, bot_token=bot_token, chat_id=chat_id)
    except Exception as exc:  # pragma: no cover - fallo de red o configuración
        return jsonify({"ok": False, "error": str(exc)}), 500

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
