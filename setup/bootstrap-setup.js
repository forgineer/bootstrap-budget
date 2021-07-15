/**
 * Name: bootstrap-setup.js
 * Purpose: Initialize the Bootstrap-Budget DB and configurations
 * Author: Blake Phillips (forgineer)
 */

var fs = require('fs');
var os = require('os');
var path = require('path');
var readline = require('readline');

var curDate = new Date();
var curTime = curDate.getTime();
var curIso = curDate.toISOString();


console.log("DIR Name --> " + __dirname);
console.log("OS Type --> " + os.type);
console.log("curDate --> " + curDate);
console.log("curTime --> " + curTime);
console.log("curIso --> " + curIso);

// Main setup object
var setupObj = {
    // Database Server
    "db_service": "sqlite"
    , "db_name": "BOOTSTRAP"
    , "db_username": "usern@me"
    , "db_password": "passwd"
    , "db_address": "localhost"
    , "db_port": "9999"

    // API Services
    , "service_username": "usern@me"
    , "service_password": "passwd"
    , "service_address": "localhost"
    , "service_port": "8081"

    // Administration Configuration
    , "admin_password": "bootstrap"
}


// Define acceptable SQL server list
var dbServerList = ["SQLITE", "MARIADB"];


// Define prepared CREATE statements
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


// Define readline interface
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});


// 
function exitError(errString) {
    console.log(errString);
    process.exit(0);
}


/*
    Setup Questions / Answers
*/
rl.question('Define your SQL service (sqlite or mariadb): ', (answer) => {
    if (answer.length > 0 && dbServerList.includes(answer.toUpperCase)) {
        setupObj.db_service = answer;
    } else {
        exitError("Specified database server is unsupported. Exiting...");
    }

    rl.close();
});

if(setupObj.db_service.toUpperCase != "SQLITE") {

}




if(setupObj.db_server.toUpperCase == "SQLITE") {
    var sqlite3 = require('sqlite3').verbose();
    var db = new sqlite3.Database(path.join(__dirname, "../data/" + setupObj.db_name));    // TODO: Change to bootstrap.db

    try {
        for(table in tableBuildList) {
            if(fs.existsSync(path.join(__dirname, "../data/sql/sqlite", tableBuildList[table]))) {
                console.log(tableBuildList[table] + " exists. Building...");
        
                data = fs.readFileSync(path.join(__dirname, "../data/sql/sqlite", tableBuildList[table]), { encoding:'utf8', flag:'r' },
                    function(err, data) { if(err) { console.log(err); } }
                );
    
                //console.log(data);

                db.serialize(function() { db.run(data); });
            
            } else {
                console.log(tableBuildList[table] + " does NOT exists in sql dir. Exiting...");
                process.exit(0);
            }
        }

        if(fs.existsSync(path.join(__dirname, "../data/sql/sqlite/INSERT_USER.sql"))) {
            data = fs.readFileSync(path.join(__dirname, "../data/sql/sqlite/INSERT_USER.sql"), { encoding:'utf8', flag:'r' },
                function(err, data) { if(err) { console.log(err); } }
            );
            
            var stmt = db.prepare(data);
            stmt.run("ADMIN", "ADMIN", "", "ADMIN", "", "", "", "", "", "", "", 1, "", "", curTime, curIso, 1);
            stmt.finalize();

        } else {
            console.log("INSERT_USER.sql does NOT exists in sql dir. Exiting...");
            process.exit(0);
        }

    } catch (err) {
        console.error(err);
    }

    db.close();
}


console.log("The End!");