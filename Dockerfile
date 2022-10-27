FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN export DISCORD_TOKEN
RUN export DISCORD_GUILD
CMD python3.10 bot.py
