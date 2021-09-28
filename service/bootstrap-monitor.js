const forever = require('forever-monitor');
const path = require('path');

var monArgs = process.argv.slice(2);
var jSourceDir = "";

var jSourceDir = path.join(__dirname, "../service");

var jService = monArgs[0]
var jConfig = {
    //
    // Basic configuration options
    //
    'silent': false,            // Silences the output from stdout and stderr in the parent process
    'uid': 'your-UID',          // Custom uid for this forever process. (default: autogen)
    'pidFile': 'path/to/a.pid', // Path to put pid information for the process(es) started
    'max': 10,                  // Sets the maximum number of times a given script should run
    'killTree': true,           // Kills the entire child process tree on `exit`

    //
    // Command to spawn as well as options and other vars
    // (env, cwd, etc) to pass along
    //
    'args':    ['foo','bar'],  // Additional arguments to pass to the script,
    'sourceDir': 'script/path',// Directory that the source script is in

    //
    // Options for restarting on watched files.
    //
    'watch': true,               // Value indicating if we should watch files.
    'watchIgnoreDotFiles': null, // Whether to ignore file starting with a '.'
    'watchIgnorePatterns': null, // Ignore patterns to use when watching files.
    'watchDirectory': null,      // Top-level directory to watch from. You can provide multiple watchDirectory options to watch multiple directories (e.g. for cli: forever start -w='app' -w='some_other_directory' app\index.js)

    //
    // Log files and associated logging options for this instance
    //
    'logFile': 'path/to/file', // Path to log output from forever process (when daemonized)
    'outFile': 'path/to/file', // Path to log output from child stdout
    'errFile': 'path/to/file', // Path to log output from child stderr
}

var child = new (forever.Monitor)(jService, jConfig);

child.on('exit', function () {
  console.log('your-filename.js has exited after 3 restarts');
});

child.start();