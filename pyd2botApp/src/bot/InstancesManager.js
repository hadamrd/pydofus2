const path = require('path');
const child_process = require('child_process');
const process = require('process');
const thrift = require('thrift');
const Pyd2botService = require('../pyd2botService/Pyd2botService.js');
const ejse = require('ejs-electron')

class InstancesManager {

    // this class manages the running instances of pyd2bot
    static get instance() {
        return InstancesManager._instance || (InstancesManager._instance = new InstancesManager()), InstancesManager._instance
    }

    constructor() {
        this.pyd2botExePath = path.join(process.env.AppData, 'pyd2bot', 'pyd2bot.exe');
        this.runningInstances = {};
        this.freePorts = Array(100).fill().map((element, index) => index + 9999);
        this.wantsToKillServer = {};
        this.wantsToKillClient = {};
        ejse.data('runningInstances', this.runningInstances);
    }

    spawnClient(instanceId) {
        var inst = this.runningInstances[instanceId];
        var transport = thrift.TBufferedTransport;
        var protocol = thrift.TBinaryProtocol;
        var connection = thrift.createConnection("127.0.0.1", inst.port, {
            transport : transport,
            protocol : protocol
        });
        connection.on('error', function(err) {
            if (this.wantsToKillClient[instanceId]) {
                this.wantsToKillClient[instanceId] = false;
            }
            else {
                console.log("Error in client : " + err);
            }
        });
        var client = thrift.createClient(Pyd2botService, connection);
        if (inst.connection) {
            this.wantsToKillClient[instanceId] = true;
            inst.connection.end();
        }
        inst.connection = connection;
        inst.client = client;
        return client;
    }

    spawnServer(instanceId) {
        var port = this.freePorts.pop();
        var instance = child_process.execFile(this.pyd2botExePath, ['--host', '0.0.0.0', '--port', port],
            (error, stdout, stderr) => {
                if (error) {
                    if (this.wantsToKillServer[instanceId]) {
                        this.wantsToKillServer[instanceId] = false;
                    }
                    else {
                        console.log("Error while spawning server : " + error);
                    }
                }
                if (stdout) {
                    console.log("Server stdout : " + stdout);
                }
                if (stderr) {
                    if (this.wantsToKillServer[instanceId]) {
                        this.wantsToKillServer[instanceId] = false;
                    }
                    else {
                        console.log("Server stderr : " + stderr);
                    }
                }
            }
        );
        this.runningInstances[instanceId] = {"port": port, "server" : instance, "client" : null, "connection" : null};
        return instance
    }

    clear() {
        for (var instanceId in this.runningInstances) {
            this.killInstance(instanceId);
        }
    }

    killInstance(instanceId) {
        if (this.runningInstances[instanceId]) {
            
            
            var i = this.runningInstances[instanceId]
            if (i.connection) {
                console.log("Killing client for instance " + instanceId);
                this.wantsToKillClient[instanceId] = true;
                i.connection.end();
            }
            if (i.server) {
                console.log("Killing server for instance " + instanceId);
                this.wantsToKillServer[instanceId] = true;
                i.server.kill()
            }
            this.freePorts.push(i.port);
            delete this.runningInstances[instanceId];
        }
    }

}

module.exports = InstancesManager;