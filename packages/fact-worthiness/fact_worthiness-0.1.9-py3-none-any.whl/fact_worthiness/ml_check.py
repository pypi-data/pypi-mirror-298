import yaml
import numpy as np
import onnxruntime as ort
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from tokenizers import Tokenizer
import os

package_dir = os.path.dirname(__file__)

model_path = os.path.join(package_dir,"models","classification_model.onnx")


def load_model(model_path: str) -> ort.InferenceSession:
    """Load the ONNX model from the given path.

    Parameters
    ----------
    model_path : str
        The path to the ONNX model file.

    Returns
    -------
    ort.InferenceSession
        The loaded ONNX model as an InferenceSession object.
    """    
    try:
        ort_session = ort.InferenceSession(model_path)
        return ort_session
    except Exception as e:
        logger.error(f"Error loading model from {model_path}: {e}")
        raise

def preprocess_tweet(tweet: str, max_seq_length=128) -> dict:
    """Preprocesses a tweet for classification.

    Parameters
    ----------
    tweet : str
        The tweet to preprocess.
    max_seq_length : int, optional
        The maximum sequence length for the input, by default 128

    Returns
    -------
    dict
        A dictionary containing the preprocessed input for the model.
    """    
    tokenizer = Tokenizer.from_pretrained('bert-base-uncased')
    encoded = tokenizer.encode(tweet)
    input_ids = np.array(encoded.ids[:max_seq_length]).reshape(1, -1).astype(np.float32)
    attention_mask = np.array(encoded.attention_mask[:max_seq_length]).reshape(1, -1).astype(np.float32)
    token_type_ids = np.zeros_like(input_ids).astype(np.float32)

    if input_ids.shape[1] < max_seq_length:
        padding_length = max_seq_length - input_ids.shape[1]
        input_ids = np.pad(input_ids, ((0, 0), (0, padding_length)), mode='constant')
        attention_mask = np.pad(attention_mask, ((0, 0), (0, padding_length)), mode='constant')
        token_type_ids = np.pad(token_type_ids, ((0, 0), (0, padding_length)), mode='constant')

    return {'input_ids': input_ids, 'attention_mask': attention_mask, 'token_type_ids': token_type_ids, 'embedding_1_input': input_ids}

def perform_ml_classification(tweet:str, ml_threshold: int) -> str:
    """Perform ML classification on a given tweet.

    Parameters
    ----------
    tweet : str
        The tweet to classify.
    ml_threshold : float, optional

    Returns
    -------
    str
        The classification result ('Y' for positive, 'N' for negative).
    """    
    try:
        ort_session = load_model(model_path)

        inputs = preprocess_tweet(tweet)
        input_names = [i.name for i in ort_session.get_inputs()]
        session_inputs = {name: inputs[name] for name in input_names}
        outputs = ort_session.run(None, session_inputs)

        prediction = outputs[0][0][0]
        return 'Y' if prediction > ml_threshold else 'N'
    except Exception as e:
        logger.error(f"Error processing tweet: {tweet}. Error: {e}")
        raise

def classify_tweets(tweets: list, ml_threshold = 0.5) -> list:
    """Classify a list of tweets using ML model.

    Parameters
    ----------
    tweets : list
        The list of tweets to classify.
    ml_threshold : float, optional

    Returns
    -------
    list
        The classification results for each tweet.
    """    
    try:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(perform_ml_classification, tweet, ml_threshold) for tweet in tweets]
            return [future.result() for future in as_completed(futures)]
    except Exception as e:
        logger.error(f"An error occurred while classifying tweets: {e}")
        raise
