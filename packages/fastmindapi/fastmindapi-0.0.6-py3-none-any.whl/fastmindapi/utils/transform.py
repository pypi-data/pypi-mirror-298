import numpy as np
import math

def convert_numpy_float32_to_float(d):
    if isinstance(d, dict):
        return {k: convert_numpy_float32_to_float(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [convert_numpy_float32_to_float(item) for item in d]
    elif isinstance(d, np.float32):
        return float(d)
    else:
        return d
    
def convert_openai_logprobs(logprobs):
    logprobs = logprobs.model_dump()
    logits_list = []
    for token_info in logprobs["content"]:
        logits = {
            "token": token_info["token"],
            "pred_token": [],
            # "logits": [],
            "probs": [],
            "logprobs": []
        }
        for predict_info in token_info["top_logprobs"]:
            logits["pred_token"].append(predict_info["token"])
            logits["logprobs"].append(round(predict_info["logprob"],4))
            logits["probs"].append(round(math.exp(predict_info["logprob"]),4))
        logits_list.append(logits)
    return logits_list