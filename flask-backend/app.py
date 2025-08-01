from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://sh_user:YourPass@localhost/smarthome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    status = db.Column(db.Boolean, default=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/devices', methods=['GET'])
def get_devices():
    return jsonify([{'id': d.id, 'name': d.name, 'status': d.status} for d in Device.query.all()])

@app.route('/api/device/<int:device_id>/toggle', methods=['POST'])
def toggle_device(device_id):
    d = Device.query.get_or_404(device_id)
    d.status = not d.status
    db.session.commit()
    return jsonify({'id': d.id, 'status': d.status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)