

import pickle

TOKENIZER_PATH = "app/prediction_models/tokenizer.pkl"

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)