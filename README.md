[![Build Status](https://travis-ci.org/tomcooperca/mlb-slack-tracker.svg?branch=master)](https://travis-ci.org/tomcooperca/mlb-slack-tracker)
# mlb-slack-tracker
Slack app that will update your status with your favourite teams stats/standings!

## TODO
1. ~~Add Flask route to listen for OAuth 2.0 authorization requests (to be used as redirect URL)~~ Done
2. As part of a background celery task, monitor all teams for updates on a day's game, standings and any other tracked info. Upon changes, fire off Slack status updates.
3. Separate parsing of `mlbgame` API results into appropriate objs (such as a `Team`?)
4. ~~Get decent unit tests and add them to Travis CI.~~ Done
5. Bot form of this app that will message an individual on today's game and standings instead of mucking with a status.
6. Team factory creates instances of all teams on app startup.

## Starting the server
```
pipenv run flask run
```

## Tests
```
pipenv run py.test
```
