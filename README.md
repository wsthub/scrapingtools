Author : Yoshio Yamauchi 山内義生 == SPARKLE  
Twitter : [@sparkle_twtt](https://twitter.com/sparkle_twtt)  
Medium : [@sparkle_mdm](https://sparkle-mdm.medium.com/contents-list-f89c9700ba8)  
Email : sparkle.official.01@gmail.com  
You can ask me whatever about the usage of scrapingtools


## Description
  This module helps you scrape the Internet without revealing your identity. It
also features parallel processing allowing you to send requests concurrently
over several threads. All programs are written in Python3 and you need
Ubuntu-18.04 or later.  

  The anonymity is backed by the Tor network. The tor network is a free
proxy chain network available for anyone without any registration. We assume
that you use a Linux operation system, and if you do, it's not that difficult
to set up the tor. I'll show you that below.  

  The threading is done by a python module "multiprocessing". It's different
from a similar module "threading" in a meaning that "multiprocessing" actually
splits tasks over multiple cores and run them concurrently, while "threading"
is just a pseudo parallelization.


## Required System
Ubuntu-18.04 or later  
Python3

## Python Dependencies
`stem`, `random-user-agent`, `numpy`, `requests_html`, `lxml`, `requests`, `bs4`

## Install Tor and Privoxy
### install tor and start
```
$ sudo apt update
$ sudo apt install tor
$ sudo srvice tor start
```

### change password of tor
```
$ kill $(pidof tor)
$ sudo bash -c 'echo "ControlPort 9051" >> /etc/tor/torrc'
$ sudo bash -c 'echo HashedControlPassword $(tor --hash-password "password" | tail -n 1) >> /etc/tor/torrc'
$ sudo service tor restrat
```

### install privoxy
```
$ sudo apt update
$ sudo apt install privoxy
$ sudo bash -c 'echo "forward-socks5t / 127.0.0.1:9050 ." >> /etc/privoxy/config'
$ sudo service privoxy restart
```


## Usage
### definition
```
class AnonymizedConcurrentRequest():
   def __init__(self, tor_password, proxies, port=9051, max_rpm=45, ipchange_interval=1,
                 num_processes=1, replace=True, verbose=False):
```
`tor_password` : the password of the tor server  
`proxies` : the IP and port number of the tor server  
`port` : tor setup port (9051 as default)  
`max_rpm` : maximun number of requests sent per minute  
`ipcahge_interval` : interval of checking IP  
`num_processes` : number of subprocesses == degree of parallelization  
`replace` : if files already exists, then replace that with new ones  
`verbose` : show progress  


### runtest.py
Restart tor and privoxy
```
$ sudo /etc/init.d/tor restart
$ sudo /etc/init.d/privoxy restart
```


Import the module first
```
from scrapingtools import utils
```
Then give a dict of proxies, the setup port, and the password  
```
PROXIES = {"https":"127.0.0.1:8118",
           "http":"127.0.0.1:8118"} # default
PORT = 9051 # default
PROXY_PASSWORD="password" # default
```
The URLs are given as a list of lists, each of which is a pair of a URL and
the destination file for saving  
```
TASKS = [["results_apple.txt","https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch"],
         ["results_nvida.txt","https://finance.yahoo.com/quote/NVDA?p=NVDA&.tsrc=fin-srch"]]
```
Then run the program, giving the number of CPU cores, maximum number of requests sent per minute

```
ACR = utils.AnonymizedConcurrentRequest(PROXY_PASSWORD, max_rpm=60, ipchange_interval=1,
                                        num_processes=1, replace=True, proxies=PROXIES,
                                        port=PORT, verbose=True)
ACR.concurrent_request(TASKS)
```
