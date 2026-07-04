FROM python:3.9-slim-bookworm
RUN mkdir /bot && chmod 777 /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y git wget pv jq python3-dev ffmpeg mediainfo

COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD ["bash","run.sh"]
