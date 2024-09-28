import sys
import yaml
import numpy as np
from loguru import logger
from tokenizers import Tokenizer
import onnxruntime as ort
import os


package_dir = os.path.dirname(__file__)

tokenizer = Tokenizer.from_file(os.path.join(package_dir, "models","onnx_model","tokenizer.json"))

model_path = os.path.join(package_dir,"models","onnx_model","model_quantized.onnx")


session = ort.InferenceSession(model_path)

def preprocess(text, max_length=512):
    """Preprocesses the input text for NER.

    Parameters
    ----------
    text : str
        The input text to preprocess.
    max_length : int, optional
        The maximum length of the input text, by default 512.

    Returns
    -------
    dict
        A dictionary containing the preprocessed input, including 'input_ids', 'attention_mask', and 'token_type_ids'.
    """    
    encoded = tokenizer.encode(text)
    input_ids = np.array(encoded.ids[:max_length]).reshape(1, -1)
    attention_mask = np.array(encoded.attention_mask[:max_length]).reshape(1, -1)
    token_type_ids = np.zeros_like(input_ids)
    return {'input_ids': input_ids, 'attention_mask': attention_mask, 'token_type_ids': token_type_ids}

def perform_ner(tweet: str) -> str:
    """Performs named entity recognition (NER) on the given tweet.

    Parameters
    ----------
    tweet : str
        The input tweet to perform NER on.

    Returns
    -------
    str
        'Y' if the tweet contains entities, 'N' otherwise.
    """    
    try:
        logger.debug(f"Processing tweet for NER: {tweet}")
        inputs = preprocess(tweet)
        input_names = [i.name for i in session.get_inputs()]
        session_inputs = {name: inputs[name] for name in input_names}
        outputs = session.run(None, session_inputs)
        entities = extract_entities(outputs, inputs)
        has_entities = 'Y' if entities else 'N'
        return has_entities
    except Exception as e:
        logger.error(f"Error processing tweet for NER: {tweet}. Error: {e}")
        return 'N'

def extract_entities(outputs: list, inputs: dict) -> list:
    """Extracts entities from the model outputs.

    Parameters
    ----------
    outputs : list
        The outputs from the ONNX model.
    inputs : dict
        The preprocessed inputs.

    Returns
    -------
    list
        A list of tuples representing the entities found in the tweet. Each tuple contains the token and its corresponding label.
    """    
    logits = outputs[0]
    input_ids = inputs['input_ids'][0]
    attention_mask = inputs['attention_mask'][0]
    predictions = np.argmax(logits, axis=-1)
    if predictions.shape[1] != input_ids.shape[0]:
        logger.error("Mismatch between tokenized input length and predictions length.")
        return []
    entities = []
    for i in range(predictions.shape[1]):
        label = predictions[0][i]
        if label != 0 and attention_mask[i] == 1:
            token = tokenizer.decode([input_ids[i]])
            entities.append((token, label))

    return entities
