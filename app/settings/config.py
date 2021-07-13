#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

SECRET_KEY = None
if os.getenv('SECRET_KEY'):
    SECRET_KEY = os.getenv('SECRET_KEY')
else:
    print("""
    Please, set the SECRET_KEY environment variable:\n
    export SECRET_KEY='<secret_key_value>'.\n
    You can put the command to your '~/.bashrc' file (or virtualenv 'activate' script) 
    for a permanent effect.\n
    Use the 'openssl rand -base64 24' command to generate a secure secret key.
    """)
    exit(1)

# The name or IP address of this server
# for listening on incoming HTTP(S) and WebSocket connections.
SERVER_HOST = os.getenv('HOST', '0.0.0.0')

HTTP_SERVER_PORT = os.getenv('HTTP_SERVER_PORT', 5000)

# A pfSense instance IP-address for listening on incoming filterlog messages
PFSENSE_HOST = os.getenv('PFSENSE_HOST', '0.0.0.0')

# The port number for listening on incoming pfSense filterlog messages
FILTERLOG_SERVER_PORT = os.getenv('FILTERLOG_SERVER_PORT', 1514)

# To display debug messages of the flask-socketio server, change the value to True
DEBUG = os.getenv('DEBUG', False)

# The PFSENSE_FILTERLOG_STRUCT is used to parse pfSense firewall syslog messages.
#
# A typical pfSense firewall message looks like this:
# '<134>Jul 12 13:45:28 filterlog: 214,,,1000037315,vtnet2,match,pass,out,4,0x0,,120,7521,0,none,6,tcp,5
# 2,95.173.153.210,178.154.131.216,27308,443,0,S,772281041,,64240,,mss;nop;wscale;nop;nop;sackOK'
PFSENSE_FILTERLOG_STRUCT = [
        'rule',
        'sub_rule',
        'anchor',
        'tracker',
        'interface',
        'reason',
        'action',
        'direction',
        'ip_ver',
        'tos',
        'ecn',
        'ttl',
        'id',
        'offset',
        'flags',
        'protocol_id',
        'protocol',
        'length',
        'source',
        'destination',
        'source_port',
        'destination_port',
        'data_length',
        'tcp_flags',
        'seq_number',
        'ack',
        'window',
        'urg',
        'options',
    ]
