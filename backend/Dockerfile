FROM python:3

RUN apt-get update && apt-get upgrade -y && apt-get install \
  -y --no-install-recommends python3

RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
&& rm -rf /var/lib/apt/lists/*



RUN mkdir /code
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
