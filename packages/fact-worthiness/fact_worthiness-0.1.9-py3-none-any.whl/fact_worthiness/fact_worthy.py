import yaml
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from .len_check import filter_tweets_by_length
from .ner_check import perform_ner
from .ml_check import perform_ml_classification
from .keyword_check import filter_tweets_by_claim_indicators

def process_tweet(tweet: str, min_words: int, ml_threshold: float) -> tuple:
    """Process a tweet and return a tuple containing various evaluation results.

    Parameters
    ----------
    tweet : str
        The tweet to be processed.
    min_words : int
        The minimum number of words required for the tweet to pass the length filter.
    ml_threshold : float
        The threshold value for ML classification.

    Returns
    -------
    tuple
        A tuple containing the tweet, keyword indicator flag, entity presence, and ML classification result.
    """
    try:
        filtered_tweets = filter_tweets_by_length(tweets=[tweet], min_words=min_words)
        if not filtered_tweets:
            return (tweet, 'N', 'N', 'N')

        keyword_result = filter_tweets_by_claim_indicators(tweets=[tweet])
        keyword_indicator_flag = keyword_result[0][1]
        has_entities = perform_ner(tweet)
        ml_classification = perform_ml_classification(tweet, ml_threshold)

        return (tweet, keyword_indicator_flag, has_entities, ml_classification)
    except Exception as e:
        logger.error(f"An error occurred while processing a tweet: {tweet}. Error: {e}")
        return None

def check_worthiness(input_tweets: list, min_words: int, ml_threshold: float = 0.5) -> list:
    """Check the worthiness of input tweets.

    Parameters
    ----------
    input_tweets : list
        A list of tweets to be checked.
    min_words : int
        The minimum number of words required for a tweet to pass the length filter.
    ml_threshold : float, optional
        The threshold value for ML classification, defaults to 0.5.

    Returns
    -------
    list
        A list of tuples containing the tweet, keyword indicator flag, entity presence, and ML classification result.
    """
    try:
        logger.info("Starting worthiness check for tweets.")
        filtered_tweets = filter_tweets_by_length(tweets=input_tweets, min_words=min_words)
        failed_tweets = [tweet for tweet in input_tweets if tweet not in filtered_tweets]

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_tweet, tweet, min_words, ml_threshold) for tweet in filtered_tweets]
            final_results = [future.result() for future in as_completed(futures) if future.result() is not None]

        # Append failed tweets with all flags set to 'N'
        final_results.extend([(tweet, 'N', 'N', 'N') for tweet in failed_tweets])

        logger.info(f"Worthiness check completed.")
        return final_results

    except Exception as e:
        logger.error(f"An error occurred while checking the worthiness of tweets. Error: {e}")
        raise

def vote_on_worthiness(input_tweets: list, min_words: int, ml_threshold: float = 0.5) -> dict:
    """Determine the worthiness of tweets based on voting.

    Parameters
    ----------
    input_tweets : list
        A list of tweets to be checked.
    min_words : int
        The minimum number of words required for a tweet to pass the length filter.
    ml_threshold : float, optional
        The threshold value for ML classification, defaults to 0.5.

    Returns
    -------
    dict
        A dictionary with tweet text as key and 'N' or 'Y' as value based on the majority of flags.
    """
    results = check_worthiness(input_tweets, min_words, ml_threshold)
    worthiness_dict = {}

    for result in results:
        tweet, keyword_flag, ner_flag, ml_flag = result
        flags = [keyword_flag, ner_flag, ml_flag]
        y_count = flags.count('Y')
        n_count = flags.count('N')

        if y_count > n_count:
            worthiness_dict[tweet] = 'Y'
        else:
            worthiness_dict[tweet] = 'N'

    return worthiness_dict
