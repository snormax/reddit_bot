import json
import praw
import time
import os

WAIT_TIME = 500
CHALLENGE_TEXT = " to compete in 'Rock, Paper, Scissors.' Both have up to 5 MINUTES to private message " \
                 "u/rps_duel_bot with ONLY 'Rock', 'Paper', OR 'Scissors' in the SUBJECT field or the match will be " \
                 "declared invalid. The winner will be announced in a reply to the challenger's comment."
VALID_INPUT = ["rock", "paper", "scissors"]


def rps(user_a: str, user_a_rps: str, user_b: str, user_b_rps: str) -> str:
    """
    Determines the winner in a rps match.

    Case: if username_a_choice == username_b_choice: return "draw" handled elsewhere
    :param user_a: author
    :param user_a_rps: author's rps choice
    :param user_b: challenger
    :param user_b_rps: challengee's rps choice
    :return: username of winner
    """
    if user_a_rps == "rock":
        if user_b_rps == "paper":
            return user_b
        else:
            return user_a
    elif user_a_rps == "paper":
        if user_b_rps == "scissors":
            return user_b
        else:
            return user_a
    elif user_a_rps == "scissors":
        if user_b_rps == "rock":
            return user_b
        else:
            return user_a


def parse_body(body: str):
    """
    Parses the body of the challenger's mention/comment for name of challengee.

    u/rps_duel_bot cannot be the challengee.
    :param body: body of mention comment
    :return: challengee's username (user_b) or '-1' if invalid
    """
    # Edge case
    if body is None:
        return '-1'

    # Extract possible usernames to username_list
    username_list = [t for t in body.split() if t.startswith('u/')]

    # Check username_list
    for username in username_list:
        if username != 'u/rps_duel_bot' and username is not None:
            return username[2:]  # Up to 3 if /u/
    return "-1"


def check_mentions(reddit):
    """
    Checks for valid mentions, initiates match, checks messages

    :param reddit: Reddit object
    """
    for mention in reddit.inbox.mentions():
        if mention.new:
            print("Checking a mention...")
            mention.mark_read()
            user_a = mention.author.name

            # Parse and check for user_b
            user_b = parse_body(mention.body)
            if user_b == '-1' or user_b == user_a:
                continue
            print("UserA: %s, UserB: %s" % (user_a, user_b))

            # Send challenge reply
            reply_text = "u/" + user_a + " has challenged u/" + user_b + CHALLENGE_TEXT
            mention.reply(reply_text)

            # For five minutes check unread messages, avoiding 'username mention'
            rps_tuple = check_messages(reddit, user_a, user_b)
            user_a_rps = rps_tuple[0]
            user_b_rps = rps_tuple[1]

            # Reply with decision
            print("user_a_rps: %s, user_b_rps: %s" % (user_a_rps, user_b_rps))
            if user_b_rps is None or user_a_rps is None:
                mention.reply("This match is invalid due rule violation(s)")
            elif user_a_rps == user_b_rps:
                mention.reply("Draw!")
            else:
                winner = rps(user_a, user_a_rps, user_b, user_b_rps)
                winner_reply = "u/" + winner + " is the winner!"
                mention.reply(winner_reply)
        else:
            mention.delete()


def check_messages(reddit, user_a: str, user_b: str):
    """
    Sets a timer, continuously checks messages (until either timer or RPS choices), and returns the RPS choices

    :param reddit: Reddit object
    :param user_a: author
    :param user_b: challengee
    :return: RPS chosen by users and/or None
    """
    start_time = time.time()
    stop_time = start_time + WAIT_TIME
    user_a_rps = None
    user_b_rps = None

    print("Start Time: %s, Stop Time: %s" % (start_time, stop_time))

    while True:
        for message in reddit.inbox.unread():
            current_time = time.time()
            if current_time >= stop_time or (user_a_rps is not None and user_b_rps is not None):
                return None, None
            # Check if message is old: /message/ may be older than /mention/
            if message.created_utc < start_time:
                message.mark_read()
                continue

            # Subject parsing
            elif user_a_rps is None and message.author.name == user_a:
                subject = message.subject.lower()
                if subject in VALID_INPUT:
                    user_a_rps = subject.lower()
            elif user_b_rps is None and message.author.name == user_b:
                subject = message.subject.lower()
                if subject in VALID_INPUT:
                    user_b_rps = subject.lower()

    print("User_A chose: %s, User_B chose: %s" % (user_a_rps, user_b_rps))
    return user_a_rps, user_b_rps


def log_in():
    """
    For credential security:
    Testing can be done using locally stored credentials (not hosted to GitHub)
    Heroku configuration file set with credentials as well
    :return: Reddit object
    """
    # True if testing locally
    testing = False

    if not testing:
        # REDDIT_CLIENT_ID = os.environ['reddit_client_id']
        # REDDIT_CLIENT_SECRET = os.environ['reddit_client_secret']
        # REDDIT_USERNAME = os.environ['reddit_username']
        # REDDIT_PASSWORD = os.environ['reddit_password']
        # REDDIT_USER_AGENT = os.environ['reddit_user_agent']
        REDDIT_CLIENT_ID = "mc8vD0FAxRHMqA"
        REDDIT_CLIENT_SECRET = "UP-mLKR04qYfg_RkdLNuvzNCGNA"
        REDDIT_USERNAME = "rps_duel_bot"
        REDDIT_PASSWORD = "aMu8AVLWXOuFpFCVMYcK"
        REDDIT_USER_AGENT = "rps game by u/rps_duel_bot"

    else:
        credentials = open("credentials.json", "r")
        credentials_json = json.load(credentials)
        credentials.close()

        REDDIT_CLIENT_ID = credentials_json['data']['REDDIT_CLIENT_ID']
        REDDIT_CLIENT_SECRET = credentials_json['data']['REDDIT_CLIENT_SECRET']
        REDDIT_USERNAME = credentials_json['data']['REDDIT_USERNAME']
        REDDIT_PASSWORD = credentials_json['data']['REDDIT_PASSWORD']
        REDDIT_USER_AGENT = credentials_json['data']['REDDIT_USER_AGENT']

    return praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
                       password=REDDIT_PASSWORD, username=REDDIT_USERNAME, user_agent=REDDIT_USER_AGENT)


def main():
    # Log-in and test
    reddit = log_in()
    print("Logged in as: %s" % (reddit.user.me()))

    while True:
        # Downtime precaution
        try:
            check_mentions(reddit)
        except Exception as e:
            print(e)
            time.sleep(60)


if __name__ == '__main__':
    main()
