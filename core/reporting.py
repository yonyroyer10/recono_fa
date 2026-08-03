import os
import tempfile
from pathlib import Path
from urllib import request as urllib_request

from database.connection import get_session
from database.models import Alumno, Asistencia, ClaseConfig, Sesion


def build_summary_report(title=None):
    session = get_session()
    try:
        total_alumnos = session.query(Alumno).count()
        total_sesiones = session.query(Sesion).count()
        total_clases = session.query(ClaseConfig).count()
        total_asistencias = session.query(Asistencia).count()
        presentes = session.query(Asistencia).filter(Asistencia.estado == "PRESENTE").count()
        tardes = session.query(Asistencia).filter(Asistencia.estado == "TARDE").count()
        faltas = session.query(Asistencia).filter(Asistencia.estado == "FALTA").count()

        latest_rows = (
            session.query(Asistencia, Alumno, Sesion)
            .join(Alumno, Asistencia.alumno_id == Alumno.id)
            .join(Sesion, Asistencia.sesion_id == Sesion.id)
            .order_by(Asistencia.timestamp.desc())
            .limit(5)
            .all()
        )

        lines = []
        lines.append(title or "Reporte REC - Resumen de asistencia")
        lines.append("=" * 40)
        lines.append(f"Alumnos registrados: {total_alumnos}")
        lines.append(f"Clases configuradas: {total_clases}")
        lines.append(f"Sesiones registradas: {total_sesiones}")
        lines.append(f"Asistencias registradas: {total_asistencias}")
        lines.append(f"Presentes: {presentes}")
        lines.append(f"Tardes: {tardes}")
        lines.append(f"Faltas: {faltas}")
        lines.append("")
        lines.append("Últimos registros:")
        if not latest_rows:
            lines.append("- Sin registros aún")
        else:
            for asistencia, alumno, sesion in latest_rows:
                lines.append(
                    f"- {alumno.nombre} | sesion {sesion.id} | {asistencia.estado} | {asistencia.metodo} | {asistencia.timestamp}"
                )
        return "\n".join(lines)
    finally:
        session.close()


def send_report_via_telegram(report_text, bot_token=None, chat_id=None, caption="Reporte REC"):
    if not bot_token or not chat_id:
        raise ValueError("TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID son obligatorios")

    temp_file = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
            handle.write(report_text)
            temp_file = Path(handle.name)

        payload = []
        boundary = "----RECReportBoundary"
        with temp_file.open("rb") as handle:
            document_bytes = handle.read()

        file_name = Path(temp_file.name).name
        payload.append(f"--{boundary}\r\n".encode("utf-8"))
        payload.append(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode("utf-8"))
        payload.append(f"--{boundary}\r\n".encode("utf-8"))
        payload.append(f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode("utf-8"))
        payload.append(f"--{boundary}\r\n".encode("utf-8"))
        payload.append(
            f'Content-Disposition: form-data; name="document"; filename="{file_name}"\r\n'
            f'Content-Type: text/plain\r\n\r\n'.encode("utf-8")
        )
        payload.append(document_bytes)
        payload.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
        body = b"".join(payload)

        request = urllib_request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendDocument",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        with urllib_request.urlopen(request, timeout=20) as response:
            response.read()
        return True
    finally:
        if temp_file and temp_file.exists():
            temp_file.unlink(missing_ok=True)


def generate_and_send_report(title=None, bot_token=None, chat_id=None):
    report_text = build_summary_report(title=title)
    sent = send_report_via_telegram(report_text, bot_token=bot_token, chat_id=chat_id, caption=title or "Reporte REC")
    return {
        "ok": sent,
        "message": "Reporte enviado a Telegram",
        "report": report_text,
    }
