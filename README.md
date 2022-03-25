# pyCTelebot


## Description

Telegram bot to trade.


## System requirements

### Programming language
* [Python3](https://www.python.org/) [(doc)](https://docs.python.org/)

### Packages
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) [(doc)](https://python-telegram-bot.readthedocs.io/en/stable/)
* [ccxt](https://github.com/ccxt/ccxt) [(doc)](https://docs.ccxt.com/en/latest/manual.html)
### APIs
* [API Telegram](https://core.telegram.org/bots/api)

## Instructions
### Installation

```shell
$ pip install ...
```
#### Configure Vars

| Vars                 | Description                                                  |
|----------------------|--------------------------------------------------------------|
| TOKEN_TELEGRAM       | Token telegram bot                                           |
| WEBHOOK_URL_TELEGRAM | URL app in [Heroku](https://www.heroku.com/) or other server |
| TOKEN_CRYPTO_KEY     | Cryptocurrency exchange apiKey                               |
| TOKEN_CRYPTO_SECRET  | Cryptocurrency exchange secret                               |
| USER_ADMIN           | Telegram user ID                                             |

#### Activate Webhook in Telegram bot
Execute: https://api.telegram.org/bot<TOKEN_TELEGRAM>/setWebHook?url=<WEBHOOK_URL_TELEGRAM>

NOTE: If you want to run it with polling, you can use param -Tp
```shell
$ python -m pyCTelebot.pyCTelebotBase -Tp
```

#### For developers
```shell
git clone https://github.com/juanjo78git/pyCTelebot.git
cd pyCTelebot
$ pip install -e . 
$ python -m pyCTelebot.pyCTelebotBase  # Or run without install
```


## Info

- https://planetachatbot.com/telegram-bot-webhook-heroku/
- https://planetachatbot.com/crea-e-implementa-bot-telegram-memoria-corto-largo-plazo/

## License

MIT
