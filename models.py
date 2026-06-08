from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    pin = db.Column(db.String(10), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    pagado = db.Column(db.Boolean, default=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)


class Partido(db.Model):
    __tablename__ = "partidos"

    id = db.Column(db.Integer, primary_key=True)
    etapa = db.Column(db.String(50))
    grupo = db.Column(db.String(50))
    numero = db.Column(db.Integer)
    equipo_local = db.Column(db.String(100))
    equipo_visitante = db.Column(db.String(100))
    fecha_texto = db.Column(db.String(100))
    fecha_hora = db.Column(db.DateTime)
    goles_local = db.Column(db.Integer)
    goles_visitante = db.Column(db.Integer)
    cerrado = db.Column(db.Boolean, default=False)


class Pronostico(db.Model):
    __tablename__ = "pronosticos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    partido_id = db.Column(db.Integer, db.ForeignKey("partidos.id"))
    pron_local = db.Column(db.Integer)
    pron_visitante = db.Column(db.Integer)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship("Usuario", backref="pronosticos")
    partido = db.relationship("Partido", backref="pronosticos")
