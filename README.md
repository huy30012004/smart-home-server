# Smart Home Server

This repository contains a full-stack IoT smart home project consisting of:

* **Flask Backend**: REST and real-time API built with Flask and Flask-SocketIO, connecting to a MariaDB database for data storage and retrieval. Handles device state toggling and logs.
* **React Dashboard**: Front-end application (Create React App) providing a user interface to monitor and control devices in real-time via Socket.IO and HTTP requests.
* **Device Mock API** *(optional)*: Node.js-based mock server for rapid front-end development without hardware.

---

## Features

* **Device Management**: List, toggle, and track the state of devices (LEDs, relays, sensors).
* **Real-Time Updates**: Leveraging WebSockets to push device state changes instantly to all connected clients.
* **Persistent Storage**: Uses MariaDB to store device configurations and action logs.
* **Modular Architecture**: Clean separation between backend API, database models, and front-end UI.

---

## Repository Structure

```
smart-home-server/
├── app.py                     # Flask application entry point
├── models.py                  # SQLAlchemy ORM definitions
├── requirements.txt           # Python dependencies
├── smart-home-dashboard/      # React front-end application
│   ├── public/
│   ├── src/
│   ├── .env.development       # Front-end env for API URL
│   └── package.json           # React scripts and dependencies
├── smart-home-dashboard-api/  # Node.js mock API server (optional)
│   └── index.js
├── .gitignore                 # Ignore venv, node_modules, env files
└── README.md                  # This file
```

---

## Prerequisites

* Python 3.8+ and pip
* Node.js 14+ and npm (for front-end and mock API)
* MariaDB Server
* (For hardware) Raspberry Pi OS with GPIO libraries (e.g., `gpiozero`)

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/your-username/smart-home-server.git
cd smart-home-server
```

### 2. Set up Backend (Flask)

1. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Configure database URI in `app.py`:

   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = \
     'mysql+pymysql://sh_user:YourPass@localhost:3306/smarthome'
   ```
4. Initialize database and run server:

   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```

### 3. Set up Frontend (React)

```bash
cd smart-home-dashboard
npm install
# Ensure .env.development contains:
# REACT_APP_DEV_API_URL=http://localhost:5000
npm start
```

Access the dashboard at `http://localhost:3000`.

### 4. *(Optional)* Mock API Server

```bash
cd ../smart-home-dashboard-api
npm install
npm start
```

Configure `.env.development` to point to `http://localhost:4001` for mock testing.

---

## Deploy to Raspberry Pi

1. Copy backend folder to Pi (`git clone` or `scp`).
2. Install Python, venv, MariaDB client:

   ```bash
   sudo apt update
   sudo apt install python3-venv python3-pip mariadb-client -y
   ```
3. Set up virtual environment and dependencies as above.
4. Install and configure MariaDB on Pi:

   ```sql
   CREATE DATABASE smarthome;
   CREATE USER 'sh_user'@'%' IDENTIFIED BY 'YourPass';
   GRANT ALL ON smarthome.* TO 'sh_user'@'%';
   ```

   * Edit `/etc/mysql/my.cnf` to `bind-address = 0.0.0.0`
5. Run Flask server on Pi:

   ```bash
   flask run --host=0.0.0.0
   ```
6. Update `REACT_APP_DEV_API_URL` to Pi's IP.

---

## GPIO Integration

In `app.py`, within the toggle route:

```python
from gpiozero import LED

@app.route('/api/device/<int:device_id>/toggle', methods=['POST'])
def toggle(device_id):
    device = Device.query.get_or_404(device_id)
    device.status = not device.status
    db.session.commit()
    led = LED(device.pin)
    if device.status:
        led.on()
    else:
        led.off()
    # Broadcast via SocketIO if enabled
    return jsonify({'id': device.id, 'status': device.status})
```

---

## Contributing

1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/xyz`).
3. Commit your changes (`git commit -m 'Add xyz'`).
4. Push branch (`git push origin feature/xyz`).
5. Open a Pull Request.

---

## License

[MIT](LICENSE)
