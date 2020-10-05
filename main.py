import praw
import time
from os import environ
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
            return username[2:]     # Up to 3 if /u/
    return "-1"


def check_messages():
    # TODO
    pass


def check_mentions():
    # TODO
    pass


def main():
    # Log-in
    REDDIT_CLIENT_ID = environ['REDDIT_CLIENT_ID']
    REDDIT_CLIENT_SECRET = environ['REDDIT_CLIENT_SECRET']
    REDDIT_USERNAME = environ['REDDIT_USERNAME']
    REDDIT_PASSWORD = environ['REDDIT_PASSWORD']
    REDDIT_USER_AGENT = environ['REDDIT_USER_AGENT']
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
                         password=REDDIT_PASSWORD, username=REDDIT_USERNAME, user_agent=REDDIT_USER_AGENT)

    # Check if logged-in correctly
    print(reddit.user.me())

    while True:
        # Downtime precaution
        try:
            for mention in reddit.inbox.mentions():
                if mention.new:
                    print("Checking message...")
                    mention.mark_read()
                    start_time = time.time()
                    end_time = start_time + WAIT_TIME
                    user_a = mention.author.name
                    user_a_rps = None
                    user_b_rps = None

                    # Parse and check for user_b
                    user_b = parse_body(mention.body)
                    if user_b == '-1' or user_b == user_a:
                        continue

                    print("Start Time: %s, End Time: %s, UserA: %s, UserB %s" % (start_time, end_time, user_a, user_b))

                    # Send challenge reply
                    reply_text = "u/" + user_a + " has challenged u/" + user_b + CHALLENGE_TEXT
                    mention.reply(reply_text)

                    # For five minutes check unread messages, avoiding 'username mention',
                    while True:
                        current_time = time.time()
                        if current_time >= end_time or (user_a_rps is not None and user_b_rps is not None):
                            break
                        for message in reddit.inbox.unread():
                            # Checks if username mention and if so does NOT mark as read
                            if message.subject.lower() == 'username mention':
                                continue

                            # Get this over with
                            message.mark_read()

                            # Old mail check
                            if message.created_utc < start_time:
                                continue

                            # Subject check
                            elif user_a_rps is None and message.author.name == user_a:
                                subject = message.subject.lower()
                                if subject in VALID_INPUT:
                                    user_a_rps = subject
                            elif user_b_rps is None and message.author.name == user_b:
                                subject = message.subject.lower()
                                if subject in VALID_INPUT:
                                    user_b_rps = subject
                                # NOT elif continue -- give them time for another attempt

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

        except Exception as e:
            print(e)
            time.sleep(60)


if __name__ == '__main__':
    main()
