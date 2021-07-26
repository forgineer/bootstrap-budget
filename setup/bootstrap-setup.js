/**
 * Name: bootstrap-setup.js
 * Purpose: Initialize the Bootstrap-Budget DB and configurations
 * Author: Blake Phillips (forgineer)
 */

const fs = require('fs');
const os = require('os');
const path = require('path');
const inquirer = require('inquirer');
const bcrypt = require('bcrypt');


var curDate = new Date();
var curTime = curDate.getTime();
var curIso = curDate.toISOString();


let config = {
    "os_type": os.type,
    "db_name": "BOOTSTRAP",
};


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


let bootstrapSetup = new Promise(function(resolve, reject) {

    function setConfigObj(name, value) {
        config[name] = value;
    }

    function inqireDBService() {
        inquirer.prompt(
            {
                type: 'list',
                name: 'db_service',
                message: 'Select your database service:',
                choices: ['SQLite (localhost)', 'MariaDB'],
                filter(val) {
                    if(val == 'SQLite (localhost)') {
                        return 'sqlite';
                    } else {
                        return val.toLowerCase();
                    }
                },
            },
        ).then((answers) => {
            //console.log(answers);
            //console.log(Object.keys(answers)[0]);
            setConfigObj(Object.keys(answers)[0], answers.db_service);

            if(answers.db_service == "sqlite") {
                //console.log(config);
                inqireServices ();
            } else {
                inqireDBAttributes(answers.db_service);
            }
        });
    }


    function inqireDBAttributes(service) {
        var dbPort;
    
        switch(service) {
            case "mariadb":
                dbPort = '3306';
                break;
            case "mysql":
                dbPort = '3306';
                break;
            case "postgresql":
                dbPort = '5432';
                break;
        }

        inquirer.prompt([
            {
                type: 'input',
                name: 'db_username',
                message: 'Enter database admin username:',
            },
            {
                type: 'password',
                name: 'db_password',
                message: 'Enter database admin password:',
            },
            {
                type: 'input',
                name: 'db_address',
                message: 'Enter database address:',
                default: 'localhost',
            },
            {
                type: 'input',
                name: 'db_port',
                message: 'Enter database port:',
                default: dbPort,
            },
        ]).then((answers) => {
            setConfigObj(Object.keys(answers)[0], answers.db_username);
            setConfigObj(Object.keys(answers)[1], answers.db_password);
            setConfigObj(Object.keys(answers)[2], answers.db_address);
            setConfigObj(Object.keys(answers)[3], answers.db_port);

            inqireServices();
        });
    }


    function inqireServices() {
        inquirer.prompt([
            {
                type: 'input',
                name: 'services_address',
                message: 'Enter API services address:',
                default: 'localhost',
            },
            {
                type: 'input',
                name: 'services_port',
                message: 'Enter API services port:',
                default: '8080',
            },
        ]).then((answers) => {
            setConfigObj(Object.keys(answers)[0], answers.services_address);
            setConfigObj(Object.keys(answers)[1], answers.services_port);

            inquireAdmin();
        });
    }


    function inquireAdmin() {
        inquirer.prompt([
            {
                type: 'password',
                name: 'admin_password',
                message: 'Enter Bootstrap administrator password:',
            },
            {
                type: 'password',
                name: 'password_check',
                message: 'Re-enter Bootstrap administrator password:',
            },
        ]).then((answers) => {
            if(answers.admin_password == answers.password_check) {
                setConfigObj(Object.keys(answers)[0], answers.admin_password);
                console.log(JSON.stringify(config, null, '  '));
                resolve();
            } else {
                inquireAdmin();
            }
        });
    }

    inqireDBService();  // Start
}); // End bootstrapSetup


