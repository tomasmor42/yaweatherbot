In the current repository the bots that checks the weather is imlemented. 

To a source of the data we're using [https://openweathermap.org/](https://openweathermap.org/)
To start the conversation add the bot to your contact list and use `/start` command. 
From there you can set up the city you want to know weather. If you made a typo, bot will show you similar names from the [list](http://bulk.openweathermap.org/sample/) of cities we support.

To start this code for your bot you have to set environment variables `TOKEN` and `API_KEY` with  [token for the telegram bot](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) and [api key to an open weather](https://openweathermap.org/appid) accordingly.
The application is meant to be deployed to Heroky. To set up the name of the application use environment variable `HEROKU_APP_NAME`. 
To find a list of cities some additional data has to be prepared. 