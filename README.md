# REC Asistencia - Clean rebuild

Esta rama contiene una versión limpia orientada a despliegue web (Flask).

Endpoints:
- / -> student_app.html
- /student-app -> student_app.html
- /health -> status
- POST /reportes/enviar -> enviar reporte a Telegram

Variables de entorno:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- DATABASE_URL (opcional, Postgres)
