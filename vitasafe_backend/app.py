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
        "ultimo_alerta": status_store.ultimo_alerta
    })

@app.route("/api/emergencia", methods=["POST"])
def set_emergencia():
    data = request.json
    status_store.emergencia_ativa = data.get("ativa", False)
    status_store.ultimo_alerta = time.strftime("%Y-%m-%d %H:%M:%S") if status_store.emergencia_ativa else None
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
