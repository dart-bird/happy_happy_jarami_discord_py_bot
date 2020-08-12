ARG distro=stretch
FROM resin/rpi-raspbian:$distro

RUN apt-get update
RUN apt-get install python3 python3-dev python3-pip
RUN sudo apt-get install build-essential
RUN sudo apt-get install gdb-multiarch

RUN pip3 install setuptools
RUN pip3 install wheel
RUN pip3 install discord.py
RUN pip3 install bs4

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY main.py /usr/src/bot

CMD ["python3", "main.py"]