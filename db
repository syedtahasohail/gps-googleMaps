var Sequelize = require('sequelize');
var db = new Sequelize(undefined, undefined, undefined, {
    dialect: 'sqlite',
    storage: './data/database.sqlite',
    typeValidation: true
});
var wayPoints = db.import('./models/waypoints.js');

module.exports.database = db;
module.exports.wayPoints = wayPoints;
module.exports.Sequelize = Sequelize;