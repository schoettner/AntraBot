#!/usr/bin/env bash

echo "print env"
echo $TWITCH_USERNAME
echo $CLIENT_ID
echo $TWITCH_TOKEN
echo $CHANNEL

echo "start bot"
python3 ./antra_bot.py $TWITCH_USERNAME $CLIENT_ID $TWITCH_TOKEN $CHANNEL