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
 const nets = os.networkInterfaces();
 //console.log(JSON.stringify(nets));
 
 
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

 var configPath = path.join(__dirname, "../data")
 console.log(configPath);

 // Get Config
 const sqlite3 = require('sqlite3').verbose();
    
 var db = new sqlite3.Database(path.join(__dirname, "../data/BOOTSTRAP"));

 

 
 // Setup - Main
 service.get('/bootstrap/setup', function (req, res) {
     res.set('Content-Type', 'application/json');
 
     if(fs.existsSync(path.join(__dirname, "../data/BOOTSTRAP"))) {
         res.status(200).json( {'setup': true} );
     } else {
         res.status(200).json( {'setup': false} );
     }
 })
 
 
 // Bootstrap Setup Service
 var setup = service.listen(8081);