function sqliteSetup() {

    const sqlite3 = require('sqlite3').verbose();
    var db = new sqlite3.Database(path.join(__dirname, "../data/" + config.db_name));
    let adminId;

    createTables(); // Start


    function setAdminId(id) {
        adminId = id;
        console.log("Admin ID: " + adminId);
    }


    function createTables() {
        for(table in tableBuildList) {
            if(fs.existsSync(path.join(__dirname, "../data/sql/sqlite", tableBuildList[table]))) {
                console.log(tableBuildList[table] + " exists. Building...");
            
                var sql = fs.readFileSync(path.join(__dirname, "../data/sql/sqlite", tableBuildList[table]), { encoding:'utf8', flag:'r' },
                    function(err, sql) { if(err) { console.log(err); } }
                );
    
                db.serialize(function() { db.run(sql) });
                
            } else {
                exitWithError(tableBuildList[table] + " does NOT exists in sql dir. Exiting...");
            }
        }

        adminConfig();
    }
    

    function adminConfig() {
        if(fs.existsSync(path.join(__dirname, "../data/sql/sqlite/INSERT_USER.sql"))) {
            var sql = fs.readFileSync(path.join(__dirname, "../data/sql/sqlite/INSERT_USER.sql"), { encoding:'utf8', flag:'r' },
                function(err, sql) { if(err) { console.log(err); } }
            );
    
            const salt = bcrypt.genSaltSync(10);
            const hash = bcrypt.hashSync(config.admin_password, salt);

            db.serialize(function() {
                db.run(sql, 'ADMIN', 'ADMIN', '', 'ADMIN', '', '', '', '', '', '', '', hash, salt, 0, 1, curTime, curIso, curTime, curIso, 1, 
                    function(err) {
                        setAdminId(this.lastID);
                    }
                );
            });

        } else {
            exitWithError("INSERT_USER.sql does NOT exists in sql dir. Exiting...");
        }

        setTimeout(function(){ postConfig(adminId); }, 1000);
    }


    function postConfig(adminId) {
        if(fs.existsSync(path.join(__dirname, "../data/sql/sqlite/INSERT_CONFIG.sql"))) {
            var sql = fs.readFileSync(path.join(__dirname, "../data/sql/sqlite/INSERT_CONFIG.sql"), { encoding:'utf8', flag:'r' },
                function(err, sql) { if(err) { console.log(err); } }
            );
    
            db.serialize(function() { 
                //(config_text, config_value_int, config_value_flt, config_value_txt, config_value_set, user_id, create_dt_tm, create_iso_ts, updt_dt_tm, updt_iso_ts, active_ind)
                db.run(sql, 'os_type', 0, 0, config.os_type, 3, adminId, curTime, curIso, curTime, curIso, 1);
                db.run(sql, 'db_service', 0, 0, config.db_service, 3, adminId, curTime, curIso, curTime, curIso, 1);
                db.run(sql, 'db_name', 0, 0, config.db_name, 3, adminId, curTime, curIso, curTime, curIso, 1);
                if(config.db_service == "sqlite") {
                    db.run(sql, 'db_username', 0, 0, config.db_username, 3, adminId, curTime, curIso, curTime, curIso, 1);
                    db.run(sql, 'db_address', 0, 0, config.db_address, 3, adminId, curTime, curIso, curTime, curIso, 1);
                    db.run(sql, 'db_port', 0, 0, config.db_port, 3, adminId, curTime, curIso, curTime, curIso, 1);
                }
                db.run(sql, 'services_address', 0, 0, config.services_address, 3, adminId, curTime, curIso, curTime, curIso, 1);
                db.run(sql, 'services_port', 0, 0, config.services_port, 3, adminId, curTime, curIso, curTime, curIso, 1);
            });
    
        } else {
            exitWithError("INSERT_CONFIG.sql does NOT exists in sql dir. Exiting...");
        }
    }

    //db.close();

}   // End sqliteSetup


//function mariadbSetup () {}
//function mysqlSetup () {}
//function startServices () {}


function exitWithError(errString) {
    console.log(errString);
    process.exit(0);
}


bootstrapSetup.then(
    function() { sqliteSetup(); },
    function() { console.log("Failed at first step!"); }
);

//console.log("The End!");