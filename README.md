# Bustabit Bot

Bustabit Bot is a solution to run the bustabit game (https://www.bustabit.com/) without using a web browser directly

### How it works

> Bustabit does not offer an API to work with, the best workaround is to simulate a web browser activty.
>*Selenium* (https://www.selenium.dev/) is a powerfull api to automates browser activty.

We are simulating the creation of a new bot in the bustabit format (https://github.com/bustabit/autobet) and we launch it.

### How to setup (Only Firefox)

  - Loggin to Bustabit with your Firefox account
  - Get your Firefox profile folder (https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data)
  - Copy your folder next to the bot.py
  

### How to launch
```sh
$ python3 bot.py [firefox_folder]
```