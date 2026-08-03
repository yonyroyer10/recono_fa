from sqlalchemy import Column, String, LargeBinary, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from database.connection import Base

class Alumno(Base):
    __tablename__ = "alumnos"
    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    embedding = Column(LargeBinary, nullable=True)
    totp_secret = Column(String, nullable=False)
    creado_en = Column(DateTime, server_default=func.now())

class ClaseConfig(Base):
    __tablename__ = "clases_config"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_materia = Column(String, nullable=False)
    hora_inicio = Column(String, nullable=False)
    limite_presente = Column(Integer, nullable=False)
    limite_tarde = Column(Integer, nullable=False)
    activo = Column(Integer, default=1)

class Sesion(Base):
    __tablename__ = "sesiones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    clase_config_id = Column(Integer, ForeignKey("clases_config.id"), nullable=False)
    fecha = Column(String, server_default=func.current_date())
    hora_apertura = Column(DateTime, server_default=func.now())
    hora_cierre = Column(DateTime, nullable=True)
    estado = Column(String, default="ABIERTA")

class Asistencia(Base):
    __tablename__ = "asistencias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sesion_id = Column(Integer, ForeignKey("sesiones.id"), nullable=False)
    alumno_id = Column(String, ForeignKey("alumnos.id"), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    metodo = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    __table_args__ = (UniqueConstraint("sesion_id", "alumno_id", name="uq_sesion_alumno"),)
