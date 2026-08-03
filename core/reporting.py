import os
import tempfile
from database.connection import get_session
from database.models import Alumno, Asistencia, Sesion, ClaseConfig

import requests


def build_summary_report(title=None):
    session = get_session()
    try:
        total_alumnos = session.query(Alumno).count()
        total_asistencias = session.query(Asistencia).count()
        presentes = session.query(Asistencia).filter(Asistencia.estado=="PRESENTE").count()
        lines = []
        lines.append(title or "Reporte REC - Resumen")
        lines.append("="*40)
        lines.append(f"Alumnos: {total_alumnos}")
        lines.append(f"Asistencias: {total_asistencias}")
        lines.append(f"Presentes: {presentes}")
        return "\n".join(lines)
    finally:
        session.close()


def send_report_via_telegram(report_text, bot_token, chat_id, caption="Reporte REC"):
    if not bot_token or not chat_id:
        raise ValueError("Missing Telegram configuration")

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt") as f:
            f.write(report_text)
            temp_path = f.name

        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        with open(temp_path, 'rb') as fh:
            files = {'document': (os.path.basename(temp_path), fh)}
            payload = {'chat_id': chat_id, 'caption': caption}
            r = requests.post(url, data=payload, files=files, timeout=20)
            r.raise_for_status()

        return True
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception:
                pass


def generate_and_send_report(title=None, bot_token=None, chat_id=None):
    report = build_summary_report(title)
    return send_report_via_telegram(report, bot_token, chat_id, caption=title or "Reporte REC")
