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
    var curDate = new Date();
    var curTime = curDate.getTime();
    var curIso = curDate.toISOString();

    res.send('In setup - ' + curIso);
    res.sendStatus(200);
})

// Setup - SQLite DB
service.post('/bootstrap/setup/sqlite', function (req, res) {
    const sqlite3 = require('sqlite3').verbose();
    var db = new sqlite3.Database(path.join(__dirname, "../data/" + req.body.db_name));
    let adminId;

    var curDate = new Date();
    var curTime = curDate.getTime();
    var curIso = curDate.toISOString();


    function setAdminId(id) {
        adminId = id;
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

        setTimeout(function(){ adminConfig(); }, 1000);
    }


    function adminConfig() {
        if(fs.existsSync(path.join(__dirname, "../data/sql/sqlite/INSERT_USER.sql"))) {
            console.log("Posting ADMIN account...");

            var sql = fs.readFileSync(path.join(__dirname, "../data/sql/sqlite/INSERT_USER.sql"), { encoding:'utf8', flag:'r' },
                function(err, sql) { if(err) { console.log(err); } }
            );
    
            const salt = bcrypt.genSaltSync(10);
            const hash = bcrypt.hashSync(req.body.admin_password, salt);

            db.serialize(function() {
                db.run(sql, 'ADMIN', 'ADMIN', '', 'ADMIN', '', '', '', '', '', '', '', hash, salt, 0, 1, curTime, curIso, curTime, curIso, 1, 
                    function(err) {
                        setAdminId(this.lastID);
                    }
                );
            });

        } else {
            console.log("INSERT_USER.sql does NOT exists in sql dir. Exiting...");
        }

        setTimeout(function(){ postConfig(adminId); }, 1000);
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
    
        } else {
            console.log("INSERT_CONFIG.sql does NOT exists in sql dir. Exiting...");
        }

        setTimeout(function() {
            db.close();
            res.set('Content-Type', 'application/json')
            res.status(200).json({'sqlite_time': curIso});
        }, 1000);
    }

    createTables(); // Start


//    res.set('Content-Type', 'application/json')
//    res.status(200).json({'sqlite_time': curIso});
})

// Setup - MariaDB DB
service.post('/bootstrap/setup/mariadb', function (req, res) {
    var curDate = new Date();
    var curTime = curDate.getTime();
    var curIso = curDate.toISOString();

    res.send('In mariadb - ' + curIso);
    res.sendStatus(200);
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
console.log("Bootstrap Setup micro-service listening at http://localhost:8081/bootstrap/setup")
console.log('Navigate to http://localhost:8080/bootstrap-web-setup.html to complete Bootstrap install');