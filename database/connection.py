from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from core.config import DATABASE_URL


def _build_engine():
    engine_kwargs = {"pool_pre_ping": True}
    if DATABASE_URL.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(DATABASE_URL, **engine_kwargs)


# Crear el motor de Base de Datos (SQLite local o PostgreSQL en Render)
engine = _build_engine()

# Fabrica de sesiones con soporte para hilos concurrentes
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)

# Clase base declarativa para los modelos ORM
Base = declarative_base()


def init_db():
    """Inicializa la base de datos y crea todas las tablas si no existen."""
    import database.models  # Importación tardía para asegurar el registro de los modelos
    Base.metadata.create_all(bind=engine)


def get_session():
    """Retorna una sesión limpia para operaciones directas."""
    return Session()
