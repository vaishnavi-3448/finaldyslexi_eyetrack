import express from "express";
import { spawn } from "child_process";
import cors from "cors";

const app = express();
const PORT = 5000;

app.use(cors()); 

let pythonProcess = null;


app.get("/start-test", (req, res) => {
    if (!pythonProcess) {
        pythonProcess = spawn("python", ["eyetracking.py"]);

        pythonProcess.stdout.on("data", (data) => {
            console.log(`Python Output: ${data}`);
        });

        pythonProcess.stderr.on("data", (data) => {
            console.error(`Python Error: ${data}`);
        });

        pythonProcess.on("exit", (code) => {
            console.log(`Python Process exited with code ${code}`);
            pythonProcess = null;
        });

        res.send("Eye tracking started.");
    } else {
        res.send("Eye tracking is already running.");
    }
});


app.get("/stop-test", (req, res) => {
    if (pythonProcess) {
        pythonProcess.kill();
        pythonProcess = null;
        res.send("Eye tracking stopped.");
    } else {
        res.send("No active eye tracking process.");
    }
});
app.get("/get-score", (req, res) => {
    res.json({ score: finalScore });
  });
  
  
  app.post("/set-score", express.json(), (req, res) => {
    finalScore = req.body.score;
    console.log("Received score:", finalScore);
    res.sendStatus(200);
  });
  

app.get("/", (req, res) => {
    res.send("Eye Tracking Server is Running!");
});


app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});