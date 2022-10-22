FROM python:3.9.10-slim
ARG usesource="https://github.com/zytomorrow/AutoScripts.git"
ARG usebranche="dev"

ENV pullbranche=${usebranche}
ENV Sourcepath=${usesource}
ENV TZ=Asia/Shanghai
ENV CRONTIME="30 9 * * *"

RUN \
    apt-get update; \
    apt-get install -y git cron; \
    apt-get clean

WORKDIR /app

RUN \
    git clone -b ${usebranche} ${usesource}; \
    cp -r /app/AutoScripts/* /app; \
    rm -rf AutoScripts/; \
    pip install -r requirements.txt

ENTRYPOINT ["/bin/bash", "./start.sh"]