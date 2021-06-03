/**
 * Name: bootstrap-setup.js
 * Purpose: Initialize the Bootstrap-Budget DB, configurations, and services
 * Author: Blake Phillips (forgineer)
 */
var fs = require('fs'); // Include the 'fs' (File System) module
var sqlite3 = require('sqlite3').verbose();


var tableBuildList = [
    "CREATE_ACCOUNT_TABLE.sql"
//    , "CREATE_CONFIG_TABLE.sql"
//    , "CREATE_DASHBOARD_TABLE"
    , "CREATE_TRANSACTION_TABLE.sql"
//    , "CREATE_TRANSLATION_TABLE.sql"
    , "CREATE_USER_TABLE.sql"
];


// Check to see if the setup configuration (JSON) file eixsts
// If exists, retrieve the setup object
try {
    if(fs.existsSync(__dirname + "/bootstrap-setup.json")) {
        console.log("bootstrap-setup.json exists in setup dir.");

        data = fs.readFileSync(__dirname + "/bootstrap-setup.json", {encoding:"utf8", flag:"r"},
            function(err, data) {if(err) { console.log(err); }}
        );
        
        var setupObj = JSON.parse(data);
        
        //console.log(data);
        //console.log(setupObj.admin_password);
        //console.log(setupObj.local_db_dir);

    } else {
        console.log("bootstrap-setup.json does NOT exists in setup dir. Exiting...");
        process.exit(0);
    }

} catch (err) {
    console.error(err);
}


// Check for prepared statements of each table and create them
var db = new sqlite3.Database('../test/testdb.db');

try {
    for(table in tableBuildList) {
        if(fs.existsSync("../data/sql/" + tableBuildList[table])) {
            console.log(tableBuildList[table] + " exists. Building...");
    
            data = fs.readFileSync("../data/sql/" + tableBuildList[table], {encoding:'utf8', flag:'r'},
                function(err, data) { if(err) { console.log(err); } }
            );

            //console.log(data);

            db.serialize(function() { db.run(data); });
        
        } else {
            console.log(tableBuildList[table] + " does NOT exists in sql dir. Exiting...");
            process.exit(0);
        }
    }

} catch (err) {
    console.error(err);
}

db.close();


// 



console.log("hello!");

//var db = new sqlite3.Database('');