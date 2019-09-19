# Version 0.2
import praw
import tweepy
import time
import os

# Place your Twitter API keys here
access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''

#Here is the max amount of characters we can put in a tweet
tweet_max_char = 240

#Here is the amount of characters a shortlink takes up
shortlink_max_char = 24

#Subreddit we are trying to extraxt posts from (no need to add the r/ in the beggining)
subreddit_to_watch = ''

#Every reddit post has an ID, here we want to store these ID's in a .txt file to avoid tweeting the same post twice.
posted_reddit_ids = 'ID_Logs.txt'

#Duration your bot will wait before tweeting again in seconds
time_between_tweets = 60

#Duration the bot will sleep before restarting the main process in seconds
time_between_restarts = 30 * 60 # 30 minutes

#Keyword inside reddit title.
#Bot will only tweet posts with the keywords in this list. Reccomended to enter one keyword at a time.
#Leave List empty if you want bot to tweet all posts.
keyword_list = []

#Place hastag you want here
hashtags_suffix = '#' #determines what hashtag are you using at the end of your tweets
search = '#' #determines what hashtag are you gonna search for
numberOfTweets = 1 #number of tweets it will look that are using the hashtag
numberOfTweets = int(numberOfTweets)
phrase = "Phrase here" #phrase for replies
reply = "" #reply with phrase to people using the hashtag
retweet = "" #retweet tweets that are using the hashtag
favorite = "yes" #favorite tweets that are using the hashtag
follow = "" #Follow users that use the hashtag
followAll = "" #Follow all users that are currently following you
autoFollow = "yes" #auto follows users that follows you

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
user = api.me()

print(user.name)
print(user.location)

def connection_to_reddit(subreddit):
    '''Connects to Reddit API'''
    print('[bot] Setting up connection with reddit')
    #Place reddit API keys here.
    reddit_api = praw.Reddit(user_agent = 'Twitter Bot'.format(subreddit),
                              client_id = '', #Place Client ID
                              client_secret = '') #Place Client Secret
    return reddit_api.subreddit(subreddit)


def shrink_title(title,character_count):
    '''Shortens title if too long so that it will fit into a tweet'''
    if len(title) >= character_count:
        return title[:character_count - 1] + '…'
    else:
        return title


def tweet_composer(subreddit_info):
    '''Goes through posts on reddit and extracts a shortened link, title & ID'''
    post_links = []  # list to store our links
    post_titles = []  # list to store our titles
    post_ids = []  # list to store our id's
    print("[bot] extracting posts from sub-reddit")
    print('[bot] Sucessfully authenticated on Twitter as @' + user.name)

    for submission in subreddit_info.new(limit=5):
        if not conflicting_tweet(submission.id):
            if not keyword_list:
                print("No keywords defined.")
                 # This stores a link to the reddit post itself
                 # If you want to link to what the post is linking to instead, use
                 # "submission.url" instead of "submission.permalink"
                post_titles.append(submission.title)
                post_links.append(submission.shortlink)
                post_ids.append(submission.id)
            else:
                if any(word in submission.title.casefold() for word in keyword_list): #.casefold() to ignore case when comparing the title and keyword
                    post_titles.append(submission.title)
                    post_links.append(submission.shortlink)
                    post_ids.append(submission.id)
                else:
                    print("This isn't the post your looking for.")

        else:
            print("[" + user.name +"] Skipping because tweet was already posted")
    return post_links, post_titles, post_ids


def id_logging(id):
    '''Logs reddit post ID's into our .txt file'''
    with open(posted_reddit_ids, 'a') as f:
        f.write(str(id)+ '\n')


def conflicting_tweet(post_id):
    '''reads through our .txt file and determines if tweet has already been posted'''
    found = 0
    with open(posted_reddit_ids, 'r') as f:
        for line in f:
            if post_id in line:
                found = 1
                break
    return found



def tweeting(post_links,post_titles,post_ids):
    '''Tweets our reddit posts'''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    for post_title, post_link, post_id in zip(post_titles, post_links, post_ids):
        extra_text = ' ' + post_link #space needed to seperate the link and the title
        hashtag = ' ' + hashtags_suffix #space needed to seperate the link with hashtag
        post_text = shrink_title(post_title, tweet_max_char - shortlink_max_char - 1) + extra_text + hashtag
        print('[' + user.name + '] Posting this tweet to Twitter:')
        print(post_text)
        api.update_status(status = post_text)
        print('[bot] Sleeping for', time_between_tweets, 'seconds')
        time.sleep(time_between_tweets)
        print('[bot] Cleaning up...')
        id_logging(post_id)

def main():
    '''Main function'''
    # If the tweet tracking file does not already exist, create it
    if not os.path.exists(posted_reddit_ids):
        with open(posted_reddit_ids, 'w'):
            pass

    subreddit = connection_to_reddit(subreddit_to_watch)
    post_links, post_titles, post_ids = tweet_composer(subreddit)
    

    if reply == "yes":
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Reply
                print('\nTweet by: @' + tweet.user.screen_name)
                print('ID: @' + str(tweet.user.id))
                tweetId = tweet.user.id
                username = tweet.user.screen_name
                api.update_status("@" + username + " " + phrase, in_reply_to_status_id = tweetId)
                print ("Replied with " + phrase)
                
            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    if retweet == "yes": 
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Retweet
                tweet.retweet()
                print('[' + user.name + '] Retweeted a tweet')   

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    if favorite == "yes": 
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Favorite
                tweet.favorite()
                print('[' + user.name + '] Favorited a tweet')   

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    if follow == "yes": 
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Follow
                tweet.user.follow()
                print('[' + user.name + '] Followed a user')
                
            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break 

    if followAll == "yes":
        for follower in tweepy.Cursor(api.followers).items():
            try: 
                print("[bot] Checking if", user.name, "has more followers")
                follower.follow()
                print("[bot] Followed everyone that is following " + user.name, "if it wasnt following already.")
            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    if autoFollow == "yes":
        print("[bot] Checking if", user.name, "has more followers")
        for follower in tweepy.Cursor(api.followers).items():
            if not follower.following:
                print("[bot]", user.name, "now following " + follower.name)
                follower.follow()
    
    tweeting(post_links, post_titles, post_ids)
    print('[bot] Restarting main process in', time_between_restarts, 'seconds')
    time.sleep(time_between_restarts)
    main()

if __name__ == '__main__':
    main()
