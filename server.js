var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var server = require('http').createServer(app);

app.use(bodyParser.json());
app.use(express.static('public'));

var data = {};

//GET Request for latLng.
app.get('/location', function (req, res){
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.send(data);
  
}, function (e) {
  res.status(400).json(e);
});

// POST request for latLng.
app.post('/location/', function (req, res) {
  data.lat = req.body.lat;
  data.lng = req.body.lng;

  if (isNaN(data.lat))
    data.lat = JSON.parse(data.lat(/\bNaN\b/g, "null"));

  if(isNaN(data.lng))
    data.lng = JSON.parse(data.lng(/\bNaN\b/g, "null"));

  console.log('(lat, lng): (' +data.lat+', '+data.lng+')');
  
  res.status(200).send('Data Received');

}, function (e) {
  res.status(400).send();
});

server.listen(8000,'127.0.0.1',function(){
 server.close(function(){
   server.listen(8001,'192.168.0.199');
   console.log('Server running on 192.168.0.199');
 });
});