# Python Reddit to Twitter Bot

This is a simple Python bot that looks up new posts in a loop from specified subreddits and automatically posts them on Twitter.
This project was done mainly for self learning purposes and personal use. You are free to use or distribute the source any way you like.

This bot is being used in the twitter account: [Psychology Bot](https://twitter.com/PsychologyBot24)

**Features:**

* It can post to Twitter from a specific subreddit
* It can search a specific hashtag and:
  * Follow the user
  * Like the tweet
  * Retweet it
  * Reply to it with a specific phrase
* Follow all your followers
* Auto follow new followers


This uses the [tweepy](https://github.com/tweepy/tweepy) and [praw](https://praw.readthedocs.io/en/latest/)

### Prerequisites

1. You will need tweepy and praw installed. Simply run the corresponding pip command like: 

    `pip install tweepy`

    `pip install praw`

2. "Client ID" & "Client Secret" from your reddit account. [Instructions](https://github.com/reddit-archive/reddit/wiki/OAuth2)
3. "Access Token" & "Access Token Secret","Consumer Key" & "Consumer Secret",  from the twitter account that your bot will be using. [Instructions](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)

### To do list:

* ~~Add retweet, like and follow functionality~~
* ~~Add post hashtags and searcg by hashtag~~
* Add config.json file for easier setup
* Add Reddit Content Filter
* Add Multiple subreddit
* Add other sources
* Add a GUI.

## Disclaimer

Use at your own liability, I'm not held responsible for what you do with this script or what happens to you by using this script. Abusing this script *can* get you banned from Twitter.

## License

This project is licensed under the MIT License.

## Other

* Feel free to make edits or to comment on my code so that I can improve!
* Thanks for reading!

If you run into any problems please [file an issue](https://github.com/Keinta15/Python-Reddit-to-Twitter-Bot/issues).


