FROM python:3.5.7-slim-stretch
MAINTAINER Bastian Schoettner

# copy the app in the container
ADD ["antra_bot.py", "requirements.txt", "/bot/"]
ADD ["src/", "/bot/src/"]
ADD ["config/", "/bot/config/"]
WORKDIR /bot

# check if the copy is successful
RUN ls -l

# install requirements
RUN pip install -r requirements.txt

ENV TWITCH_USERNAME=""
ENV CLIENT_ID=""
ENV TWITCH_TOKEN=""
ENV CHANNEL=""

CMD python -u ./antra_bot.py $TWITCH_USERNAME $CLIENT_ID $TWITCH_TOKEN $CHANNEL