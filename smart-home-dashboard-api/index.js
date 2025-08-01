const express = require("express");
const { createServer } = require("http");
const { Server } = require("socket.io");
const fs = require("fs");
const path = require("path");


const port = process.env.PORT || 4001;
const app = express();
const pathToFile = path.resolve("./feed.json");

const updateFeed = () => {
  const { SmartBulb, SmartOutlet, SmartTemperatureSensor } = JSON.parse(
    fs.readFileSync(pathToFile)
  );

  SmartOutlet.powerConsumption === 6
    ? (SmartOutlet.powerConsumption = 10)
    : (SmartOutlet.powerConsumption = 6);

  SmartBulb.brightness === 78
    ? (SmartBulb.brightness = 85)
    : (SmartBulb.brightness = 78);

  SmartTemperatureSensor.temperature === 21
    ? (SmartTemperatureSensor.temperature = 23)
    : (SmartTemperatureSensor.temperature = 21);

  fs.writeFileSync(
    pathToFile,
    JSON.stringify({ SmartBulb, SmartOutlet, SmartTemperatureSensor }, null, 2)
  );
};

setInterval(() => {
  updateFeed();
}, 2000);

app.get("/", (req, res) => {
  res.status(200).send("Server ready");
});

const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: [
      "http://localhost:3000",
      "https://smart-home-dashboard.vercel.app",
    ],
  },
});
const getDeviceDetails = () => JSON.parse(fs.readFileSync(pathToFile));

let interval;

io.on("connection", (socket) => {
  console.log(`New client connected,${socket.id} `);
  if (interval) {
    clearInterval(interval);
  }
  interval = setInterval(() => getApiAndEmit(socket), 2000);
  socket.on("disconnect", () => {
    clearInterval(interval);
    console.log(`Client disconnected, ${socket.id}`);
  });
});
const getApiAndEmit = (socket) => {
  getDeviceDetails();

  socket.emit("refresh", getDeviceDetails());
};
httpServer.listen(port, () => console.log(`Listening on port ${port}`));
