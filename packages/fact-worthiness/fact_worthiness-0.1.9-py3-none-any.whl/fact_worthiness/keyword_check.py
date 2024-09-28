import yaml
import sys
import time
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

claim_indicators = [
    "according to",
    "studies show",
    "research indicates",
    "experts say",
    "scientists claim",
    "reportedly",
    "allegedly",
    "sources say",
    "it is said that",
    "it is believed that",
    "breaking news",
    "exclusive",
    "shocking",
    "unbelievable",
    "groundbreaking",
    "controversial",
    "debunked",
    "fact check",
    "fake news",
    "hoax",
    "conspiracy",
    "official statement",
    "leaked",
    "anonymous sources",
    "insider information",
    "confirmed",
    "denied",
    "disputed",
    "evidence suggests",
    "new study",
    "poll shows",
    "survey reveals",
    "statistics indicate",
    "in my opinion",
    "I believe",
    "proves that",
    "disproves",
    "demonstrates",
    "refutes",
    "debunks",
    "exposes",
    "reveals"
]



def filter_tweets_by_claim_indicators(tweets: list) -> list:
    """Filter tweets by claim indicators.

    Parameters
    ----------
    tweets : list
        The list of tweets to filter.

    Returns
    -------
    list
        The filtered list of tweets.
    """
    try:

        def check_tweet(tweet):
            matches = any(indicator.lower() in tweet.lower() for indicator in claim_indicators)
            return (tweet, 'Y' if matches else 'N')

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(check_tweet, tweets))

        return results

    except Exception as e:
        logger.error(f"An error occurred while filtering tweets by claim indicators: {e}")
        raise
