#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import eventlet
eventlet.monkey_patch()

import json
import signal
import socket
import threading

from io import BytesIO
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

from settings import config  # noqa


app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
socketio = SocketIO(app, async_mode='eventlet')

emit_thread = None          # The instance of the emitting thread
stop_thread = False         # The flag that stops the emit_thread


def _signal_handler(signum, stack_frame):
    global stop_thread
    stop_thread = True
    if emit_thread.is_alive():
        emit_thread.join()
    socketio.stop()
    exit(0)

# Intercepting a SIGTERM signal correctly
signal.signal(signal.SIGTERM, _signal_handler)


def _emit_filterlog_messages(id, stop_thread_func):
    """
    The function receives the syslog (filterlog) messages from the pfSense
    instances and emit them via the WebSocket protocol to browser clients.

    :param id: the thread id.
    :param stop_thread_func: the function that returns the stop_thread flag value.
    """

    # Creating the UDP socket for listening on incoming pfSense syslog messages
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((config.PFSENSE_HOST, config.FILTERLOG_SERVER_PORT))

    while not stop_thread_func():
        data, _ = sock.recvfrom(1024)  # 1024 is the buffer size
        log_string = BytesIO(data).getvalue().decode('utf-8')
        if "filterlog" not in log_string:
            continue
        log_values = log_string.split("filterlog: ")[-1].split(",")
        log_json = json.dumps(
            dict(zip(config.PFSENSE_FILTERLOG_STRUCT, log_values))
        )
        socketio.emit('log', {'data': log_json}, namespace="/logs")
        eventlet.sleep(0.01)

    sock.close()
    socketio.emit("info_msg", {"data": "Thread stopped.", "type": "info"},
                  namespace="/logs")


@socketio.on('connect', namespace='/logs')
def connect():
    global emit_thread
    if emit_thread.is_alive():
        socketio.emit(
            "info_msg", {
                "data": "Connected to server. Emitting thread has been started.",
                "type": "info"
            },
            namespace="/logs"
        )


@app.route("/")
def stream():
    return render_template("stream.html")


@app.route("/favicon.ico")
def send_favicon():
    return send_from_directory("static", "favicon.ico")


if __name__ == "__main__":
    try:
        emit_thread = threading.Thread(target=_emit_filterlog_messages,
                                       args=(id, lambda: stop_thread))
        emit_thread.start()
        socketio.run(
            app,
            host=config.SERVER_HOST,
            port=config.HTTP_SERVER_PORT,
            debug=config.DEBUG
        )
    except KeyboardInterrupt:
        stop_thread = True
        emit_thread.join()
        socketio.stop()
        exit(0)
