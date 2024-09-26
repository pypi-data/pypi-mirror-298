
from ...server.router.openai import ChatMessage

class TransformersCausalLM:
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model
        self.model.eval()
        pass

    @classmethod
    def from_path(self, model_path: str):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        return TransformersCausalLM(AutoTokenizer.from_pretrained(model_path, trust_remote_code=True),
                         AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, device_map="auto"))

    def __call__(self, input_text: str, max_new_tokens: int = 256):
        import torch
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        full_text = self.tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        # output_text = full_text[len(input_text):]
        re_inputs = self.tokenizer.batch_decode(inputs.input_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        output_text = full_text[len(re_inputs):]
        return output_text
    
    def generate(self,
                 input_text: str,
                 max_new_tokens: int = 256,
                 return_logits: bool = False,
                 logits_top_k: int = 10,
                 stop_strings: list[str] = None):
        import torch
        import torch.nn.functional as F

        inputs = self.tokenizer(input_text, return_tensors='pt').to(self.model.device) # shape: (1, sequence_length)
        input_id_list = inputs.input_ids[0].tolist()
        input_token_list = [self.tokenizer.decode([token_id]) for token_id in input_id_list]

        with torch.no_grad():
            outputs = self.model.generate(**inputs, 
                                          max_new_tokens=max_new_tokens,
                                          stop_strings=stop_strings,
                                          tokenizer=self.tokenizer)
        full_id_list = outputs[0].tolist()
        full_token_list = [self.tokenizer.decode([token_id]) for token_id in full_id_list]
        full_text = self.tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        # output_text = full_text[len(input_text):] 
        re_inputs = self.tokenizer.batch_decode(inputs.input_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        output_text = full_text[len(re_inputs):]

        logits_list = None
        if return_logits:
            # 获取模型的输出 logits
            fulls = self.tokenizer(full_text, return_tensors='pt')
            with torch.no_grad():
                logits = self.model(**fulls).logits # shape: (batch_size, sequence_length, vocab_size)
                probabilities = F.softmax(logits, dim=-1)  # shape: (1, sequence_length, vocab_size)

            # 使用 torch.topk 在 vocab_size 维度上获取 top_k 的 logits 和 token IDs
            topk_logits, topk_tokens = torch.topk(logits, k=logits_top_k, dim=-1)  # shape: (batch_size, sequence_length, top_k)
            topk_probs, topk_tokens2 = torch.topk(probabilities, k=logits_top_k, dim=-1)  # shape: (batch_size, sequence_length, top_k)
            assert(torch.equal(topk_tokens,topk_tokens2))

            # 提取 batch_size 和 sequence_length
            _, sequence_length, _ = topk_tokens.shape
            assert sequence_length == len(full_id_list)

            # 遍历每个位置，打印 top_k 的 token 和 logits
            logits_list = []
            for i in range(sequence_length):
                token_id = full_id_list[i]
                token = full_token_list[i]
                # print(f"Position {i} (Token: {repr(token)}):")
                logits = {
                    "id": token_id,
                    "token": token,
                    "pred_id": [],
                    "pred_token": [],
                    "logits": [],
                    "probs": []
                }
                for j in range(logits_top_k):
                    pred_token_id = topk_tokens[0, i, j].item()
                    pred_token = self.tokenizer.decode([pred_token_id])
                    logit = topk_logits[0, i, j].item()
                    prob = topk_probs[0, i, j].item()
                    # print(f"  Top {j+1}: Token ID={pred_token_id}, Token={repr(pred_token)}, Logit={logit:.4f}, Prob={prob:.4%}")
                    logits["pred_id"].append(pred_token_id)
                    logits["pred_token"].append(pred_token)
                    logits["logits"].append(round(logit,4))
                    logits["probs"].append(round(prob,4))
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

    def chat(self, messages: list[ChatMessage], max_completion_tokens: int = None):
        import torch
        import time

        # 将消息列表转换为输入文本
        input_text = ""
        for message in messages:
            role = message.role
            content = message.content
            input_text += f"{role}: {content}\n"

        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.model.device)
        
        generate_kwargs = {
            "max_new_tokens": max_completion_tokens,
        }

        with torch.no_grad():
            outputs = self.model.generate(**inputs, **generate_kwargs)
        
        full_text = self.tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        re_inputs = self.tokenizer.batch_decode(inputs.input_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        output_text = full_text[len(re_inputs):]
        # 对output_text进行后处理
        if output_text.lower().startswith("assistant:"):
            output_text = output_text[len("assistant:"):].strip()

        choices = []
        choices.append({
            "index": 0,
            "message": {
                "role": "assistant",
                "content": output_text
            },
            "finish_reason": "stop"
        })

        response = {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": self.model.config.name_or_path,
            "choices": choices,
            "usage": {
                "prompt_tokens": inputs.input_ids.shape[1],
                "completion_tokens": sum(len(self.tokenizer.encode(text)) for text in output_texts),
                "total_tokens": inputs.input_ids.shape[1] + sum(len(self.tokenizer.encode(text)) for text in output_texts)
            }
        }
        return response