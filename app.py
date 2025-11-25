from flask import Flask, render_template
import uuid
import qrcode
import os


app = Flask(__name__)
app.config["QR_FOLDER"] = "static/qrcodes"

def generate_qr():
    # generate unique ID for this QR
    qr_id = str(uuid.uuid4())
    file_path = os.path.join(app.config["QR_FOLDER"], f"{qr_id}.png")
    
    # creating QR
    qr = qrcode.make(qr_id)
    qr.save(file_path)

    return qr_id, file_path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/showqrcode", methods=['POST'])
def showqrcode():
    qr_id, file_path = generate_qr()

    return render_template("showqrcode.html", qr_id=qr_id, qr_path=file_path)

if __name__ == "__main__":
    app.run(debug=True)