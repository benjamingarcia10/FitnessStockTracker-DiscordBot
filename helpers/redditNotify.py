import praw
import os
from dotenv import load_dotenv

load_dotenv(override=True)


# Post notification to r/homegym Stock and Shipping pinned/stickied thread
def notify_stock_reddit_submission(description):
    stock_thread = None
    try:
        reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                             client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                             user_agent='windows:com.redditbot.roguestocknotifier:v1 (by /u/bennykgarcia)',
                             username=os.getenv('REDDIT_USERNAME'),
                             password=os.getenv('REDDIT_PASSWORD'))

        # Retrieve r/homegym subreddit object
        subreddit = reddit.subreddit('homegym')

        # Get the stickied thread with Stock and Shipping in title
        for submission in subreddit.hot(limit=5):
            if 'stock and shipping' in submission.title.lower().strip() and submission.stickied:
                stock_thread = submission
                break
        if stock_thread is None:
            print(f'Stock thread not found')
            return
        # Post reply based on passed in argument
        stock_thread.reply(description)
    except Exception as e1:
        print(f'{type(e1)} - {e1}: Unable to post Reddit reply')
