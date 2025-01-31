# pyCTelebot


## Description

Telegram bot to trade.


## System requirements

### Programming language
* [Python3](https://www.python.org/) [(doc)](https://docs.python.org/)

### Packages
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) [(doc)](https://python-telegram-bot.readthedocs.io/en/stable/)
* [CCXT – CryptoCurrency eXchange Trading Library](https://github.com/ccxt/ccxt) [(doc)](https://docs.ccxt.com/en/latest/manual.html)
* [APScheduler - Advanced Python Scheduler](https://github.com/agronholm/apscheduler) [(doc)](https://apscheduler.readthedocs.io/en/3.x/)
### APIs
* [API Telegram](https://core.telegram.org/bots/api)

## Instructions
### Installation

```shell
$ pip install pyCTelebot
```
#### Configure Vars

| Vars                 | Description                                                                                                                                         |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| TOKEN_TELEGRAM       | Token telegram bot                                                                                                                                  |
| WEBHOOK_URL_TELEGRAM | URL app in [Heroku](https://www.heroku.com/) or other server                                                                                        |
| TELEGRAM_ADMIN_GROUP | Telegram admin group id list. Format: \[chat_id]                                                                                                    |
| ENV_CONFIG           | Environment config. log values: DEBUG / INFO / WARNING / ERROR / CRITICAL. env values: TEST / PROD. Default values: {"log": "DEBUG", "env": "TEST"} |
| DATABASE_URL         | DB Connection                                                                                                                                       |
| ENCRYPTION_KEY       | Encryption key for APIs                                                                                                                             |


#### DataBase
- [DDL](data/initial_ddl.sql)
- [DML](data/initial_dml.sql) - For test
- ER Model
![ER Model](data/ER_model.png)

#### Activate Webhook in Telegram bot
Execute: https://api.telegram.org/bot<TOKEN_TELEGRAM>/setWebHook?url=<WEBHOOK_URL_TELEGRAM>
Info about your webhook: https://api.telegram.org/bot<TOKEN_TELEGRAM>/getWebhookInfo
```shell
$ python -m pyCTelebot.pyCTelebotBase
```
NOTE: If you want to run it with polling, you can use param -Tp
```shell
$ python -m pyCTelebot.pyCTelebotBase -Tp
```

#### Run cron for do something
If you want to run a cron, you can use param -c
```shell
$ python -m pyCTelebot.pyCTelebotBase -c
```

#### For developers
```shell
git clone https://github.com/juanjo78git/pyCTelebot.git
cd pyCTelebot
$ pip install -e . 
$ python -m pyCTelebot.pyCTelebotBase  -poc # Run PoC implemented
```

## Info

- https://planetachatbot.com/telegram-bot-webhook-heroku/
- https://planetachatbot.com/crea-e-implementa-bot-telegram-memoria-corto-largo-plazo/
- http://kaffeine.herokuapp.com/
- https://github.com/martin-ueding/vigilant-crypto-snatch

## License

[MIT](LICENSE)
