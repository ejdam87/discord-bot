FROM python:3.10

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

WORKDIR /bot
COPY requirements.txt /bot/
RUN python3 -m pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz
RUN pip3 install -r requirements.txt
COPY . /bot
CMD python bot.py