/**
 * Name: bootstrap-web-setup.js
 * Purpose: Initialize the Bootstrap-Budget DB and Configurations over Web
 * Author: Blake Phillips (forgineer)
 */
const bcrypt = require('bcrypt');
const cors = require('cors');
const express = require('express');
const fs = require('fs');
const http = require('http');
const os = require('os');
const path = require('path');


// Capture local IP addresses (best attempt anyway...)
const osType = os.type();
const osHostname = os.hostname();   // TODO: Using hostname over IP address
const nets = os.networkInterfaces();
//console.log("osType -> " + osType);
//console.log("osHostname -> " + osHostname);
//console.log(JSON.stringify(nets));

const interfaces = Object.create(null); // Or just '{}', an empty object
let address;

for(const name of Object.keys(nets)) {
    for(const net of nets[name]) {
        // Skip over non-IPv4 and internal (i.e. 127.0.0.1) addresses
        if(net.family === 'IPv4' && !net.internal) {
            if(!interfaces[name]) {
                interfaces[name] = [];
            }
            interfaces[name].push(net.address);
        }
    }
}

//console.log(interfaces);

// Set localhost IP address
if(osType.includes("Windows")) {
    if("Ethernet" in interfaces) {
        address = interfaces["Ethernet"][0];
    } else if("Wi-Fi" in interfaces) {
        address = interfaces["Wi-Fi"][0];
    } else {
        address = "localhost"
    }
} else {    // TODO: Linux hosts
    address = "localhost"
}


// Table SQL scripts
var tableBuildList = [
    "CREATE_ACCOUNT_TABLE.sql"
    , "CREATE_BUDGET_ITEM_TABLE.sql"
    , "CREATE_BUDGET_TABLE.sql"
    , "CREATE_CONFIG_TABLE.sql"
    , "CREATE_DASHBOARD_TABLE.sql"
    , "CREATE_TRANSACTION_TABLE.sql"
    , "CREATE_USER_TABLE.sql"
    , "CREATE_USER_BUDGET_TABLE.sql"
];


/**
 * Setup API Service
 */

// Create Service
var service = express();

// Required to read POST objects
service.use(express.json());
service.use(express.urlencoded({extended: false}));

// Enable Cross Origin
service.use(cors());
service.options('*', cors());

// Setup - Main
service.get('/bootstrap/setup', function (req, res) {
    res.set('Content-Type', 'application/json');

    if(fs.existsSync(path.join(__dirname, "../data/BOOTSTRAP"))) {
        res.status(200).json( {'setup': true, 'hostname': osHostname} );
    } else {
        res.status(200).json( {'setup': false} );
    }
})

