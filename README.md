# Bustabit Bot
This project aims to use a free Heroku webserver (https://www.heroku.com/) to run the bustabit game (https://www.bustabit.com/) 24/7

## How it works
> Bustabit does not offer an API to work with, the best workaround is to simulate a web browser activity.
> Selenium (https://www.selenium.dev/) is a powerfull api to automate browser activity.

Bustabit bot is simulating the creation of an auto bet script and launch it.

## How to setup
### Heroku
- Create a new application
- Clone this project and add the heroku remote
- Set the stack of your app to container `$ heroku stack:set container`
- Configure your app environment variable to add **HEROKU_APP_URL** (eg: *https://MY_APP.herokuapp.com/*)

### firefox_profile
- Create a new Firefox profile (https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles?redirectlocale=en-US&redirectslug=profile-manager-create-and-remove-firefox-profiles)
- Loggin to Bustabit with your new Firefox profile
- Get your Firefox profile folder (https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data)
- Copy your folder at the root project
- Rename it **firefox_profile**

> You could implement a logging process with Selenium but Captcha makes it impossible
> Firefox profile remove this logging process.

### bustabit_script
- Create a compatible bustabit auto bet script (https://github.com/bustabit/autobet)
- Copy your script at the root project
- Rename it **bustabit_script.js**

## How to launch
Push all the files (Bustabot bot + firefox_profile + bustabit_script.js) to the heroku remote.