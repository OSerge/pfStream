"use strict";

document.addEventListener("DOMContentLoaded", (e) => {
    const socketAddr = 'http://' + document.domain + (location.port ? ':' + location.port : '') + '/logs',
          socket = io.connect(socketAddr, {secure:false});
    let logCount = 0,
        rowCount = 0,
        rowColorCount = 0,
        rowMax = 200,
        append = true,
        log = null,
        sourceIP = null,
        sourcePort = null,
        destIP = null,
        destPort = null,
        any_substring = null,
        startButton = document.getElementById("start-button"),
        stopButton = document.getElementById("stop-button"),
        cleanButton = document.getElementById("clean-button");


    socket.on('connect', () => {
        stopButton.removeAttribute("disabled");
        stopButton.style.cursor = "pointer";
        startButton.setAttribute("disabled", "disabled");
        startButton.style.cursor = "not-allowed";
    })

    socket.on('disconnect', () => {
        stopButton.setAttribute("disabled", "disabled");
        stopButton.style.cursor = "not-allowed";
        startButton.removeAttribute("disabled");
        startButton.style.cursor = "pointer";
    })

    socket.emit('connect');

    socket.on('info_msg', (msg) => {
        console.log(msg.data);
    });

    socket.on('log', (msg) => {
        log = JSON.parse(msg.data);
        // console.log(log);
        logCount += 1;
        append = true;
        sourceIP = document.getElementById("sourceIP").value;
        sourcePort = document.getElementById("sourcePort").value;
        destIP = document.getElementById("destIP").value;
        destPort = document.getElementById("destPort").value;
        any_substring = document.getElementById("any_substring").value;

        if (log.protocol === null) {
            append = false;
        } else if (sourceIP !== '' && log.source != null && !log.source.includes(sourceIP)) {
            append = false;
        } else if (sourcePort !== '' && log.source_port != null && log.source_port !== sourcePort) {
            append = false;
        } else if (destIP !== '' && log.destination != null && !log.destination.includes(destIP)) {
            append = false;
        } else if (destPort !== '' && log.destination_port != null && log.destination_port !== destPort) {
            append = false;
        } else if (any_substring !== '' && !msg.data.includes(any_substring)) {
            append = false;
        } else if ( document.getElementById("TCPTransport").checked && log.protocol !== 'tcp') {
            append = false;
        } else if ( document.getElementById("UDPTransport").checked && log.protocol !== 'udp') {
            append = false;
        }
        if (append === true) {
            rowColorCount += 1;
            document.getElementById('log-body').insertAdjacentHTML('beforeend',
                `<tr class="${log.action} ${(rowColorCount % 2 === 0 ? 'grey-row' : '')}"><td>` +
                logCount +
                '. </td><td>' +
                log.action +
                '</td><td>' +
                log.protocol +
                '</td><td>' +
                log.source + ':' + log.source_port +
                '</td><td>' +
                log.destination + ':' + log.destination_port +
                '</td><td>' +
                log.interface +
                '</td><td>' +
                log.direction +
                '</td><td>' +
                log.rule +
                '</td></tr>');
            rowCount += 1;
        }
        if (rowCount > rowMax) {
            document.getElementById("log-body").deleteRow(0);
            rowCount = rowMax;
        }
        let scrollDiv = document.getElementById("log-container");
        scrollDiv.scrollTop = scrollDiv.scrollHeight;
        return false;
    });

    startButton.onclick = () => {
        socket.connect();
        return false;
    };

    stopButton.onclick = () => {
        socket.disconnect();
        return false;
    };

    cleanButton.onclick = () => {
        document.getElementById('log-body').innerHTML = '';
        rowCount = 0;
        logCount = 0;
        rowColorCount = 0;
        return false;
    };
});