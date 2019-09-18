import praw
import tweepy
import time
import os


# Place your Twitter API keys here
access_token = '1174196504728408064-nJJ5hvbyFREDWGCj2DtXNsjCzYQKNN'
access_token_secret = 'KwgwiVDRU6WLi7llQCOtjKfcYCi0gi45aqGLzEauAHZj9'
consumer_key = 'O1L7WOMajLAB9MZfLTVwgBfbo'
consumer_secret = 'JDtVG7j1hTyOd7B6T0CqEU3EoKnCCxmgRDoH8baZAjWNPzSo4R'

#Here is the max amount of characters we can put in a tweet
tweet_max_char = 240
#Here is the amount of characters a shortlink takes up
shortlink_max_char = 24

#Subreddit we are trying to extraxt posts from (no need to add the r/ in the beggining)
subreddit_to_watch = 'psychology'

#Every reddit post has an ID, here we want to store these ID's in a .txt file to avoid tweeting the same post twice.
posted_reddit_ids = 'example.txt'

#Duration your bot will wait before tweeting again in seconds
time_between_tweets = 60

#Duration the bot will sleep before restarting the main process in seconds
time_between_restarts = 120

#Keyword inside reddit title.
#Bot will only tweet posts with the keywords in this list. Reccomended to enter one keyword at a time.
#Leave List empty if you want bot to tweet all posts.
keyword_list = []

hashtags_id = '#psychology'



def setup_connection_reddit(subreddit):
    '''Connects to Reddit API'''
    print('[bot] Setting up connection with reddit')
    #Place reddit API keys here.
    reddit_api = praw.Reddit(user_agent = 'Twitter Bot'.format(subreddit),
                              client_id = 'n7TRTkXLMy2QlQ', client_secret = 'Ukf4dDG6nIHwbp8wbkqPUlwyWJo')
    return reddit_api.subreddit(subreddit)


def shorten_title(title,character_count):
    '''Shortens title if too long so that it will fit into a tweet'''
    if len(title) >= character_count:
        return title[:character_count - 1] + '…'
    else:
        return title


def tweet_creator(subreddit_info):
    '''Goes through posts on reddit and extracts a shortened link, title & ID'''
    post_links = []  # list to store our links
    post_titles = []  # list to store our titles
    post_ids = []  # list to store our id's
    print("[bot] extracting posts from sub-reddit")

    for submission in subreddit_info.new(limit=20):
        if not already_tweeted(submission.id):
            if not keyword_list:
                print("No keywords.")
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
            print("Already Tweeted")
    return post_links, post_titles, post_ids


def record_id(id):
    '''Logs reddit post ID's into our .txt file'''
    with open(posted_reddit_ids, 'a') as f:
        f.write(str(id)+ '\n')


def already_tweeted(post_id):
    '''reads through our .txt file and determines if tweet has already been posted'''
    found = 0
    with open(posted_reddit_ids, 'r') as f:
        for line in f:
            if post_id in line:
                found = 1
                break
    return found



def tweeter(post_links,post_titles,post_ids):
    '''Tweets our reddit posts'''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    #twitter_username = twitter.me().screen_name
    #print('[ OK ] Sucessfully authenticated on Twitter as @' + twitter_username)

    for post_title, post_link, post_id in zip(post_titles, post_links, post_ids):
        extra_text = ' ' + post_link #space needed to seperate the link and the title
        hashtag = ' ' + hashtags_id
        post_text = shorten_title(post_title, tweet_max_char - shortlink_max_char - 1) + extra_text + hashtag
        print('[bot] Posting this tweet to Twitter:')
        print(post_text)
        api.update_status(status = post_text)
        print('[bot] Sleeping for', time_between_tweets, 'seconds')
        time.sleep(time_between_tweets)
        print('[bot] Restarting main process...')
        record_id(post_id)




def main():
    '''Main function'''
    # If the tweet tracking file does not already exist, create it
    if not os.path.exists(posted_reddit_ids):
        with open(posted_reddit_ids, 'w'):
            pass

    subreddit = setup_connection_reddit(subreddit_to_watch)
    post_links, post_titles, post_ids = tweet_creator(subreddit)
    tweeter(post_links, post_titles, post_ids)
    print('[bot] Restarting main process in', time_between_restarts, 'seconds')
    time.sleep(time_between_restarts)
    main()

if __name__ == '__main__':
    main()
