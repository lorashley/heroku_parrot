Quickly deploy this to Heroku and have a working parrot bot up in seconds!
1. [Create a bot on Cisco Spark](https://developer.ciscospark.com/add-bot.html)

2. Deploy this on Heroku with your **bot token** and **bot username**:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

3. [Create a Webhook](https://developer.ciscospark.com/endpoint-webhooks-post.html) using the **bot token**, and the following example webhook: 
- name: Heroku Parrot Bot
- targetUrl:  _yourherokuproject_.herokuapp.com
- resource: messages
- event: created
