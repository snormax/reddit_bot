import praw
import time


WAIT_TIME = 500
CHALLENGE_TEXT = "are summoned to compete in 'Rock, Paper, Scissors.' Both have 5 minutes to private message " \
                 "u/RPS_Bot with exactly 'Rock', 'Paper', OR 'Scissors' in the subject field. Matches are invalid if " \
                 "either party fails to send a valid message within 5 minutes. The victor will be announced in a " \
                 "reply to the challenge "
VALID_INPUT = ["rock", "paper", "scissors"]


def outcome(username_a, username_a_choice, username_b, username_b_choice):
    # if username_a_choice == username_b_choice: return "draw" handled elsewhere
    if username_a_choice == "rock":
        if username_b_choice == "paper":
            return username_b
        else:
            return username_a
    elif username_a_choice == "paper":
        if username_b_choice == "scissors":
            return username_b
        else:
            return username_a
    elif username_a_choice == "scissors":
        if username_b_choice == "rock":
            return username_b
        else:
            return username_a


def main():
    reddit = praw.Reddit(client_id="mc8vD0FAxRHMqA", client_secret="UP-mLKR04qYfg_RkdLNuvzNCGNA", password="aMu8AVLWXOuFpFCVMYcK", username="rps_duel_bot", user_agent="game by u/rps_duel_bot")
    print(reddit.user.me())

    while True:
        # Downtime precaution
        try:
            for mention in reddit.inbox.mentions():
                if mention.new:
                    mention.mark_read()
                    start_time = time.time()
                    end_time = start_time + WAIT_TIME
                    username_a = mention.author.name
                    username_b = None   # TODO parse mention.body for name NOT username_a break/continue if invalid
                    print(start_time, end_time, username_a, username_b)
                    mention.reply(username_b, username_a, CHALLENGE_TEXT)
                    print(5)
                    # For five minutes check unread messages, avoiding 'username mention',
                    while time.time() < end_time or (username_a_choice is not None and username_b_choice is not None):
                        for message in reddit.inbox.unread():
                            if message.subject.lower() == 'username mention':
                                continue

                            message.mark_read()
                            if message.created_utc < start_time:
                                continue
                            elif username_a_choice is None and message.author == username_a:
                                subject = message.subject.lower()
                                if subject in VALID_INPUT:
                                    username_a_choice = subject
                            elif username_b_choice is None and message.author == username_b:
                                subject = message.subject.lower()
                                if subject in VALID_INPUT:
                                    username_b_choice = subject

                    if username_b_choice is None or username_a_choice is None:
                        mention.reply("This mach is invalid due rule violation(s)")
                    elif username_a_choice == username_b_choice:
                        mention.reply("Draw!")
                    else:
                        victor = outcome(username_a, username_a_choice, username_b, username_b_choice)
                        mention.reply(victor, "is the champion!")

        except Exception as e:
            print(e)
            time.sleep(60)


if __name__ == '__main__':
    main()
