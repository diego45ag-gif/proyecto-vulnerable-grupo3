from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Almacenamiento en memoria (sin base de datos)
notas = []
contador_id = 1


def buscar_nota(nota_id):
    for nota in notas:
        if nota["id"] == nota_id:
            return nota
    return None


@app.route("/")
def index():
    return render_template("index.html", notas=notas)


@app.route("/agregar", methods=["POST"])
def agregar():
    global contador_id

    titulo = request.form.get("titulo", "").strip()
    contenido = request.form.get("contenido", "").strip()

    # Validación: título y contenido no pueden estar vacíos
    if titulo and contenido:
        notas.append({
            "id": contador_id,
            "titulo": titulo,
            "contenido": contenido,
            "fecha_creacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
        })
        contador_id += 1

    return redirect(url_for("index"))


@app.route("/editar/<int:nota_id>", methods=["GET"])
def editar_form(nota_id):
    nota = buscar_nota(nota_id)

    if nota is None:
        return redirect(url_for("index"))

    return render_template("index.html", notas=notas, nota_editar=nota)


@app.route("/editar/<int:nota_id>", methods=["POST"])
def editar(nota_id):
    nota = buscar_nota(nota_id)

    if nota is not None:
        titulo = request.form.get("titulo", "").strip()
        contenido = request.form.get("contenido", "").strip()

        # Validación: título y contenido no pueden estar vacíos
        if titulo and contenido:
            nota["titulo"] = titulo
            nota["contenido"] = contenido

    return redirect(url_for("index"))


@app.route("/eliminar/<int:nota_id>", methods=["POST"])
def eliminar(nota_id):
    nota = buscar_nota(nota_id)

    if nota is not None:
        notas.remove(nota)

    return redirect(url_for("index"))


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)
