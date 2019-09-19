# Python Reddit to Twitter Bot

This is a simple Python bot that looks up new posts from specified subreddits and automatically posts them on Twitter. 


**Features:**

* It can post to Twitter from a specific subreddit
* It can search a specific hashtag and:
  * Follow the user
  * Like the tweet
  * Retweet it
  * Reply to it with a specific phrase
* Follow all your followers
* Auto follow new followers


This uses the [tweepy](https://github.com/tweepy/tweepy), [PRAW](https://praw.readthedocs.io/en/latest/)

### Prerequisites

1. You will need tweepy and praw installed. Simply run the corresponding pip command like: 

`pip install tweepy`

`pip install praw`

2. "Client ID" & "Client Secret" from your reddit account. [Instructions](https://github.com/reddit-archive/reddit/wiki/OAuth2)
3. "Consumer Key","Consumer Secret", "Access Token" & "Access Token Secret" from the twitter account that your bot will be using. [Instructions](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)

~~Additionally, you will need to set up your config.json file.~~

### ~~Setting up config.json file~~

~~This file is the heart of the bot. You must place your twitter auth info in the auth object. I've labeled what you have to put and where to the best of my abilities.~~

### Todo:

* Add config.json file
* Add Reddit Content Filter
* Add Multiple subreddit
* Add other sources
* Add a GUI.

## Disclaimer

Use at your own liability, I'm not held responsible for what you do with this script or what happens to you by using this script. Abusing this script *can* get you banned from Twitter.

## Authors

* **Keinta15** - [Keinta15](https://github.com/keinta15)

## License

This project is licensed under the MIT License.

## Acknowledgments/Other

* Feel free to make edits or to comment on my code so that I can improve!
* Thanks for reading!

If you run into any problems please [file an issue](https://github.com/princeali909/reddit-to-twitter-bot/issues).


