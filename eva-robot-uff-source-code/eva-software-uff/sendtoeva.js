let low = require('lowdb'),
FileSync = require('lowdb/adapters/FileSync'),
adapter = new FileSync('db.json'),
db = low(adapter);
db.defaults({script: [], scriptdata: [], interaccion: [], voice: [], led: [], mov: [], woo: []}).write();
