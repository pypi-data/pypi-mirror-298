from ...server.router.openai import ChatMessage
from ...utils.transform import convert_numpy_float32_to_float
from ... import logger

class LlamacppLLM:
    def __init__(self, model):
        self.model = model

    @classmethod
    def from_path(cls, model_path: str):
        from llama_cpp import Llama
        return cls(Llama(model_path, n_gpu_layers=-1, logits_all=True))
    
    def __call__(self, input_text: str, max_new_tokens: int=256):
        response = self.model(input_text, max_tokens=max_new_tokens)
        output_text = response["choices"][0]["text"]
        return output_text
        # {"id":"cmpl-bab2b133-cf08-43aa-8ea0-7c4b109b9cf4","object":"text_completion","created":1726721257,"model":"/Users/wumengsong/Resource/gguf/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf","choices":[{"text":" I'm a beginner and I'ts my first time playing this game. I","index":0,"logprobs":null,"finish_reason":"length"}],"usage":{"prompt_tokens":9,"completion_tokens":16,"total_tokens":25}}

    def generate(self,
                 input_text: str,
                 max_new_tokens: int = 256,
                 return_logits: bool = False,
                 logits_top_k: int = 10,
                 stop_strings: list[str] = None):
        response = self.model(input_text, 
                              max_tokens=max_new_tokens,
                              logprobs = logits_top_k if return_logits else None,
                              stop = stop_strings,
                              echo = True,
                              )
        full_text = response["choices"][0]["text"]
        output_text = full_text[len(input_text):]

        full_id_list = self.model.tokenize(full_text.encode('utf-8'))
        input_id_list = self.model.tokenize(input_text.encode('utf-8'))
        full_token_list = [self.model.detokenize([full_id], special=True) for full_id in full_id_list]
        input_token_list = full_token_list[:len(input_id_list)]
        logits_list = [{"id": full_id_list[0], "token": full_token_list[0]}, 
                       {"id": full_id_list[1], "token": full_token_list[1]}]
        if return_logits:
            import math
            logprobs = convert_numpy_float32_to_float(response["choices"][0]["logprobs"])
            for i in range(1, len(full_id_list)-1):
                logits = {
                    "id": full_id_list[i+1],
                    "token": full_token_list[i+1],
                    "pred_id": [],
                    "pred_token": [],
                    # "logits": [],
                    "probs": [],
                    "logprobs": []
                }
                for token in logprobs["top_logprobs"][i]:
                    logits["pred_id"].append(self.model.tokenize(token.encode('utf-8'),add_bos=False,special=True)[0])
                    logits["pred_token"].append(token)
                    logits["logprobs"].append(round(logprobs["top_logprobs"][i][token],4))
                    logits["probs"].append(round(math.exp(logprobs["top_logprobs"][i][token]),4))
                logits_list.append(logits)

        generation_output = {"output_text": output_text,
                             "input_id_list": input_id_list,
                             "input_token_list": input_token_list,
                             "input_text": input_text,
                             "full_id_list": full_id_list,
                             "full_token_list": full_token_list,
                             "full_text": full_text,
                             "logits": logits_list}

        return generation_output

    def chat(self, messages: list[ChatMessage], max_completion_tokens: int = None, logprobs: bool = False, top_logprobs: int = 10):
        response = self.model.create_chat_completion(messages, 
                                                     max_tokens=max_completion_tokens, 
                                                     logprobs=logprobs, 
                                                     top_logprobs=top_logprobs if logprobs else None)
        return response