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
La interfaz web de [student_app.html](student_app.html) está lista para publicarse como un sitio estático en Vercel o Render.

### Opción rápida
1. Sube este repositorio a GitHub.
2. Conecta el repositorio en Vercel o Render.
3. Usa la raíz del proyecto como carpeta de publicación.
4. El archivo `index.html` será la entrada principal.

## Variables de entorno recomendadas
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `DATABASE_URL` (opcional; por defecto usa SQLite local)

## Nota importante
La parte de escritorio (`app.py`) no está pensada para correr en Vercel/Render porque depende de cámara local, Tkinter y OpenCV. Para una versión completamente web haría falta reescribirla como backend con interfaz web.
