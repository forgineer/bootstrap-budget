/**
 * Name: bootstrap-setup.js
 * Purpose: Initialize the Bootstrap-Budget DB, configurations, and services
 * Author: Blake Phillips (forgineer)
 */
var fs = require('fs');
var os = require('os');
var path = require('path');


var curDate = new Date();
var curTime = curDate.getTime();
var curIso = curDate.toISOString();


console.log("DIR Name --> " + __dirname);
console.log("OS Type --> " + os.type);
console.log("curDate --> " + curDate);
console.log("curTime --> " + curTime);
console.log("curIso --> " + curIso);



// Check to see if the setup configuration (JSON) file eixsts
// If exists, retrieve the setup object
try {
    if(fs.existsSync(__dirname + "/bootstrap-setup.json")) {
        console.log("bootstrap-setup.json exists in setup dir.");

        data = fs.readFileSync(__dirname + "/bootstrap-setup.json", { encoding:"utf8", flag:"r" },
            function(err, data) { if(err) { console.log(err); } }
        );
        
        var setupObj = JSON.parse(data);
        
        //console.log(data);
        //console.log(setupObj.admin_password);

    } else {
        console.log("bootstrap-setup.json does NOT exists in setup dir. Exiting...");
        process.exit(0);
    }

} catch (err) {
    console.error(err);
}


// Define prepared CREATE statements
var tableBuildList = [
    "CREATE_ACCOUNT_TABLE.sql"
    , "CREATE_BUDGET_ITEM_TABLE.sql"
    , "CREATE_CONFIG_TABLE.sql"
    , "CREATE_TRANSACTION_TABLE.sql"
    , "CREATE_USER_TABLE.sql"
];

if(setupObj.db_server == "sqlite") {
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