FROM alpine:edge

RUN apk add --update py-pip
RUN apk add gcc python3-dev musl-dev postgresql-dev
RUN apk add  --no-cache ffmpeg

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY Voice_Recognition_Service.py /usr/src/app/

EXPOSE 5000

CMD ["python3", "/usr/src/app/Voice_Recognition_Service.py"]
