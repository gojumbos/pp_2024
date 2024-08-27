FROM ubuntu:latest
LABEL authors="declanborcich"

ENTRYPOINT ["top", "-b"]