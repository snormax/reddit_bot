import praw
import time

# Enter your correct Reddit information into the variable below
userAgent = 'Enter Bot name'
cID = 'Enter your personal use script'
cSC = 'Enter you client secret'
userN = 'Enter your Reddit username'
userP = 'Enter your Reddit password'
numFound = 0
reddit = praw.Reddit(user_agent=userAgent, client_id=cID, client_secret=cSC, username=userN, password=userP)

subreddit = reddit.subreddit('weather')  # any subreddit you want to monitor

bot_phrase = 'Aw shucks, looks like I am staying in >:('  # phrase that the bot replies with

keywords = {'Cold', 'chicago', 'polar', 'vortex'}  # makes a set of keywords to find in subreddits

for submission in subreddit.hot(limit=10):  # this views the top 10 posts in that subbreddit
    n_title = submission.title.lower()  # makes the post title lowercase so we can compare our keywords with it.
    for i in keywords:  # goes through our keywords
        if i in n_title:  # if one of our keywords matches a title in the top 10 of the subreddit
            numFound = numFound + 1
            print('Bot replying to: ')  # replies and outputs to the command line
            print("Title: ", submission.title)
            print("Text: ", submission.selftext)
            print("Score: ", submission.score)
            print("---------------------------------")
            print('Bot saying: ', bot_phrase)
            print()
            submission.reply(bot_phrase)

if numFound == 0:
    print()
    print("Sorry, didn't find any posts with those keywords, try again!")

# ANOTHER BOT -----------------------------------

r = reddit
r.login()

already_done = []
prawWords = ['praw', 'reddit_api', 'mellort']

while True:
    subreddit = r.get_subreddit('learnpython')
    for submission in subreddit.get_hot(limit=10):
        op_text = submission.selftext.lower()
        has_praw = any(string in op_text for string in prawWords)
        # Test if it contains a PRAW-related question
        if submission.id not in already_done and has_praw:
            msg = '[PRAW related thread](%s)' % submission.short_link
            r.send_message('_Daimon_', 'PRAW Thread', msg)
            already_done.append(submission.id)
    time.sleep(1800)
