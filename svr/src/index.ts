import express from "express";
import cors from "cors";
import path from "node:path";
import { WebSocketServer, WebSocket } from "ws";
import { createServer } from "node:http";

import { spawn } from "node:child_process";
import { join } from "node:path";




const app = express();
app.use(cors());
app.use(express.json());

const server = createServer(app);
const wss = new WebSocketServer({ server });
const clientDist = path.resolve("../client/dist");


// REST health check
app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.use(express.static(clientDist));

// react client
app.get("/{*path}", (_req, res) => {
  res.sendFile(path.join(clientDist, "index.html"));
});

// Broadcast hardware events to connected browsers
app.post("/api/events", (req, res) => {
  const event = req.body;

  console.log("Event:", event);

  const message = JSON.stringify(event);

  for (const client of wss.clients) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  }

  res.json({ received: true });
});

wss.on("connection", (socket) => {
  console.log("Client connected");

  socket.send(JSON.stringify({
    type: "connected",
    message: "Astrobio server ready"
  }));
});

// plays a test-to-speech message on the server through default audio
app.post("/api/tts", (req, res) => {
  const piper = spawn("../.venv/bin/python", [
    "-m", "piper",
    "-m", "voices/en_GB-alba-medium.onnx",
    "--", req.body.text
  ], { stdio: "inherit" });

  piper.on("error", console.error);
  res.json({ ok: true });
});


const PORT = 3000;

server.listen(PORT, "0.0.0.0", () => {
  console.log(`Astrobio server listening on port ${PORT}`);
  console.log(`http://127.0.0.1:${PORT}`);
});