import os
import praw
from dotenv import load_dotenv


load_dotenv()  # loads .env into env

reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent=os.environ.get("REDDIT_USER_AGENT", "hackathon_app"),
    username=os.environ.get("REDDIT_USERNAME"),
    password=os.environ.get("REDDIT_PASSWORD")
)


def search_product_mentions(keywords, limit=5):
    results = {}

    for keyword in keywords:
        posts = []
        try:
            for submission in reddit.subreddit("all").search(keyword, sort="hot", limit=limit):
                posts.append({
                    "title": submission.title,
                    "score": submission.score,
                    "comments": submission.num_comments,
                    "subreddit": submission.subreddit.display_name,
                    "url": submission.url
                })

            results[keyword] = posts

        except Exception as e:
            results[keyword] = []

    return results


# Example usage
products = ["iPhone 16", "Tesla", "Oculus"]
product_trends = search_product_mentions(products)

for product, posts in product_trends.items():
    print(f"\n🔹 {product.upper()} MENTIONS:")
    if posts:
        for post in posts:
            print(f"- {post['title']} ({post['score']} upvotes in r/{post['subreddit']})")
    else:
        print("No recent mentions found.")
