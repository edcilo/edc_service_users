FROM python:3.9.1-alpine

# causes all output to stdout to be flushed immediately,
ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add --no-cache \
        gcc \
        jpeg-dev \
        libjpeg \
        musl-dev \
        postgresql-dev \
        python3-dev \
        zlib-dev

RUN mkdir /code
WORKDIR /code

COPY . /code/
RUN pip install -r requirements.txt

RUN chmod a+rx ./start.sh

EXPOSE 8000
CMD ["./start.sh"]
