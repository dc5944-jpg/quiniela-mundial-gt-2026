import random
from datetime import datetime

from flask import Flask, render_template, request, redirect, session, flash
from config import Config
from models import db, Usuario, Partido, Pronostico

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

PRECIO_INSCRIPCION = 150
PARTIDOS_INICIALES = [('Jornada 1', 'Grupo A', 1, 'México', 'Sudáfrica', 'Jue 11 Jun 2026'), ('Jornada 1', 'Grupo A', 2, 'Corea del Sur', 'Chequia', 'Jue 11 Jun 2026'), ('Jornada 1', 'Grupo B', 3, 'Canadá', 'Bosnia y Herzegovina', 'Vie 12 Jun 2026'), ('Jornada 1', 'Grupo D', 4, 'Estados Unidos', 'Paraguay', 'Vie 12 Jun 2026'), ('Jornada 1', 'Grupo C', 5, 'Haití', 'Escocia', 'Sáb 13 Jun 2026'), ('Jornada 1', 'Grupo D', 6, 'Australia', 'Turquía', 'Sáb 13 Jun 2026'), ('Jornada 1', 'Grupo C', 7, 'Brasil', 'Marruecos', 'Sáb 13 Jun 2026'), ('Jornada 1', 'Grupo B', 8, 'Qatar', 'Suiza', 'Sáb 13 Jun 2026'), ('Jornada 1', 'Grupo E', 9, 'Costa de Marfil', 'Ecuador', 'Dom 14 Jun 2026'), ('Jornada 1', 'Grupo E', 10, 'Alemania', 'Curazao', 'Dom 14 Jun 2026'), ('Jornada 1', 'Grupo F', 11, 'Países Bajos', 'Japón', 'Dom 14 Jun 2026'), ('Jornada 1', 'Grupo F', 12, 'Suecia', 'Túnez', 'Dom 14 Jun 2026'), ('Jornada 1', 'Grupo H', 13, 'Arabia Saudita', 'Uruguay', 'Lun 15 Jun 2026'), ('Jornada 1', 'Grupo H', 14, 'España', 'Cabo Verde', 'Lun 15 Jun 2026'), ('Jornada 1', 'Grupo G', 15, 'Irán', 'Nueva Zelanda', 'Lun 15 Jun 2026'), ('Jornada 1', 'Grupo G', 16, 'Bélgica', 'Egipto', 'Lun 15 Jun 2026'), ('Jornada 1', 'Grupo I', 17, 'Francia', 'Senegal', 'Mar 16 Jun 2026'), ('Jornada 1', 'Grupo I', 18, 'Irak', 'Noruega', 'Mar 16 Jun 2026'), ('Jornada 1', 'Grupo J', 19, 'Argentina', 'Argelia', 'Mar 16 Jun 2026'), ('Jornada 1', 'Grupo J', 20, 'Austria', 'Jordania', 'Mar 16 Jun 2026'), ('Jornada 1', 'Grupo L', 21, 'Ghana', 'Panamá', 'Mié 17 Jun 2026'), ('Jornada 1', 'Grupo L', 22, 'Inglaterra', 'Croacia', 'Mié 17 Jun 2026'), ('Jornada 1', 'Grupo K', 23, 'Portugal', 'RD Congo', 'Mié 17 Jun 2026'), ('Jornada 1', 'Grupo K', 24, 'Uzbekistán', 'Colombia', 'Mié 17 Jun 2026'), ('Jornada 2', 'Grupo A', 1, 'Chequia', 'Sudáfrica', 'Jue 18 Jun 2026'), ('Jornada 2', 'Grupo B', 2, 'Suiza', 'Bosnia y Herzegovina', 'Jue 18 Jun 2026'), ('Jornada 2', 'Grupo B', 3, 'Canadá', 'Qatar', 'Jue 18 Jun 2026'), ('Jornada 2', 'Grupo A', 4, 'México', 'Corea del Sur', 'Jue 18 Jun 2026'), ('Jornada 2', 'Grupo D', 5, 'Estados Unidos', 'Australia', 'Vie 19 Jun 2026'), ('Jornada 2', 'Grupo C', 6, 'Escocia', 'Marruecos', 'Vie 19 Jun 2026'), ('Jornada 2', 'Grupo C', 7, 'Brasil', 'Haití', 'Vie 19 Jun 2026'), ('Jornada 2', 'Grupo D', 8, 'Turquía', 'Paraguay', 'Vie 19 Jun 2026'), ('Jornada 2', 'Grupo F', 9, 'Países Bajos', 'Suecia', 'Sáb 20 Jun 2026'), ('Jornada 2', 'Grupo E', 10, 'Alemania', 'Costa de Marfil', 'Sáb 20 Jun 2026'), ('Jornada 2', 'Grupo E', 11, 'Ecuador', 'Curazao', 'Dom 21 Jun 2026'), ('Jornada 2', 'Grupo F', 12, 'Túnez', 'Japón', 'Dom 21 Jun 2026'), ('Jornada 2', 'Grupo H', 13, 'España', 'Arabia Saudita', 'Dom 21 Jun 2026'), ('Jornada 2', 'Grupo G', 14, 'Bélgica', 'Irán', 'Dom 21 Jun 2026'), ('Jornada 2', 'Grupo H', 15, 'Uruguay', 'Cabo Verde', 'Dom 21 Jun 2026'), ('Jornada 2', 'Grupo G', 16, 'Nueva Zelanda', 'Egipto', 'Dom 21 Jun 2026'), ('Jornada 2', 'Grupo J', 17, 'Argentina', 'Austria', 'Lun 22 Jun 2026'), ('Jornada 2', 'Grupo I', 18, 'Francia', 'Irak', 'Lun 22 Jun 2026'), ('Jornada 2', 'Grupo I', 19, 'Noruega', 'Senegal', 'Mar 23 Jun 2026'), ('Jornada 2', 'Grupo J', 20, 'Jordania', 'Argelia', 'Mar 23 Jun 2026'), ('Jornada 2', 'Grupo K', 21, 'Portugal', 'Uzbekistán', 'Mar 23 Jun 2026'), ('Jornada 2', 'Grupo L', 22, 'Inglaterra', 'Ghana', 'Mar 23 Jun 2026'), ('Jornada 2', 'Grupo L', 23, 'Panamá', 'Croacia', 'Mié 24 Jun 2026'), ('Jornada 2', 'Grupo K', 24, 'Colombia', 'RD Congo', 'Mié 24 Jun 2026'), ('Jornada 3', 'Grupo B', 1, 'Suiza', 'Canadá', 'Mié 24 Jun 2026'), ('Jornada 3', 'Grupo B', 2, 'Bosnia y Herzegovina', 'Qatar', 'Mié 24 Jun 2026'), ('Jornada 3', 'Grupo C', 3, 'Marruecos', 'Haití', 'Mié 24 Jun 2026'), ('Jornada 3', 'Grupo C', 4, 'Escocia', 'Brasil', 'Mié 24 Jun 2026'), ('Jornada 3', 'Grupo A', 5, 'Sudáfrica', 'Corea del Sur', 'Jue 25 Jun 2026'), ('Jornada 3', 'Grupo A', 6, 'Chequia', 'México', 'Jue 25 Jun 2026'), ('Jornada 3', 'Grupo E', 7, 'Curazao', 'Costa de Marfil', 'Jue 25 Jun 2026'), ('Jornada 3', 'Grupo E', 8, 'Ecuador', 'Alemania', 'Jue 25 Jun 2026'), ('Jornada 3', 'Grupo F', 9, 'Túnez', 'Países Bajos', 'Vie 26 Jun 2026'), ('Jornada 3', 'Grupo F', 10, 'Japón', 'Suecia', 'Vie 26 Jun 2026'), ('Jornada 3', 'Grupo D', 11, 'Turquía', 'Estados Unidos', 'Vie 26 Jun 2026'), ('Jornada 3', 'Grupo D', 12, 'Paraguay', 'Australia', 'Vie 26 Jun 2026'), ('Jornada 3', 'Grupo I', 13, 'Noruega', 'Francia', 'Vie 26 Jun 2026'), ('Jornada 3', 'Grupo I', 14, 'Senegal', 'Irak', 'Vie 26 Jun 2026'), ('Jornada 3', 'Grupo H', 15, 'Cabo Verde', 'Arabia Saudita', 'Sáb 27 Jun 2026'), ('Jornada 3', 'Grupo H', 16, 'Uruguay', 'España', 'Sáb 27 Jun 2026'), ('Jornada 3', 'Grupo G', 17, 'Nueva Zelanda', 'Bélgica', 'Sáb 27 Jun 2026'), ('Jornada 3', 'Grupo G', 18, 'Egipto', 'Irán', 'Sáb 27 Jun 2026'), ('Jornada 3', 'Grupo L', 19, 'Panamá', 'Inglaterra', 'Sáb 27 Jun 2026'), ('Jornada 3', 'Grupo L', 20, 'Croacia', 'Ghana', 'Sáb 27 Jun 2026'), ('Jornada 3', 'Grupo K', 21, 'Colombia', 'Portugal', 'Dom 28 Jun 2026'), ('Jornada 3', 'Grupo K', 22, 'RD Congo', 'Uzbekistán', 'Dom 28 Jun 2026'), ('Jornada 3', 'Grupo J', 23, 'Argelia', 'Austria', 'Dom 28 Jun 2026'), ('Jornada 3', 'Grupo J', 24, 'Jordania', 'Argentina', 'Dom 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 1, 'Ronda de 32 - Equipo A 1', 'Ronda de 32 - Equipo B 1', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 2, 'Ronda de 32 - Equipo A 2', 'Ronda de 32 - Equipo B 2', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 3, 'Ronda de 32 - Equipo A 3', 'Ronda de 32 - Equipo B 3', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 4, 'Ronda de 32 - Equipo A 4', 'Ronda de 32 - Equipo B 4', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 5, 'Ronda de 32 - Equipo A 5', 'Ronda de 32 - Equipo B 5', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 6, 'Ronda de 32 - Equipo A 6', 'Ronda de 32 - Equipo B 6', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 7, 'Ronda de 32 - Equipo A 7', 'Ronda de 32 - Equipo B 7', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 8, 'Ronda de 32 - Equipo A 8', 'Ronda de 32 - Equipo B 8', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 9, 'Ronda de 32 - Equipo A 9', 'Ronda de 32 - Equipo B 9', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 10, 'Ronda de 32 - Equipo A 10', 'Ronda de 32 - Equipo B 10', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 11, 'Ronda de 32 - Equipo A 11', 'Ronda de 32 - Equipo B 11', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 12, 'Ronda de 32 - Equipo A 12', 'Ronda de 32 - Equipo B 12', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 13, 'Ronda de 32 - Equipo A 13', 'Ronda de 32 - Equipo B 13', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 14, 'Ronda de 32 - Equipo A 14', 'Ronda de 32 - Equipo B 14', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 15, 'Ronda de 32 - Equipo A 15', 'Ronda de 32 - Equipo B 15', 'Desde 28 Jun 2026'), ('Ronda de 32', 'Eliminación', 16, 'Ronda de 32 - Equipo A 16', 'Ronda de 32 - Equipo B 16', 'Desde 28 Jun 2026'), ('Octavos', 'Eliminación', 1, 'Octavos - Equipo A 1', 'Octavos - Equipo B 1', 'Jul 2026'), ('Octavos', 'Eliminación', 2, 'Octavos - Equipo A 2', 'Octavos - Equipo B 2', 'Jul 2026'), ('Octavos', 'Eliminación', 3, 'Octavos - Equipo A 3', 'Octavos - Equipo B 3', 'Jul 2026'), ('Octavos', 'Eliminación', 4, 'Octavos - Equipo A 4', 'Octavos - Equipo B 4', 'Jul 2026'), ('Octavos', 'Eliminación', 5, 'Octavos - Equipo A 5', 'Octavos - Equipo B 5', 'Jul 2026'), ('Octavos', 'Eliminación', 6, 'Octavos - Equipo A 6', 'Octavos - Equipo B 6', 'Jul 2026'), ('Octavos', 'Eliminación', 7, 'Octavos - Equipo A 7', 'Octavos - Equipo B 7', 'Jul 2026'), ('Octavos', 'Eliminación', 8, 'Octavos - Equipo A 8', 'Octavos - Equipo B 8', 'Jul 2026'), ('Cuartos', 'Eliminación', 1, 'Cuartos - Equipo A 1', 'Cuartos - Equipo B 1', 'Jul 2026'), ('Cuartos', 'Eliminación', 2, 'Cuartos - Equipo A 2', 'Cuartos - Equipo B 2', 'Jul 2026'), ('Cuartos', 'Eliminación', 3, 'Cuartos - Equipo A 3', 'Cuartos - Equipo B 3', 'Jul 2026'), ('Cuartos', 'Eliminación', 4, 'Cuartos - Equipo A 4', 'Cuartos - Equipo B 4', 'Jul 2026'), ('Semifinales', 'Eliminación', 1, 'Semifinal - Equipo A 1', 'Semifinal - Equipo B 1', 'Jul 2026'), ('Semifinales', 'Eliminación', 2, 'Semifinal - Equipo A 2', 'Semifinal - Equipo B 2', 'Jul 2026'), ('Tercer Lugar', 'Eliminación', 1, 'Perdedor Semifinal 1', 'Perdedor Semifinal 2', 'Jul 2026'), ('Final', 'Eliminación', 1, 'Ganador Semifinal 1', 'Ganador Semifinal 2', 'Jul 2026')]


def usuario_actual():
    if "usuario_id" not in session:
        return None
    return Usuario.query.get(session["usuario_id"])


def es_admin():
    usuario = usuario_actual()
    return usuario and usuario.es_admin


def ganador(gl, gv):
    if gl is None or gv is None:
        return None
    if gl > gv:
        return "L"
    if gv > gl:
        return "V"
    return "E"


def diferencia(gl, gv):
    return gl - gv


def puntos_pronostico(pronostico, partido):
    if partido.goles_local is None or partido.goles_visitante is None:
        return 0, False

    exacto = (
        pronostico.pron_local == partido.goles_local and
        pronostico.pron_visitante == partido.goles_visitante
    )

    if exacto:
        return 5, True

    if diferencia(pronostico.pron_local, pronostico.pron_visitante) == diferencia(partido.goles_local, partido.goles_visitante):
        return 3, False

    if ganador(pronostico.pron_local, pronostico.pron_visitante) == ganador(partido.goles_local, partido.goles_visitante):
        return 1, False

    return 0, False


def calcular_ranking(etapa=None):
    participantes = Usuario.query.filter_by(es_admin=False).all()
    ranking = []

    for participante in participantes:
        query = Pronostico.query.join(Partido).filter(
            Pronostico.usuario_id == participante.id
        )

        if etapa:
            query = query.filter(Partido.etapa == etapa)

        pronosticos = query.all()

        puntos = 0
        exactos = 0
        pronosticos_validos = 0

        for pron in pronosticos:
            if pron.pron_local is None or pron.pron_visitante is None:
                continue

            # No contar 0-0 automático como pronóstico válido si el partido aún no tiene resultado
            if pron.pron_local == 0 and pron.pron_visitante == 0:
                if pron.partido.goles_local is None and pron.partido.goles_visitante is None:
                    continue

            pronosticos_validos += 1

            pts, ex = puntos_pronostico(pron, pron.partido)
            puntos += pts

            if ex:
                exactos += 1

        ranking.append({
            "participante": participante,
            "puntos": puntos,
            "exactos": exactos,
            "pronosticos": pronosticos_validos
        })

    ranking.sort(
        key=lambda x: (x["puntos"], x["exactos"], x["pronosticos"]),
        reverse=True
    )

    return ranking


def crear_partidos_iniciales():
    if Partido.query.count() > 0:
        return

    for etapa, grupo, numero, local, visitante, fecha in PARTIDOS_INICIALES:
        partido = Partido(
            etapa=etapa,
            grupo=grupo,
            numero=numero,
            equipo_local=local,
            equipo_visitante=visitante,
            fecha_texto=fecha,
            cerrado=False
        )
        db.session.add(partido)

    db.session.commit()


with app.app_context():
    db.create_all()

    admin = Usuario.query.filter_by(telefono="admin").first()

    if not admin:
        admin = Usuario(
            nombre="Administrador",
            telefono="admin",
            pin="2026",
            es_admin=True,
            pagado=True
        )
        db.session.add(admin)
        db.session.commit()

    crear_partidos_iniciales()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        telefono = request.form.get("telefono", "").strip()
        pin = request.form.get("pin", "").strip()

        usuario = Usuario.query.filter_by(
            telefono=telefono,
            pin=pin
        ).first()

        if usuario:
            session["usuario_id"] = usuario.id

            if usuario.es_admin:
                return redirect("/admin")

            return redirect("/dashboard")

        flash("Credenciales incorrectas")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    usuario = usuario_actual()
    if not usuario:
        return redirect("/")

    ranking = calcular_ranking()
    posicion = "-"
    puntos = 0
    exactos = 0

    for idx, row in enumerate(ranking, 1):
        if row["participante"].id == usuario.id:
            posicion = idx
            puntos = row["puntos"]
            exactos = row["exactos"]
            break

    total_pronosticos = Pronostico.query.filter_by(usuario_id=usuario.id).count()

    return render_template(
        "dashboard.html",
        usuario=usuario,
        posicion=posicion,
        puntos=puntos,
        exactos=exactos,
        total_pronosticos=total_pronosticos
    )


@app.route("/admin")
def admin():
    if not es_admin():
        return redirect("/")

    participantes = Usuario.query.filter_by(
        es_admin=False
    ).order_by(Usuario.id.desc()).all()

    total_participantes = Usuario.query.filter_by(es_admin=False).count()
    total_pagados = Usuario.query.filter_by(es_admin=False, pagado=True).count()
    total_pendientes = Usuario.query.filter_by(es_admin=False, pagado=False).count()
    bolsa = total_pagados * PRECIO_INSCRIPCION

    return render_template(
        "admin.html",
        participantes=participantes,
        total_participantes=total_participantes,
        total_pagados=total_pagados,
        total_pendientes=total_pendientes,
        bolsa=bolsa
    )


@app.route("/crear-participante", methods=["POST"])
def crear_participante():
    if not es_admin():
        return redirect("/")

    nombre = request.form.get("nombre", "").strip()
    telefono = request.form.get("telefono", "").strip()

    if not nombre or not telefono:
        flash("Debes ingresar nombre y teléfono.")
        return redirect("/admin")

    existe = Usuario.query.filter_by(telefono=telefono).first()

    if existe:
        flash("Ese teléfono ya existe.")
        return redirect("/admin")

    pin_generado = str(random.randint(1000, 9999))

    nuevo = Usuario(
        nombre=nombre,
        telefono=telefono,
        pin=pin_generado,
        es_admin=False,
        pagado=False
    )

    db.session.add(nuevo)
    db.session.commit()

    return redirect("/admin")


@app.route("/pagar/<int:id>")
def pagar(id):
    if not es_admin():
        return redirect("/")

    usuario = Usuario.query.get_or_404(id)
    usuario.pagado = True
    db.session.commit()

    return redirect("/admin")


@app.route("/pendiente/<int:id>")
def pendiente(id):
    if not es_admin():
        return redirect("/")

    usuario = Usuario.query.get_or_404(id)
    usuario.pagado = False
    db.session.commit()

    return redirect("/admin")


@app.route("/eliminar/<int:id>")
def eliminar(id):
    if not es_admin():
        return redirect("/")

    usuario = Usuario.query.get_or_404(id)

    if not usuario.es_admin:
        db.session.delete(usuario)
        db.session.commit()

    return redirect("/admin")


@app.route("/admin/partidos")
def admin_partidos():
    if not es_admin():
        return redirect("/")

    etapa = request.args.get("etapa", "Jornada 1")
    partidos = Partido.query.filter_by(etapa=etapa).order_by(Partido.numero).all()
    etapas = [x[0] for x in db.session.query(Partido.etapa).distinct().all()]

    return render_template(
        "admin_partidos.html",
        partidos=partidos,
        etapas=etapas,
        etapa=etapa
    )


@app.route("/admin/partido/<int:id>", methods=["POST"])
def editar_partido(id):
    if not es_admin():
        return redirect("/")

    partido = Partido.query.get_or_404(id)

    partido.equipo_local = request.form.get("equipo_local", "").strip()
    partido.equipo_visitante = request.form.get("equipo_visitante", "").strip()
    partido.fecha_texto = request.form.get("fecha_texto", "").strip()

    gl = request.form.get("goles_local", "").strip()
    gv = request.form.get("goles_visitante", "").strip()
    cerrado = request.form.get("cerrado", "")

    partido.goles_local = int(gl) if gl != "" else None
    partido.goles_visitante = int(gv) if gv != "" else None
    partido.cerrado = True if cerrado == "on" else False

    db.session.commit()

    return redirect(f"/admin/partidos?etapa={partido.etapa}")

def partido_cerrado_automaticamente(partido):
    if partido.cerrado:
        return True

    if not partido.fecha_texto:
        return False

    meses = {
        "Ene": "Jan", "Feb": "Feb", "Mar": "Mar", "Abr": "Apr",
        "May": "May", "Jun": "Jun", "Jul": "Jul", "Ago": "Aug",
        "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dic": "Dec"
    }

    try:
        partes = partido.fecha_texto.split()

        # Ejemplo: Jue 11 Jun 2026
        dia = partes[1]
        mes = meses.get(partes[2], partes[2])
        anio = partes[3]

        # Si tiene hora: Jue 11 Jun 2026 18:00
        hora = partes[4] if len(partes) >= 5 else "23:59"

        fecha_str = f"{dia} {mes} {anio} {hora}"
        fecha_partido = datetime.strptime(fecha_str, "%d %b %Y %H:%M")

        if datetime.now() >= fecha_partido:
            partido.cerrado = True
            db.session.commit()
            return True

    except:
        return False

    return False


@app.route("/pronosticos", methods=["GET", "POST"])
def pronosticos():
    usuario = usuario_actual()

    if not usuario:
        return redirect("/")

    if not usuario.pagado:
        flash("Tu participación aún no está autorizada. Contacta al administrador.")
        return redirect("/dashboard")

    etapa = request.args.get("etapa", "Jornada 1")

    if request.method == "POST":
        partidos = Partido.query.filter_by(etapa=etapa).order_by(Partido.numero).all()

        for partido in partidos:
            if partido_cerrado_automaticamente(partido):
                continue

            local = request.form.get(f"local_{partido.id}", "").strip()
            visita = request.form.get(f"visita_{partido.id}", "").strip()

            if local == "" or visita == "":
                continue

            pron = Pronostico.query.filter_by(
                usuario_id=usuario.id,
                partido_id=partido.id
            ).first()

            if not pron:
                pron = Pronostico(
                    usuario_id=usuario.id,
                    partido_id=partido.id
                )
                db.session.add(pron)

            pron.pron_local = int(local)
            pron.pron_visitante = int(visita)

        db.session.commit()
        flash("Pronósticos guardados correctamente.")
        return redirect(f"/pronosticos?etapa={etapa}")

    partidos = Partido.query.filter_by(etapa=etapa).order_by(Partido.numero).all()

    for partido in partidos:
        partido_cerrado_automaticamente(partido)

    etapas = [x[0] for x in db.session.query(Partido.etapa).distinct().all()]

    pronosticos_usuario = Pronostico.query.filter_by(usuario_id=usuario.id).all()
    pron_map = {p.partido_id: p for p in pronosticos_usuario}

    return render_template(
        "pronosticos.html",
        usuario=usuario,
        partidos=partidos,
        etapas=etapas,
        etapa=etapa,
        pron_map=pron_map
    )


@app.route("/ranking")
def ranking():
    etapa = request.args.get("etapa", "")
    etapas = [x[0] for x in db.session.query(Partido.etapa).distinct().all()]
    data = calcular_ranking(etapa if etapa else None)

    return render_template(
        "ranking.html",
        ranking=data,
        etapas=etapas,
        etapa=etapa
    )


@app.route("/premios")
def premios():
    total_pagados = Usuario.query.filter_by(es_admin=False, pagado=True).count()
    bolsa = total_pagados * PRECIO_INSCRIPCION

    return render_template("premios.html", bolsa=bolsa, total_pagados=total_pagados)


@app.route("/reglamento")
def reglamento():
    return render_template("reglamento.html")


if __name__ == "__main__":
    app.run(debug=True)
