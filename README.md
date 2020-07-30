# Bustabit Bot
This project aims to run the bustabit game (https://www.bustabit.com/) 24/7 in a docker container.

## How it works
> Bustabit does not offer an API to work with, the best workaround is to simulate a web browser activity.
> [Selenium](https://www.selenium.dev/) is a powerfull api to automate browser activity.

Bustabit bot is simulating the creation of an auto bet script and launch it.

## How to setup
### firefox_profile
- Create a new [Firefox profile](https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles?redirectlocale=en-US&redirectslug=profile-manager-create-and-remove-firefox-profiles)
- Loggin to Bustabit with your new Firefox profile
- Get your [Firefox profile folder](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data)
- Copy your folder at the root project
- Rename it **firefox_profile**

> You could implement a logging process with Selenium but Captcha makes it impossible.
> Firefox profile remove this logging process.

### bustabit_script
- Create a [compatible bustabit auto bet script](https://github.com/bustabit/autobet)
- Copy your script at the root project
- Rename it **bustabit_script.js**

### docker-compose
- [Install docker and docker-compose](https://docs.docker.com/compose/install/)

> The easiest way is to install it with `pip`

## How to launch
`docker-compose up -d`

After this you can browse at **localhost:8000** to see some usefull informations about your butsabit account and some of your script logs

> You can modify the port number in docker-compose.yml

## How to stop
`docker-compose down`
