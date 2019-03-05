# AntraBot
Simple chat bot for experimenting with twitch icr client. This project is also used to teach coding
by example.The bot should perform fun tasks that should be helpful.

### Requirements
The bot is written with python 3.5
```sh
$ pip3 install irc
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
| messages sent from the irc client do sometimes not appear in twitch chat | no |
|missing wiki at https://www.fandom.com/|no|

### References
[Example-Code from Amazon](https://github.com/twitchdev/chat-samples/tree/master/python)

