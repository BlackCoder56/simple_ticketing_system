from flask import Flask, render_template
import uuid
import qrcode
import os


app = Flask(__name__)
app.config["QR_FOLDER"] = "static/qrcodes"

# Events
EVENTS = [
    {"id":1, "title": "Tech Conference", "price": 20000},
    {"id":2, "title": "Freshers Bowl", "price": 40000},
    {"id":3, "title": "Python Hakathon", "price": 15000},
    {"id":4, "title": "Nyama Choma", "price": 34000},
]

@app.route("/")
def index():
    return render_template("index.html", events=EVENTS)

@app.route("/event/<int:event_id>")
def event_detail(event_id):
    event = next((e for e in EVENTS if e["id"] == event_id), None)
    return render_template("event.html", event=event)

@app.route("/showqrcode", methods=['POST'])
def showqrcode():
    qr_id, file_path = generate_qr()

    return render_template("showqrcode.html", qr_id=qr_id, qr_path=file_path)

# Helper functions
def generate_qr():
    # generate unique ID for this QR
    qr_id = str(uuid.uuid4())
    file_path = os.path.join(app.config["QR_FOLDER"], f"{qr_id}.png")
    
    # creating QR
    qr = qrcode.make(qr_id)
    qr.save(file_path)

    return qr_id, file_path

if __name__ == "__main__":
    app.run(debug=True)