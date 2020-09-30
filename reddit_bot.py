import praw
import time


def read_from_file() -> list:
    """
    Extracts data from posts_replied_to.txt, filters, and returns the data as a list
    :return: list from file
    """
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))  # removes ""
        return posts_replied_to


# TODO find a time to do this in do_thing()
def print_to_file(posts_replied_to: list):
    """
    Dumps current posts_replied_to to file to save it
    :param posts_replied_to: current list of posts replied to
    :return: None
    """
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")


def init_bot():
    pass


def do_thing():
    pass


# TODO break this up
def main():
    # Initializing bot
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('bot subreddit')  # TODO make bot subreddit
    comments = subreddit.stream.comments()  # Alternatively subreddit.get_comments(subreddit)

    posts_replied_to = read_from_file()

    # Checking for username mentions, if responded to, and then doing the thing
    while True:
        for comment in comments:
            text = comment.body
            if 'u/botname' in text.lower() and comment.id not in posts_replied_to:  # TODO bot name or !thing
                comment.reply('hello')  # TODO do thing
                posts_replied_to.append(comment.id)
        time.sleep(3600)  # hour


if __name__ == '__main__':
    main()
