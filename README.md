[![Build Status](https://travis-ci.org/tomcooperca/mlb-slack-tracker.svg?branch=master)](https://travis-ci.org/tomcooperca/mlb-slack-tracker)
# mlb-slack-tracker
Slack app that will update your status with your favourite teams stats/standings!

## TODO
1. Add Flask route to listen for OAuth 2.0 authorization requests (to be used as redirect URL)
2. As part of Flask server app, monitor a given MLB team for updates to a game, standings and any other tracked info. Upon changes, fire off Slack status updates (configurable interval, passed in by Slack app config?)
3. Separate parsing of `mlbgame` API results into appropriate objs (such as a `Team`?)
4. Get decent unit tests and add them to Travis CI.

## Starting the server
```
pipenv run flask run
```

## Tests
```
pipenv run py.test
```
