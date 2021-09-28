/**
 * Name: bootstrap-cli-setup.js
 * Purpose: Initialize the Bootstrap-Budget DB and Configurations over CLI
 * Author: Blake Phillips (forgineer)
 */
const bcrypt = require('bcrypt');
const fs = require('fs');
const inquirer = require('inquirer');
const os = require('os');
const path = require('path');


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

// TODO: Uplift from web install
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
            //setConfigObj(Object.keys(answers)[0], answers.db_service);
            config.db_service = answers.db_service;

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
            //setConfigObj(Object.keys(answers)[0], answers.db_username);
            //setConfigObj(Object.keys(answers)[1], answers.db_password);
            //setConfigObj(Object.keys(answers)[2], answers.db_address);
            //setConfigObj(Object.keys(answers)[3], answers.db_port);
            config.db_username = answers.db_username;
            config.db_password = answers.db_password;
            config.db_address = answers.db_address;
            config.db_port = answers.db_port;

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
            //setConfigObj(Object.keys(answers)[0], answers.services_address);
            //setConfigObj(Object.keys(answers)[1], answers.services_port);
            config.services_address = answers.services_address;
            config.services_port = answers.services_port;

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
                //setConfigObj(Object.keys(answers)[0], answers.admin_password);
                config.admin_password = answers.admin_password;
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


    function setAdminId(id) {
        adminId = id;
        //console.log("Admin ID: " + adminId);
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
            const hash = bcrypt.hashSync(config.admin_password, salt);

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

                for (const [key, value] of Object.entries(config)) {
                    //console.log(`${key}: ${value}`);
                    db.run(sql, `${key}`, 0, 0, `${value}`, 3, adminId, curTime, curIso, curTime, curIso, 1);
                  }
            });
    
        } else {
            console.log("INSERT_CONFIG.sql does NOT exists in sql dir. Exiting...");
        }

        setTimeout(function(){ db.close(); console.log("The End!"); }, 1000);
    }

    createTables(); // Start

};   // End sqliteSetup


bootstrapSetup.then(    // Start Setup
    function() { sqliteSetup(); },
    function(err) { console.log(err) }
);