# PyServInfo
A cool command line program to show computer resources, perfect for an always on tty!
# How to use
First, edit client.py and set the ip variable to your server's IP address. You can also change the port if you'd like. For server.py, the default hosting ip is 0.0.0.0 and port is 5000, changing server.py is optional.
# Running
Each client only requires client.py to work. The server requires main.py and server.py to work. client.py is optional for the server, but if you'd also like to see the server's resource usage you require client.py for the server aswell.
# For the server:
```
git clone https://github.com/Greenishess/PyServInfo.git
python main.py
```
# For the client
```
git clone https://github.com/Greenishess/PyServInfo.git
python client.py
```
