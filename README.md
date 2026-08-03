# REC - Sistema Híbrido de Asistencia Biométrica

Este proyecto contiene una aplicación de escritorio para registro de asistencia mediante reconocimiento facial y códigos QR dinámicos.

## Estructura principal
- `app.py`: aplicación principal de escritorio (Tkinter + OpenCV + CustomTkinter)
- `student_app.html`: app web para el alumno que genera un QR dinámico TOTP
- `enroll.py`: enrolamiento de estudiantes con rostro y TOTP
- `core/`: motores de reconocimiento facial, QR y configuración
- `database/`: modelos ORM y conexión a SQLite

## Requisitos locales
```bash
pip install -r requirements.txt
```

## Ejecutar la app de escritorio
```bash
python app.py
```

## Ejecutar el enrolamiento
```bash
python enroll.py --id 20230045 --nombre "Juan Perez"
```

## Desplegar la app del alumno en la web
La interfaz web de [student_app.html](student_app.html) ya está preparada para publicarse como una app web Python con Flask y Gunicorn.

### Opción rápida
1. Sube este repositorio a GitHub.
2. Conecta el repositorio en Render (o cualquier proveedor que ejecute Python).
3. Usa la raíz del proyecto como carpeta de publicación.
4. El servicio iniciará con `gunicorn app:app` y servirá `index.html` en la ruta `/`.

## Variables de entorno recomendadas
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `DATABASE_URL` (opcional; por defecto usa SQLite local. En Render puedes usar una base PostgreSQL gestionada)

## Base de datos y reportes
- La app usa SQLAlchemy y soporta SQLite local o PostgreSQL cuando `DATABASE_URL` esté configurada.
- El endpoint `POST /reportes/enviar` genera un reporte temporal, lo envía por Telegram y lo elimina inmediatamente después.

## Nota importante
La parte de escritorio (`app.py`) no está pensada para correr en Vercel/Render porque depende de cámara local, Tkinter y OpenCV. Para una versión completamente web haría falta reescribirla como backend con interfaz web.
