# REC Asistencia - Clean rebuild

Versión limpia orientada a despliegue web (Flask).

Rama: rebuild-clean

Resumen
- Interfaz web para alumnos: `student_app.html` (genera QR TOTP)
- Backend Flask mínimo para servir la interfaz y enviar reportes por Telegram
- SQLAlchemy para persistencia (SQLite por defecto, PostgreSQL en producción via DATABASE_URL)

Endpoints
- GET / -> student_app.html
- GET /student-app -> student_app.html
- GET /health -> {"status":"ok"}
- POST /reportes/enviar -> envía reporte resumen a Telegram (JSON: {"title":"..."})

Variables de entorno (obligatorias para reportes)
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

Optional
- DATABASE_URL (postgres://... or postgresql://...); si no existe se usa SQLite local

Instalación y ejecución local
1. Crear y activar un virtualenv (recomendado)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # PowerShell

2. Instalar dependencias
   pip install -r requirements.txt

3. Inicializar la DB y arrancar
   python app.py

Despliegue (Render)
- Branch: `rebuild-clean`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Health Check Path: `/health`
- Añadir env vars en Render: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, opcional DATABASE_URL

Notas de diseño
- La parte de reconocimiento facial y modelos ONNX quedan fuera de esta rama para mantener el servicio web ligero.
- Para producción con reconocimiento facial, separar en un servicio independiente con recursos mayores.

Contacto
- Mantén tus tokens fuera del repositorio y nunca los pegues en chats públicos.
