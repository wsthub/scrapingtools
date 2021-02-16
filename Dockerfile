# FROM python:3

# WORKDIR /usr/src/app

# The COPY instruction copies new files or directories from <src> and
# adds them to the filesystem of the container at the path <dest>
# COPY <src> <dest>


# The FROM instruction initializes a new build stage and sets the
# Base Image for subsequent instructions.
FROM ubuntu:18.04
RUN apt update && apt install -y cowsay
RUN apt-get update && apt-get install net-tools
RUN apt-get update && apt-get install -y python3-pip
RUN apt update && apt install -y tor
RUN service tor start
# RUN service tor stop
# RUN kill $(pidof tor)
RUN bash -c 'echo "ControlPort 9051" >> /etc/tor/torrc'
RUN bash -c 'echo HashedControlPassword $(tor --hash-password "password" | tail -n 1) >> /etc/tor/torrc'
# RUN service tor start
RUN apt update && apt install -y privoxy
RUN bash -c 'echo "forward-socks5t / 127.0.0.1:9050 ." >> /etc/privoxy/config'
RUN service tor restart
RUN service privoxy restart
# RUN apt update && apt install -y software-properties-common
# RUN apt update && add-apt-repository -y ppa:deadsnakes/ppa
# RUN apt updte && apt install -y python3.8
RUN mkdir installation
COPY ./runtest.py ./installation
# COPY ./scrapingtools ./installation
# COPY ./setup.py ./installation
COPY ./requirements.txt ./installation
# COPY ./LICENCE ./installation
# COPY README.md ./installation
# COPY setup.cfg ./installation
RUN pip3 install -r ./installation/requirements.txt
# RUN python3 setup.py install
# RUN pip3 install ./installation
RUN pip3 install scrapingtools
# ENV PATH=/root/.local:$PATH
# RUN apt-get update
# RUN apt install software-properties-common
# RUN add-apt-repository ppa:deadsnakes/ppa
CMD ["/usr/games/cowsay", "Dockerfiles are cool!"]
CMD ["touch", "test01.txt"]
CMD ["whoami"]
CMD ["ls"]
CMD ["ifconfig"]
# CMD ["python3", "setup.py", "install"]
# CMD ["pip3", "freeze"]
CMD pip3 freeze
CMD ["python3", "./installation/runtest.py"]
CMD python3 ./installation/runtest.py
# CMD [ "python3", "./tmp01.py"]
# CMD ["pwd"]
# CMD ["apt", "-y", "install", "python3-pip"]
# COPY . .



# docker build -t test1 . # build the image
# docker run --rm test1 # run a container
