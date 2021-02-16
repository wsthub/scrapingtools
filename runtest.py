# AUTHOR:Yoshio Yamauchi == SPARKLE
# WRITTEN:Feb 12, 2021

from scrapingtools import utils
PROXIES = {"https":"127.0.0.1:8118",
           "http":"127.0.0.1:8118"} # the proxy ip you've set
PORT = 9051 # the port number you've set
TASKS = [["results_apple.txt","https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch"],
         ["results_nvida.txt","https://finance.yahoo.com/quote/NVDA?p=NVDA&.tsrc=fin-srch"]]
PROXY_PASSWORD="password" # the password you've set
ACR = utils.AnonymizedConcurrentRequest(PROXY_PASSWORD, max_rpm=60, ipchange_interval=1,
                                        num_processes=1, replace=True, proxies=PROXIES,
                                        port=PORT, verbose=True)
ACR.concurrent_request(TASKS)

# DESCRIPTION
# class AnonymizedConcurrentRequest():
#     def __init__(self, tor_password, proxies, port, max_rpm=45, ipchange_interval=1,
#                  num_processes=1, replace=True, verbose=False):
# tor_password: the password you of the tor server
# proxies: the IP and port number of the tor server
# max_rpm: maximun number of requests sernt per minute
# ipcahge_interval: interval of checking ip
# num_processes: number of subprocesses = degree of parallelization
# replace: if file already exists, then replace that with a new one
# verbose: show progress
