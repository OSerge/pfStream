# pfStream—Getting the pfSense TCP/IP packets info in real time.

pfStream is a compact Python/Flask-based application that collects syslog messages 
from the pfSense firewall, parses and forwards them using the WebSocket protocol
to browser clients for fast monitoring and filtering.

This works as shown in the graphic below.

![](app/static/pfstream_works.gif)


## Prerequisites

The application tested with:
- Ubuntu 20.04 
- python 3.8

It will most likely work on any Debian-based distributions with a python ≥ 3.6 without any issues.

## Installation

Install the python interpreter if you need it:
```
sudo apt-get install python=3.8
``` 

Go to the directory where you intend to clone the repository and run the following command:
```
git clone https://github.com/OSerge/pfStream.git
cd ./pfstream
```

This will create the `pfstream` directory, which will contain all the necessary application files.

### Virtual environment

Next, you need to create a virtual environment and install all the app dependencies in it.

Do the following:
```
python3 -m venv ~/.envs/pfstream
source ~/.envs/pfstream/bin/activate
pip install -r requirements.txt
```

### Configuration

Create the SECRET_KEY environment variable and put it in the `~/.bashrc` file or in the `activate` virtual environment script.

For example, you can do the following:
```
KEY=$(openssl rand -base64 24) && \
export SECRET_KEY=$KEY && \
echo "export SECRET_KEY='$KEY'" >> ~/.bashrc
```

You can change other additional application parameters (IP addresses and ports) in the file `app/settings/config.py` or via environment variables.

## Running

You can start the application by simply running the main script 'app/server.py':
```
python app/server.py  # Note that you have to run it in the virtual environment
```
Or just make the `app/server` file executable and run it like any other:
```
chmod +x app/server.py
./app/server.py
```

Now the application should works.
Go to `http://<pfStream-IP-address>:5000` in your browser and use it. 

## pfSense configuration

By default, pfStream listens to the pfSense filterlog messages on the `1514` UDP port.

To forward pfSense firewall messages to our server (application) go to `Status -> System Logs -> Settings` in the pfSense web interface and in one of the `Remote log servers` fields add `<pfStream-IP-address>:1514`

Check the `Remote Syslog Contents -> Firewall Events` flag.
Now all the packet events that have gone through the firewall will be logged on our server. Please note that in the corresponding firewall rule (`Firewall -> Rules -> Edit`) you should mark `Log -> Log packets that are handled by this rule`.


## Notes

- To use a WSGI server like Gunicorn or a web server like NGINX, see the docs [here](https://flask-socketio.readthedocs.io/en/latest/deployment.html).