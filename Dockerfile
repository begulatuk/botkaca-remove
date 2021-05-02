FROM alpine:latest as prepare_env
WORKDIR /app

RUN apk --no-cache -q add \
    python3 python3-dev py3-pip libffi libffi-dev musl-dev gcc \
    build-base zlib-dev jpeg-dev libxml2-dev libxslt-dev

RUN pip3 install -q --ignore-installed distlib pipenv
RUN python3 -m venv /app/venv

ENV PATH="/app/venv/bin:$PATH" VIRTUAL_ENV="/app/venv"

ADD https://raw.githubusercontent.com/begulatuk/botkaca-1/begulatuk-patch-1/requirements.txt requirements.txt
RUN pip3 install -q -r requirements.txt


FROM alpine:latest as execute
WORKDIR /app

ENV PATH="/app/venv/bin:$PATH" VIRTUAL_ENV="/app/venv"

RUN apk --no-cache -q add \
    python3 libffi \
    ffmpeg 
RUN mkdir -p /tmp/ && cd /tmp \
    && wget -O /tmp/aria.tar.gz https://raw.githubusercontent.com/Ncode2014/megaria/req/aria2-static-linux-amd64.tar.gz \  
    && tar -xzvf aria.tar.gz \
    && cp -v aria2c /usr/local/bin/ \  
    && chmod +x /usr/local/bin/aria2c \
    && rm -rf /tmp* \
    && cd ~ 
    
COPY --from=prepare_env /app/venv venv
