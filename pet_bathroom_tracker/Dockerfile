FROM python:3.12-alpine

RUN apk add --no-cache su-exec tzdata \
    && addgroup -S dogtracker \
    && adduser -S -G dogtracker dogtracker
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py bootstrap.py ./
COPY templates ./templates
COPY run.sh /usr/local/bin/run-dog-tracker
RUN chmod 755 /usr/local/bin/run-dog-tracker

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
EXPOSE 8099
ENTRYPOINT ["/usr/local/bin/run-dog-tracker"]
