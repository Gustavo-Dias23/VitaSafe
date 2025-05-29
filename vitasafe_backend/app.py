from flask import Flask, request, jsonify, render_template
import status_store
import time

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("status.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "emergencia_ativa": status_store.emergencia_ativa,
        "ultimo_alerta": status_store.ultimo_alerta,
        "historico": status_store.historico_alertas
    })

@app.route("/api/emergencia", methods=["POST"])
def set_emergencia():
    data = request.json
    ativar = data.get("ativa", False)

    if ativar and not status_store.emergencia_ativa:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        status_store.emergencia_ativa = True
        status_store.ultimo_alerta = timestamp
        status_store.historico_alertas.append(timestamp)
    elif not ativar:
        status_store.emergencia_ativa = False

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
v