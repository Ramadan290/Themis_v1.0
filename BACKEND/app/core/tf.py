from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore

# === Constants ===
MAX_LEN = 50
PADDING_TYPE = "post"
TRUNCATING_TYPE = "post"

# === Padding Function ===
def pad_text_sequences(tokenizer, texts: list[str]):
    sequences = tokenizer.texts_to_sequences(texts)
    return pad_sequences(
        sequences,
        maxlen=MAX_LEN,
        padding=PADDING_TYPE,
        truncating=TRUNCATING_TYPE
    )

# === Helper to Run a TFLite model ===
def run_tflite_model(interpreter, input_data: np.ndarray):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])



def run_tflite_encoder(interpreter_path: str, input_array: np.ndarray) -> np.ndarray:
    interpreter = tf.lite.Interpreter(model_path=interpreter_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], input_array.astype(np.float32))
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])  # Latent vector
    return output_data