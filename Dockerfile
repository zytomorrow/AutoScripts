FROM python:3.8.13-slim
ARG usesource="https://github.com/zytomorrow/AutoScripts.git"
ARG usebranche="master"

ENV pullbranche=${usebranche}
ENV Sourcepath=${usesource}
ENV TZ=Asia/Shanghai
ENV CRONTIME="30 9 * * *"

WORKDIR /app

RUN \
    apt-get update; \
    apt-get install -y git cron; \
    apt-get clean; \
    git clone  --depth 1  -b ${usebranche} ${usesource}; \
    cp -r /app/AutoScripts/* /app; \
    rm -rf AutoScripts/; \
    pip install -r requirements.txt

ENTRYPOINT ["/bin/bash", "./start.sh"]