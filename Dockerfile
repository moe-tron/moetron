## Note this will not work with a windows host. Use wsl2 if you have a windows host.
## Exception to this is w/ wsl2 & dev build to support CUDA on wsl
## I haven't tested this but it should work in theory

## Build arg is the key for the bot
## run using -gpus all

FROM tensorflow/tensorflow:1.15.0-gpu-py3
ARG MOEKEY
ENV MOEKEY ${MOEKEY}
ADD . / moetron/
WORKDIR /moetron
RUN pip install -r docker/requirements-docker.txt
CMD python bot.py
