import praw
import time
"""
Generic bot build with exception handling and notes.

TODO:
Go to: https://www.reddit.com/prefs/apps/ and select Create App
Update praw.ini with the above
"""


def read_from_file() -> list:
    """
    Extracts data from posts_replied_to.txt, filters, and returns the data as a list

    :return: list from file
    """

    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))  # removes "" entries
        return posts_replied_to


def print_to_file(posts_replied_to: list):
    """
    Dumps current posts_replied_to to file to save it

    :param posts_replied_to: current list of posts replied to
    """

    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")


def init_bot():
    """
    Initializes bot and opens stream of comments

    Alternatively:
    To grab all once: return subreddit.get_comments(subreddit)
    (may require submission.comments.replace_more(limit=0) to exclude "MoreComments")
    To stream new comments (not 100 historical): return subreddit.stream.comments(skip_existing=True)
    :return: comment stream or the like
    """

    r = praw.Reddit('bot1')  # TODO update PRAW with details
    subreddit = r.subreddit('bot subreddit')  # TODO make bot subreddit
    return subreddit.stream.comments()


def do_thing(comments, posts_replied_to):
    """
    Does the thing!
    :param comments: stream of comments
    :param posts_replied_to: working list of posts replied to
    :return:
    """

    while True:
        try:
            for comment in comments:
                text = comment.body
                if 'u/botname' in text.lower() and comment.id not in posts_replied_to:  # TODO bot name or !thing
                    # TODO do thing
                    posts_replied_to.append(comment.id)
            time.sleep(3600)  # TODO decide duration (currently 1 hour / 3600 seconds)
        except Exception as e:
            print(e)
            print_to_file(posts_replied_to)
            time.sleep(60)


def main():
    # Generate working list of posts replied to by the bot in the past
    posts_replied_to = read_from_file()

    # Initialize bot and access comment stream
    comments = init_bot()

    # Checking for username mentions, if responded to, and then doing the thing
    do_thing(comments, posts_replied_to)


if __name__ == '__main__':
    main()
