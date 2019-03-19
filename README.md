# AntraBot
Simple chat bot for experimenting with twitch icr client. This project is also used to teach coding
by example.The bot should perform fun tasks that should be helpful.

You can find end-user documentation on [Fandom](https://antrabot.fandom.com/wiki/AntraBot_Wiki#).

### Requirements
The bot is written with python 3.5
```sh
$ pip3 install irc
$ pip3 install pymongo
```
I used **virtualenv** to manage the pyhton environment

### Get an token for the bot
|info|detail|
|-----------|----------------------------------------------------------------|
| token url | https://twitchapps.com/tokengen/#                              |
| client id | jycvlymxj2qacjlw08c1t5ud7vqgif                                 |
| scope     | chat:read chat:edit                                            |
| note      | login with the AntrasBot twitch account for the token creation |

### Start the bot
Activate your python environment
```sh
source ~/.virtualenvs/python3.5/bin/activate
```
General start command
```sh
python chatbot.py <username> <client id> <token> <channel>
```
Start command for AntraBot
```sh
python3 chatbot.py AntraBot jycvlymxj2qacjlw08c1t5ud7vqgif <token> antrazith
```

### Known issues
|info|solved|
|-----------|----------------------------------------------------------------|
| messages sent from the irc client do sometimes not appear in twitch chat | no - irc cooldown on twitch end |
| player storage is not optimal | yes |
| players can not yet purchase items with a command | yes |
| geo schedule not working yet | yes |

### References
[Example-Code from Amazon](https://github.com/twitchdev/chat-samples/tree/master/python)
[AntraBot Wiki](https://antrabot.fandom.com/wiki/AntraBot_Wiki#)
[Twitch IRC Guide](https://dev.twitch.tv/docs/irc/guide/)

### todo from feedback
impl leader board
add highest defeated str in stats
penalty for death
reward for boss defeat
add test to purchase all 10 upgrades in a row
add test for vys command handler
use embedded mongo db for testing