# PyServInfo
A cool command line program to show computer resources, perfect for an always on tty!
![demopicture](https://github.com/Greenishess/PyServInfo/blob/main/pyservinfo.png)
# How to use
First, edit client.py and set the IP variable to your server's IP address. You can also change the port if you'd like. For server.py, the default hosting IP is 0.0.0.0 and port is 5000, changing server.py is optional.
# Running
Each client only requires client.py to work. The server requires main.py and server.py to work. client.py is optional for the server, but if you'd also like to see the server's resource usage you require client.py for the server aswell.
# For the server:
```
git clone https://github.com/Greenishess/PyServInfo.git
python main.py
```
If you intend to run the server on Windows, you need the [third party port](https://pypi.org/project/windows-curses/)
```
pip install windows-curses
```
# For the client
```
git clone https://github.com/Greenishess/PyServInfo.git
python client.py
```
# Tested Operating Systems:
Windows
Ubuntu 24.04 (I think any Linux distro will work though, but regardless, only Ubuntu 24.04 was tested)
