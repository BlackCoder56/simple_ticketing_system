from flask import Flask, render_template, request
import uuid
import qrcode
import os

from models import db, Event, Ticket


app = Flask(__name__)

# Folder for saving QR images
app.config["QR_FOLDER"] = "static/qrcodes"

# PostgreSQL database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:swap1@localhost/simple_ticketing_system"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# -----------------------------
# Home - List all events from DB
# -----------------------------
@app.route("/")
def index():
    events = Event.query.all()   # instead of in-memory EVENTS[]
    return render_template("index.html", events=events)


# -----------------------------
# Show event details
# -----------------------------
@app.route("/event/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event.html", event=event)


# -----------------------------
# Buy a ticket
# -----------------------------
@app.route("/buy/<int:event_id>", methods=["POST"])
def buy_ticket(event_id):
    event = Event.query.get_or_404(event_id)

    # Validate quantity input
    try:
        quantity = int(request.form.get("quantity", 1))
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
    except ValueError as ve:
        return f"Invalid quantity: {ve}", 400

    tickets = []
    try:
        for _ in range(quantity):
            qr_id, file_path = generate_qr(event.title)
            ticket = Ticket(qr_id=qr_id, event_id=event.id, qr_path=file_path)
            db.session.add(ticket)
            tickets.append(ticket)

        db.session.commit()

    except Exception as e:
        db.session.rollback()  # Rollback if any error occurs
        return f"An error occurred while purchasing tickets: {e}", 500

    return render_template("tickets.html", tickets=tickets)


# -----------------------------
# View all purchased tickets
# -----------------------------
@app.route("/tickets")
def list_tickets():
    tickets = Ticket.query.all()
    return render_template("tickets.html", tickets=tickets)


# -----------------------------
# View a single ticket via QR ID
# -----------------------------
@app.route("/ticket/<qr_id>")
def view_ticket(qr_id):
    ticket = Ticket.query.filter_by(qr_id=qr_id).first()

    if not ticket:
        return "Ticket not found", 404

    return render_template("view_ticket.html", ticket=ticket)


# -----------------------------
# QR Generator Helper
# -----------------------------
def generate_qr(event_title):
    qr_id = str(uuid.uuid4())
    file_path = os.path.join(app.config["QR_FOLDER"], f"{qr_id}.png")

    qr = qrcode.make(qr_id)
    qr.save(file_path)

    return qr_id, file_path


# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # Creates tables ONLY if they don't exist
    app.run(debug=True)