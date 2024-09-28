from ...server.router.openai import ChatMessage
from ...utils.transform import convert_openai_logprobs
from ... import logger

class OpenAIChatModel:
    def __init__(self, client, model_name: str, system_prompt: str = "You are a helpful assistant."):
        self.client = client
        self.system_prompt = system_prompt
        self.model_name = model_name
        pass

    @classmethod
    def from_client(cls, client, model_name: str):
        return cls(client, model_name)

    def __call__(self, input_text: str, max_new_tokens: int = 256):
        try:
            completion = self.client.chat.completions.create(
            model= self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input_text}
            ],
            max_completion_tokens=max_new_tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
            return "【Error】: " + str(e)
    
    def generate(self,
                 input_text: str,
                 max_new_tokens: int = 256,
                 return_logits: bool = False,
                 logits_top_k: int = 10,
                 stop_strings: list[str] = None):
        while True:
            try:
                completion = self.client.chat.completions.create(
                model= self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": input_text}
                ],
                max_completion_tokens=max_new_tokens,
                logprobs=return_logits,
                top_logprobs=logits_top_k,
                stop=stop_strings
                )
                break
            except Exception as e:
                logger.info(f"【Error】: {e}")
        output_text = completion.choices[0].message.content
        logits_list = convert_openai_logprobs(completion.choices[0].logprobs)
        generation_output = {"output_text": output_text,
                            #  "input_id_list": input_id_list,
                            #  "input_token_list": input_token_list,
                             "input_text": input_text,
                            #  "full_id_list": full_id_list,
                            #  "full_token_list": full_token_list,
                            #  "full_text": full_text,
                             "logits": logits_list}
        return generation_output

    def chat(self, messages: list[ChatMessage], max_completion_tokens: int = None, logprobs: bool = False, top_logprobs: int =10):
        try:
            completion = self.client.chat.completions.create(
            model= self.model_name,
            messages=messages,
            max_completion_tokens=max_completion_tokens,
            logprobs=logprobs,
            top_logprobs=top_logprobs if logprobs else None,
            )
            logger.info(completion.model_dump())
            return completion.choices[0].message.content
        except Exception as e:
            return "【Error】: " + str(e)