# Feb 3, 2021
# #proxy #tor #onion #routing #onion_routing #scraping #scrape
# #stem #anonymize #anonymization #change_url
# https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b
# https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853
# sudo apt install tor
# sudo apt install stem

# before stat requestin, restart tor and privoxy:
# sudo /etc/init.d/tor restart
# sudo /etc/init.d/privoxy restart
print("utils.py:START")
import sys
import pickle
import stem
import stem.connection
import time
import urllib
from tqdm import tqdm
from stem import Signal
from stem.control import Controller
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import numpy as np
# import pandas as pd
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
from lxml import html
import requests
from lxml import etree
import re
from re import sub
from decimal import Decimal
import datetime
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os
import csv
import json
import subprocess
import threading
import logging
import multiprocessing
from multiprocessing import Process, Manager, Value
# os.system("sudo /etc/init.d/tor restart")
# os.system("sudo /etc/init.d/privoxy restart")




class AnonymizedConcurrentRequest():
    def __init__(self, tor_password, proxies, port, max_rpm=45, ipchange_interval=1,
                 num_processes=1, replace=True, verbose=False):
        self.TOR_PASSWORD = tor_password
        self.IP_CHECK_SERVICE = "http://icanhazip.com/"
        self.IP_CHECK_INTERVAL = ipchange_interval # sec
        self.n = num_processes
        self.replace = replace
        self.oldIP = "0.0.0.0"
        self.newIP = "0.0.0.0"
        self.oldIP_save = "0.0.0.0"
        self.VERBOSE=verbose
        self.PROXIES = proxies
        self.PORT = port
        self.ipchangerate = Value('f', 0)
        self.ipchagetime = None
        self.max_rpm = max_rpm # 30 request per minute
        self.last_update = time.time()
        self.last_request = time.time()
        self.ACQUIRED = False
        self.QUIT = False
        self.proxyset_time = None
        self.request_time = None
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        self.user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        self._ip_changer(interval=ipchange_interval)

    def _ip_changer(self, interval):
        th1 = threading.Thread(target=self._ipchanger_thread,
                               args=(interval,self.ipchangerate,))
        th1.start()

    def _ipchanger_thread(self, interval, ipchangerate):
        while True:
            if self.QUIT:quit()
            with Controller.from_port(port = self.PORT) as controller:
                controller.authenticate(password = self.TOR_PASSWORD)
                controller.signal(Signal.NEWNYM)
                controller.close()
            self.newIP = self._request(self.IP_CHECK_SERVICE)
            time.sleep(interval)
            if self.newIP != self.oldIP:
                self.oldIP = self.newIP
                # print("NEW IP:", self.newIP.decode("utf-8").replace("\n", ""))
                et = time.time() - self.last_update
                self.last_update = time.time()
                ipchangerate.value = 60.0/(et)
                # print("ipchangerate:%.1f"%ipchangerate.value)

    def _request(self, url):
        t1s = time.time()
        _proxy_support = urllib.request.ProxyHandler(self.PROXIES)
        _opener = urllib.request.build_opener(_proxy_support)
        urllib.request.install_opener(_opener)
        t1e = time.time()
        user_agent = self.user_agent_rotator.get_random_user_agent()
        headers={'User-Agent':user_agent}
        t2s = time.time()
        try:
            request=urllib.request.Request(url, None, headers)
            result = urllib.request.urlopen(request).read()
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(str(e))
            return 'ERROR'
        t2e = time.time()
        self.proxyset_time = t1e - t1s
        self.request_time = t2e - t2s
        return result.decode("utf-8")

    def concurrent_request(self, jobs):
        if len(jobs) < self.n:
            self.QUIT = True
            sys.exit("ERROR:number of jobs must be greater than number of subprocess")

        self.max_rpm_per_thread = self.max_rpm*1.0/self.n
        jobs_split = self._split_task(jobs, self.n)
        THREADS = []
        progress = Value('i', 0)
        ave_rpms = {}
        for i in range(self.n):
            ave_rpms[i] = Value('f', 0)
            pr = multiprocessing.Process(target=self._request_thread, args=(jobs_split[i], progress, ave_rpms[i],))
            pr.start()
            THREADS += [pr]
        watcher = multiprocessing.Process(target=self._progresswatch, args=(progress,len(jobs),self.ipchangerate, ave_rpms,))
        watcher.start()
        watcher.join()
        for i in range(self.n):
            THREADS[i].join()
            if self.VERBOSE: print("PROCESS %d JOINED"%i)
        self.QUIT = True

    def _progresswatch(self, progress, goal, ipchangerate, ave_rpms):
        tn2 = time.time()
        vn2 = progress.value
        while progress.value < 0.95*goal:
            tn1 = tn2
            tn2 = time.time()
            vn1 = vn2
            vn2 = progress.value
            rpm = 0
            for i in range(len(ave_rpms)):
                rpm += ave_rpms[i].value
            if self.VERBOSE:
                sys.stdout.write("\r" + '''%d/%d FINISHED (%.1f PERCENT) | REQUEST %.1f PM | IPCHANGE %.1f PM '''%(progress.value+1, goal, 100*progress.value/goal, rpm, ipchangerate.value))
                sys.stdout.flush()
            time.sleep(0.5)

    def _request_thread(self, jobs, progress, ave_rpm):
        last_request = time.time()
        ave_rpm.value = 0
        for job in jobs:
            t1s = time.time()
            SAVE_PATH = job[0]
            if os.path.exists and (not self.replace):continue
            URL = job[1]
            html = self._request(URL)
            # rawstr = areq.request(REQUEST_URL).decode("utf-8")
            if html == "ERROR":
                continue
            with open(SAVE_PATH, "w") as f:
                f.write(html)
            progress.value += 1
            et = time.time() - last_request
            last_request = time.time()
            sleeptime = 60./self.max_rpm_per_thread - et
            if sleeptime > 0:
                time.sleep(sleeptime)
            t1e = time.time()
            ave_rpm.value = 0.1*60.0/(t1e - t1s) + 0.9*ave_rpm.value
        ave_rpm.value = 0

    def _split_task(self, jobs, n):
        spl = []
        N = len(jobs)
        for i in range(n):
            spl += [jobs[int(i*N/n):int((i+1)*N/n)]]
        return spl
