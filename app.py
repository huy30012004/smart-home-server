# flask-backend/app.py

import os
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 1) Khởi tạo app và CORS
app = Flask(__name__)
CORS(app)

# 2) Cấu hình MariaDB
#   - Bạn có thể set biến môi trường DB_USER, DB_PASS, DB_HOST, DB_NAME
DB_USER   = os.getenv('DB_USER',   'sh_user')
DB_PASS   = os.getenv('DB_PASS',   'YourPass')
DB_HOST   = os.getenv('DB_HOST',   '192.168.0.100')  # IP của Pi hoặc host MariaDB
DB_NAME   = os.getenv('DB_NAME',   'smarthome')
DB_PORT   = os.getenv('DB_PORT',   '3306')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3) Khởi tạo SQLAlchemy
db = SQLAlchemy(app)

# 4) Định nghĩa model (ví dụ một sensor nhiệt độ)
class TemperatureSensor(db.Model):
    __tablename__ = 'temperature_sensors'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    timestamp   = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id':          self.id,
            'name':        self.name,
            'temperature': self.temperature,
            'timestamp':   self.timestamp.isoformat()
        }

# 5) Tạo bảng lần đầu (chỉ chạy 1 lần)
@app.before_first_request
def create_tables():
    db.create_all()

# 6) Routes ví dụ:
@app.route('/api/temperatures', methods=['GET'])
def list_temperatures():
    """Trả về toàn bộ record sensor."""
    records = TemperatureSensor.query.order_by(TemperatureSensor.timestamp.desc()).all()
    return jsonify([r.to_dict() for r in records])

@app.route('/api/temperatures', methods=['POST'])
def add_temperature():
    """Nhận JSON { name, temperature } và lưu vào MariaDB."""
    data = request.get_json() or {}
    name = data.get('name')
    temp = data.get('temperature')
    if name is None or temp is None:
        abort(400, description="`name` và `temperature` là bắt buộc")
    record = TemperatureSensor(name=name, temperature=float(temp))
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201

@app.route('/api/temperatures/<int:rec_id>', methods=['DELETE'])
def delete_temperature(rec_id):
    """Xoá 1 record."""
    record = TemperatureSensor.query.get_or_404(rec_id)
    db.session.delete(record)
    db.session.commit()
    return '', 204

# 7) Chạy app
if __name__ == '__main__':
    # nếu bạn muốn chạy socketIO, import và chạy socketio.run(app,...)
    app.run(host='0.0.0.0', port=4001, debug=True)