// Setup - SQLite DB
service.post('/bootstrap/setup/sqlite', function (req, res) {
    const sqlite3 = require('sqlite3').verbose();
    
    var db = new sqlite3.Database(path.join(__dirname, "../data/BOOTSTRAP"));
    
    let adminId;
    
    var curDate = new Date();
    var curTime = curDate.getTime();
    var curIso = curDate.toISOString();


    // Add OS Type to config (request) object
    req.body.os_type = osType;


    function setAdminId(id) {
        adminId = id;
        delete req.body.admin_password;
    }


    function createTables() {
        var createAction;

        for(table in tableBuildList) {
            if(fs.existsSync(path.join(__dirname, "../data/sql/sqlite", tableBuildList[table]))) {
                createAction = tableBuildList[table].split(".");
                console.log(createAction[0]);
            
                var sql = fs.readFileSync(path.join(__dirname, "../data/sql/sqlite", tableBuildList[table]), { encoding:'utf8', flag:'r' },
                    function(err, sql) { if(err) { console.log(err); } }
                );
    
                db.serialize(function() { db.run(sql) });
                
            } else {
                console.log(tableBuildList[table] + " does NOT exists in sql dir. Exiting...");
            }
        }

        setTimeout(function() { adminConfig(); }, 1000);
    }


    function adminConfig() {
        if(fs.existsSync(path.join(__dirname, "../data/sql/sqlite/INSERT_USER.sql"))) {
            console.log("Posting ADMIN account...");

            var sql = fs.readFileSync(path.join(__dirname, "../data/sql/sqlite/INSERT_USER.sql"), { encoding:'utf8', flag:'r' },
                function(err, sql) { if(err) { console.log(err); } }
            );
    
            req.body.salt = bcrypt.genSaltSync(10);
            req.body.hash = bcrypt.hashSync(req.body.admin_password, req.body.salt);

            db.serialize(function() {
                db.run(sql, 'ADMIN', 'ADMIN', '', 'ADMIN', '', '', '', '', '', '', '', req.body.hash, req.body.salt, 0, 1, curTime, curIso, curTime, curIso, 1, 
                    function(err) {
                        setAdminId(this.lastID);
                    }
                );
            });

        } else {
            console.log("INSERT_USER.sql does NOT exists in sql dir. Exiting...");
        }

        setTimeout(function() { postConfig(adminId); }, 1000);
    }


    function postConfig(adminId) {
        if(fs.existsSync(path.join(__dirname, "../data/sql/sqlite/INSERT_CONFIG.sql"))) {
            console.log("Posting CONFIG...");

            var sql = fs.readFileSync(path.join(__dirname, "../data/sql/sqlite/INSERT_CONFIG.sql"), { encoding:'utf8', flag:'r' },
                function(err, sql) { if(err) { console.log(err); } }
            );
    
            db.serialize(function() { 
                //(config_text, config_value_int, config_value_flt, config_value_txt, config_value_set, user_id, create_dt_tm, create_iso_ts, updt_dt_tm, updt_iso_ts, active_ind)

                for(const [key, value] of Object.entries(req.body)) {
                    //console.log(`${key}: ${value}`);
                    db.run(sql, `${key}`, 0, 0, `${value}`, 3, adminId, curTime, curIso, curTime, curIso, 1);
                  }
            });

            setTimeout(function() {
                console.log("...Finished!");

                db.close();
                res.set('Content-Type', 'application/json');
                res.status(200).json( {'setup': true} );
            }, 1000);
    
        } else {
            console.log("INSERT_CONFIG.sql does NOT exists in sql dir. Exiting...");
        }
    }

    // TODO: Setup HTML pages (replace host:port)
    // TODO: Setup web service (if any)

    createTables(); // Start
})

// Setup - MariaDB DB
service.post('/bootstrap/setup/mariadb', function (req, res) {
    var curDate = new Date();
    var curTime = curDate.getTime();
    var curIso = curDate.toISOString();

    res.status(200).json({'mariadb': curIso});
})

// Start Over
service.post('/bootstrap/startover', function (req, res) {
    res.set('Content-Type', 'application/json');

    let hash;

    if(fs.existsSync(path.join(__dirname, "../data/BOOTSTRAP"))) {
        const sqlite3 = require('sqlite3').verbose();
        var db = new sqlite3.Database(path.join(__dirname, "../data/BOOTSTRAP"), sqlite3.OPEN_READONLY);

        db.serialize(function() {
            db.each("SELECT config_text, config_value_txt FROM CONFIG WHERE config_text = 'hash'", function(err, row) {
                //console.log(row.config_text + ": " + row.config_value_txt);

                if(err) { res.status(200).json({'startover': false}); }

                hash = row.config_value_txt;
            });
        });

        setTimeout(function() {
            db.close();

            //console.log(hash);
            //console.log(JSON.stringify(req.body));

            bcrypt.compare(req.body.admin_password, hash, function(err, result) {
                if(result) {
                    fs.unlinkSync(path.join(__dirname, "../data/BOOTSTRAP"))
                    res.status(200).json({'startover': true}); 
                } else {
                    res.status(200).json({'startover': false});
                }
            });
        }, 1000);

    } else {
        res.status(200).json({'startover': false});
    }
})

// Bootstrap Setup Service
var setup = service.listen(8081);




/**
 * Setup Web Service
 */

// Bootstrap Setup Web Service
http.createServer(function (req, res) {

    // Read the requested file content from file system
    fs.readFile(path.join(__dirname, "/bootstrap-web-setup.html"), function (err, data) {
        if(err) {
            console.log(err);
            // HTTP Status: 404 : NOT FOUND
            // Content Type: text/plain
            res.writeHead(404, {'Content-Type': 'text/html'});

        } else {	
            // Page found	  
            // HTTP Status: 200 : OK
            // Content Type: text/plain
            res.writeHead(200, {'Content-Type': 'text/html'});	

            // Write the content of the file to response body
            res.write(data);		
        }

        // Send the response body 
        res.end();
    });

}).listen(8080);


// Console will print the message
console.log("Navigate to http://" + osHostname + ":8080 to complete Bootstrap install.");
console.log("Close service when finished (Ctrl+C).");