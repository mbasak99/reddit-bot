import praw
import prawcore
from dotenv import load_dotenv
from pathlib import Path
import os
import time
from twilio.rest import Client

""" SETUP FOR SCRIPT """
# DOTENV
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# REDDIT
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    username=os.getenv("REDDIT_USERNAME"),
    user_agent="python reddit bot"
)

# TWILIO
client = Client(os.getenv("TWILIO_ACC_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

""" REMEMBER THAT .ENV WILL ALWAYS RETURN STR SO CONVERT NUMBERS TO THEIR RESPECTIVE TYPES """


def main():
    print('running...')

    # Test the reddit config works
    # print(reddit.user.me())

    reddit.read_only = True

    # Get submissions from subreddit
    result = None
    while True:
        try:
            for submission in reddit.subreddit(os.getenv("SUBREDDIT")).new(limit=1):
                if result != submission.title and "3080" in submission.title:
                    result = submission.title
                    print(submission.title, submission.url)
                    print('Sending text message now...')
                    client.messages.create(body="Possible RTX 3080: " + submission.shortlink,
                                           from_=os.getenv("TWILIO_PHONE_NUM"), to=os.getenv("PHONE_NUM"))

            time.sleep(int(os.getenv("REQUEST_REFRESH_SECONDS")))
        except prawcore.exceptions.ResponseException as e:
            print('response error: ', e)
            time.sleep(30)


if __name__ == '__main__':
    main()
