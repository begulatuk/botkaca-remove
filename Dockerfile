FROM alpine:edge

RUN mkdir ./app
RUN chmod 777 ./app
WORKDIR /app

RUN sed -e 's;^#http\(.*\)/edge/community;http\1/edge/community;g' -i /etc/apk/repositories
RUN apk update -q && apk --no-cache -q add \
    python3-dev py3-pip py3-lxml \
    ffmpeg  aria2  && \
    apk add -qq --no-cache --virtual .build-deps \
    build-base zlib-dev jpeg-dev  \
    libffi-dev libxml2-dev libxslt-dev && \
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget -q https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.32-r0/glibc-2.32-r0.apk && \
    apk add -q glibc-2.32-r0.apk && \
    rm /etc/apk/keys/sgerrand.rsa.pub && \
    rm glibc-2.32-r0.apk && \
    rm -r /var/cache/apk/APKINDEX.* && \
    rm -rf /tmp/* /var/cache/apk/* /var/tmp/*
RUN pip3 install -q -r requirements.txt
COPY . .
CMD ["python3", "-m", "bot"]
