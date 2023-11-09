FROM python:3.11

ENV DISCORD_TOKEN=""

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD src src

HEALTHCHECK CMD discordhealthcheck || exit 1

CMD ["python", "-m", "src.run"] 
