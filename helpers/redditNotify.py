import praw
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def notify_stock_reddit_submission(description):
    stock_thread = None
    try:
        reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                             client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                             user_agent='windows:com.redditbot.roguestocknotifier:v1 (by /u/bennykgarcia)',
                             username=os.getenv('REDDIT_USERNAME'),
                             password=os.getenv('REDDIT_PASSWORD'))

        subreddit = reddit.subreddit('homegym')

        for submission in subreddit.hot(limit=5):
            if 'stock and shipping' in submission.title.lower().strip() and submission.stickied:
                stock_thread = submission
                break
        if stock_thread is None:
            print(f'Stock thread not found')
            return
        stock_thread.reply(description)
    except Exception as e1:
        print(f'{type(e1)} - {e1}: Unable to post Reddit reply')
