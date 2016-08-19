var express = require('express');
var bodyParser = require('body-parser');
var distance = require('google-distance');
var db = require('./db.js');

var app = express();
var server = require('http').createServer(app);
distance.apiKey = 'AIzaSyBSA_hN9-v-wGyRwvXHNSuk7DxTCSnOpbM';

app.use(bodyParser.json());
app.use(express.static('public'));

var data = {};

app.get('/', function (req, res) {
  res.status(200).send('Welcome');
});

//GET Request for latLng.
app.get('/location/', function (req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.send(data);

}, function (e) {
  res.status(400).json(e);
});

// POST request for latLng.
app.post('/location/', function (req, res) {
  if (req.body.flag) {
    data.sensorID = req.body.sensorID;
    data.lat = req.body.lat;
    data.lng = req.body.lng;
    data.time = req.body.time;
    data.date = req.body.date;

    if (isNaN(data.lat))
      data.lat = JSON.parse(data.lat(/\bNaN\b/g, "null"));

    if (isNaN(data.lng))
      data.lng = JSON.parse(data.lng(/\bNaN\b/g, "null"));

    console.log(JSON.stringify(data, undefined, 2));

    // INSERT data in waypoints table. 
    db.wayPoints.create(data).then(function (wayPoint) {
      res.json(wayPoint.toJSON());
    }, function (e) {
      res.status(400).json(e);
    });
  }

  // When transmission is ended by GPS.
  else {
    console.log('Flag: ' + req.body.flag);

    // Last (lat, lng) for in the database.
    db.wayPoints.max('id').then(function (lastID) {
      db.wayPoints.findOne({ where: { id: lastID } }).
        then(function (wayPointLast) {

          // Initial (lat, lng) for in the database.
          db.wayPoints.findOne({ where: { id: 1 } }).
            then(function (wayPointFirst) {

              // Calculate distance covered for the whole day. 
              distance.get(
                {
                  index: 1,
                  origin: wayPointFirst.lat + ', ' + wayPointFirst.lng,
                  destination: wayPointLast.lat + ', ' + wayPointLast.lng,
                  sensor: true
                },
                function (err, data) {
                  if (err) return console.log(err);
                  console.log('Distance covered since the GPS went on: ' + data.distance);
                });
            });
        });
    });
    res.status(200).send('Flag received');
  }
});

db.database.sync({ force: true }).then(function () {
  server.listen(8000, '127.0.0.1', function () {
    server.close(function () {
      server.listen(8001, '192.168.0.199');
      console.log('Server running on 192.168.0.199');
    });
  });
});