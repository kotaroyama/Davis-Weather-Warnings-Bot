# Davis Weather Warnigs (Bot)
A [bot](https://twitter.com/davisweatherbot) that tweets out current active weather warnings in Davis, California, USA.

## Motivation
I live in Davis, California, and there seem to be a lot of weather related warnings that are actually useful, like heat warnings. However, they're kind of a pain to keep track of. I created this bot so that all I have to do is just looking at the tweets to know if there are any currently active weather warnings.

## Logic
The [Twitter bot I created](https://twitter.com/davisweatherbot) that I created specifically tweets out weather warnings in Davis, but it can work for pretty much anywhere in the U.S. You have to give the city and state, and Google Maps API will pull the latitude and longtitude. From there, it will contact [the National Weather Services API](https://www.weather.gov/documentation/services-web-api) to see if the location has any active warnings. Twitter Authentication part is where you have to provide your own credentials via your [Twitter Developer account](https://developer.twitter.com/). Here, I am using [Tweepy](https://www.tweepy.org/) to do all the heavy lifting with the Twitter API.
Given that each tweet can only have up to 280 characters, it is often the case that the text of a warning is much longer than 280 characters, so I had to split it in to two or more tweets, which for some reason was a bit tricky.

## Todo
The reason why the tweets end up being so long is becaue the bot tweets out the raw warnings retrieved from the API with minimum formatting. What I would like to do now is to get the important pieces of information only, and shorten and prettify the tweets so that they are much easier to read.
