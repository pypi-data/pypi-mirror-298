import json
import logging
import time
from typing import List, Dict
from pathlib import Path

import tweepy
import click

logging.basicConfig(level=logging.INFO)

CONFIG_DIR = Path.home() / ".twitter_scraper"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_bearer_token():
    config = load_config()
    return config.get("bearer_token")


CLIENT = None


def init_client():
    global CLIENT
    bearer_token = get_bearer_token()
    if not bearer_token:
        raise ValueError(
            "Bearer token not set. Run 'python scrape.py setup' to configure."
        )
    CLIENT = tweepy.Client(bearer_token)


def get_user_id(username: str) -> int:
    if not CLIENT:
        init_client()
    user = CLIENT.get_user(username=username)
    if user.data:
        return user.data.id
    raise ValueError(f"User {username} not found")


def get_latest_tweets(user_id: int, count: int, retry: bool = False) -> List[Dict]:
    if not CLIENT:
        init_client()
    tweets = []
    tweet_fields = [
        "note_tweet",
        "created_at",
        "text",
        "referenced_tweets",
        "author_id",
        "in_reply_to_user_id",
        "public_metrics",
    ]
    expansions = [
        "referenced_tweets.id",
        "referenced_tweets.id.author_id",
        "in_reply_to_user_id",
    ]

    try:
        for tweet in tweepy.Paginator(
            CLIENT.get_users_tweets,
            user_id,
            max_results=100,
            tweet_fields=tweet_fields,
            expansions=expansions,
        ).flatten(limit=count):
            tweets.append(tweet.data)
            logging.info(f"Tweet saved: {tweet.data['id']}")
    except tweepy.TooManyRequests:
        if retry:
            logging.warning("Rate limit reached. Retrying after 15 minutes.")
            time.sleep(900)  # Wait for 15 minutes
            return get_latest_tweets(user_id, count, retry)
        else:
            logging.warning("Rate limit reached. Stopping.")
    except tweepy.TwitterServerError:
        logging.error("Twitter server error. Stopping.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        return tweets


def save_tweets_to_json(tweets: List[Dict], filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=4)
    logging.info(f"All tweets saved to {filename}")


def get_tweet_by_id(tweet_id: str) -> Dict:
    if not CLIENT:
        init_client()
    tweet = CLIENT.get_tweet(
        tweet_id,
        expansions=["author_id"],
        tweet_fields=["created_at", "text", "note_tweet"],
    )
    if tweet.data:
        return tweet.data.data
    raise ValueError(f"Tweet with id {tweet_id} not found")


def tweets_to_txt(tweets: List[Dict], output_txt: str):
    sorted_tweets = sorted(
        tweets, key=lambda x: x["public_metrics"]["like_count"], reverse=True
    )

    with open(output_txt, "w", encoding="utf-8") as txt_file:
        for tweet in sorted_tweets:
            text = tweet.get("note_tweet", {}).get("text") or tweet["text"]
            txt_file.write(f"{text}\n")
            txt_file.write(f"Created at: {tweet['created_at']}\n")
            txt_file.write(f"Likes: {tweet['public_metrics']['like_count']}\n")
            txt_file.write("\n---\n\n")

    print(f"Tweets sorted by likes and saved to {output_txt}")


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--token",
    prompt="Enter your Twitter Bearer Token",
    hide_input=True,
    help="Twitter Bearer Token",
)
def setup(token):
    """Set up the Twitter Bearer Token."""
    config = load_config()
    config["bearer_token"] = token
    save_config(config)
    click.echo("Bearer Token saved successfully.")


@cli.command()
@click.argument("username")
@click.argument("count", type=int)
@click.option("--output", default="{username}_max_tweets.json", help="Output JSON file")
@click.option("--to-txt", is_flag=True, help="Convert tweets to text file")
@click.option(
    "--retry", is_flag=True, help="Retry on rate limit with 15-minute backoff"
)
def fetch_tweets(username: str, count: int, output: str, to_txt: bool, retry: bool):
    """Fetch tweets for a given username."""
    latest_tweets = []
    try:
        user_id = get_user_id(username)
        latest_tweets = get_latest_tweets(user_id, count, retry)
        output_file = output.format(username=username)
        save_tweets_to_json(latest_tweets, output_file)
        click.echo(
            f"Saved {len(latest_tweets)} tweets from {username} to {Path(output_file).resolve()}"
        )

        if to_txt:
            txt_output = output_file.replace(".json", ".txt")
            tweets_to_txt(latest_tweets, txt_output)
            click.echo(f"Converted tweets to text file: {Path(txt_output).resolve()}")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)
    finally:
        if latest_tweets:
            temp_file = f"{username}_temp_tweets.json"
            save_tweets_to_json(latest_tweets, temp_file)
            click.echo(f"Saved progress to temporary file: {Path(temp_file).resolve()}")


@cli.command()
@click.argument("tweet_id")
def get_tweet(tweet_id: str):
    """Get a specific tweet by ID."""
    try:
        tweet = get_tweet_by_id(tweet_id)
        click.echo(f"Tweet data: {json.dumps(tweet, indent=2)}")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
