import yaml
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed


def filter_tweet(tweet: str, min_words: int) -> str:
    """Filters a tweet based on the minimum number of words required.

    Parameters:
    ----------------
    - tweet (str): The tweet to be filtered.
    - min_words (int): The minimum number of words required.

    Returns:
    ----------------
    - str: The filtered tweet if it meets the minimum word requirement, otherwise None.
    """
    try:
        words = tweet.split()
        if len(words) >= min_words:
            return tweet
    except Exception as e:
        logger.error(f"Error processing tweet: {tweet}. Error: {e}")
    return None


def filter_tweets_by_length(tweets: list, min_words: int) -> list:
    """Filters a list of tweets based on the minimum number of words required.

    Parameters:
    ----------------
    - tweets (list): The list of tweets to be filtered.
    - min_words (int): The minimum number of words required.

    Returns:
    ----------------
    - list: The filtered list of tweets that meet the minimum word requirement.
    """
    try:
        filtered_tweets = []

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(filter_tweet, tweet, min_words): tweet for tweet in tweets}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    filtered_tweets.append(result)
        return filtered_tweets

    except Exception as e:
        logger.error(f"An error occurred while filtering tweets by length: {e}")
        raise
    