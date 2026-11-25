FROM python:3.14-alpine

# git y ssh para trabajar con GitHub; libstdc++/libgcc los necesita el servidor de VS Code en Alpine
RUN apk add --no-cache git openssh-client bash libstdc++ libgcc

# uv copiado desde su imagen oficial (fija la versión: reemplaza X.Y.Z por la de tu `uv --version`)
COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /uvx /usr/local/bin/