/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
var fs = require('fs'); // Include the 'fs' (File System) module

fs.readFile('../../files/transactions.csv', 'utf8', function(err, data) {
   console.log(data);
});