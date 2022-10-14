FROM python:3.8.10
EXPOSE 8000
COPY . /app
WORKDIR /app

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh


RUN mkdir static
CMD ["/app/entrypoint.sh"]
