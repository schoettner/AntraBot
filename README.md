# AntrasBot [![Build Status](https://travis-ci.org/schoettner/AntraBot.svg?branch=master)](https://travis-ci.org/schoettner/AntraBot)
AntrasBot is a [Twitch](www.twitch.tv) chatbot. It is a Hollow Knight (by [Team Cherry](http://teamcherry.com.au)) themed chat RPG. It allows you to collect geo, fight bosses,
buy upgrades and climb the leaderboard. The board was initially designed for [VysualsTv](https://www.twitch.tv/vysualstv).
That is why it still contains a *vys_command_handler*. 

The bot is tested with *pytest* to ensure that new versions do not break mandatory features.

![Hollow Knight](http://teamcherry.com.au/wp-content/uploads/banner_real.jpg)



You can find end-user documentation on [Fandom](https://antrabot.fandom.com/wiki/AntraBot_Wiki#).


### Get an token for the bot ###
|info|detail|
|-----------|----------------------------------------------------------------|
| token url | https://twitchapps.com/tokengen/#                              |
| scope     | chat:read chat:edit whispers:read whispers:edit                |
| note      | login with the AntrasBot twitch account for the token creation |


### Start the bot ###
I used **virtualenv** to manage the python environment
```sh
source ~/.virtualenvs/python3.5/bin/activate
```
Install the required libraries with pip
```sh
$ pip3 install -r requirements.txt
```
Start a local mongo db instance
```sh
docker-compose up
```
Start the bot
```sh
python3 antra_bot.py <username> <client id> <token> <channel> <mongo_uri>
```

### Automatic Deployment ###
The bot has an automated test and deploy pipeline. The tests are executed with [Travis CI](https://travis-ci.org/). The config 
for executing the tests is in the *.travis.yml* file. The bot is then deployed to [Heroku](heroku.com), if the tests were
executed successful. The Heroku process config is in the *Procfile* file.


### TODO list ###
- [x] messages sent from the irc client do sometimes not appear in twitch chat
- [x] geo schedule starts itself
- [x] players can buy items and fight bosses with an id
- [x] fix whisper receive and send
- [x] impl leader board
- [ ] add highest defeated str in stats
- [x] penalty for death
- [x] reward for boss defeat
- [ ] all classes are fully tested
- [x] use embedded mongo db for testing


### References ###  
[Example-Code from Amazon](https://github.com/twitchdev/chat-samples/tree/master/python)  
[AntraBot Wiki](https://antrabot.fandom.com/wiki/AntraBot_Wiki#)  
[Twitch IRC Guide](https://dev.twitch.tv/docs/irc/guide/)  
