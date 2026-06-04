from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tareas = []


@app.route("/")
def index():
    return render_template("index.html", tareas=tareas)


@app.route("/add", methods=["POST"])
def add_task():
    texto = request.form.get("tarea", "").strip()

    if texto:
        tareas.append({"texto": texto, "completada": False})

    return redirect(url_for("index"))


@app.route("/complete/<int:tarea_id>")
def complete_task(tarea_id):
    if 0 <= tarea_id < len(tareas):
        tareas[tarea_id]["completada"] = True

    return redirect(url_for("index"))


@app.route("/delete/<int:tarea_id>")
def delete_task(tarea_id):
    if 0 <= tarea_id < len(tareas):
        tareas.pop(tarea_id)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)