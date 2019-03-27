# AntraBot [![Build Status](https://travis-ci.org/schoettner/AntraBot.svg?branch=master)](https://travis-ci.org/schoettner/AntraBot)
Simple chat bot for experimenting with twitch icr client. This project is also used to teach coding
by example.The bot should perform fun tasks that should be helpful.

You can find end-user documentation on [Fandom](https://antrabot.fandom.com/wiki/AntraBot_Wiki#).


### Get an token for the bot ###
|info|detail|
|-----------|----------------------------------------------------------------|
| token url | https://twitchapps.com/tokengen/#                              |
| scope     | chat:read chat:edit whispers:read whispers:edit                |
| note      | login with the AntrasBot twitch account for the token creation |


### Start the bot ###
Activate your python environment. I used **virtualenv** to manage the python environment
```sh
source ~/.virtualenvs/python3.5/bin/activate
```
Install the required libraries
```sh
$ pip3 install -r requirements.txt
```
Start the bot
```sh
python3 antra_bot.py <username> <client id> <token> <channel> <mongo_uri>
```


### TODO list ###
- [x] messages sent from the irc client do sometimes not appear in twitch chat
- [x] geo schedule starts itself
- [x] players can buy items and fight bosses with an id
- [ ] fix whisper receive and send
- [x] impl leader board
- [ ] add highest defeated str in stats
- [x] penalty for death
- [x] reward for boss defeat
- [ ] all classes are fully tested
- [ ] use embedded mongo db for testing


### References ###
[Example-Code from Amazon](https://github.com/twitchdev/chat-samples/tree/master/python)  
[AntraBot Wiki](https://antrabot.fandom.com/wiki/AntraBot_Wiki#)  
[Twitch IRC Guide](https://dev.twitch.tv/docs/irc/guide/)  
