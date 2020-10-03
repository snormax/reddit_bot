import praw
import time
# TODO u/ or /u/
WAIT_TIME = 500
CHALLENGE_TEXT = "to compete in 'Rock, Paper, Scissors.' Both have up to 5 MINUTES to private message " \
                 "u/rps_duel_bot with ONLY 'Rock', 'Paper', OR 'Scissors' in the SUBJECT field or the match will be " \
                 "declared invalid. The winner will be announced in a reply to the challenger's comment"
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
            return username[2:]
    return "-1"


def main():
    # Log-in
    reddit = praw.Reddit(client_id="mc8vD0FAxRHMqA", client_secret="UP-mLKR04qYfg_RkdLNuvzNCGNA",
                         password="aMu8AVLWXOuFpFCVMYcK", username="rps_duel_bot", user_agent="game by u/rps_duel_bot")

    # Check if logged-in correctly
    print(reddit.user.me())

    while True:
        # Downtime precaution
        try:
            for mention in reddit.inbox.mentions():
                if mention.new:
                    mention.mark_read()
                    start_time = time.time()
                    end_time = start_time + WAIT_TIME
                    user_a = mention.author.name
                    user_a_rps = None
                    user_b_rps = None

                    # Parse and check for user_b
                    user_b = parse_body(mention.body)
                    if user_b == '-1':
                        continue

                    print(start_time, end_time, user_a, user_b)  # TODO

                    # Send challenge reply
                    mention.reply('u/' + user_a, "has challenged", 'u/' + user_b, CHALLENGE_TEXT)

                    # For five minutes check unread messages, avoiding 'username mention',
                    while time.time() < end_time or (user_a_rps is not None and user_b_rps is not None):
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
                    if user_b_rps is None or user_a_rps is None:
                        mention.reply("This mach is invalid due rule violation(s)")
                    elif user_a_rps == user_b_rps:
                        mention.reply("Draw!")
                    else:
                        winner = rps(user_a, user_a_rps, user_b, user_b_rps)
                        mention.reply("u/" + winner, "is the winner!")

        except Exception as e:
            print(e)
            time.sleep(60)


if __name__ == '__main__':
    main()
