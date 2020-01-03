const { exec, spawn } = require('child_process');
const bodyParser = require("body-parser");
const express = require('express');
const config = require('./config.json');
const fs = require('fs');
const app = express();


app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// ADD THIS
var cors = require('cors');
app.use(cors());

app.post('/api/video', (req, res) => {

    console.log(req.body)

    fs.writeFileSync('config-video.json', JSON.stringify(req.body));


    const scriptRun = "python /home/pi/projekt/picam/record.py " + req.body.fps + " " + req.body.length + " " + req.body.slowdown

    exec(scriptRun, (err, stdout, stderr) => {
        if (err) {
            console.error(err);
            return;
        }
    });

    res.json({ status: "ok" })
});

app.listen(5000, () => console.log('PiCam camera node listening on port 5000!'));
