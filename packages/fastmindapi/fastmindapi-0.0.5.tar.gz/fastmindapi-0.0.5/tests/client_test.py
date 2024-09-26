import tests_settings  # noqa: F401
import fastmindapi as FM

client = FM.Client()

models = [
    {
        "model_name": "llama3",
        "model_type": "LlamacppLLM",
        "model_path": "/Users/wumengsong/Resource/gguf/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
    },
    {
        "model_name": "gemma2",
        "model_type": "TransformersCausalLM",
        "model_path": "/Users/wumengsong/Resource/gemma-2-2b"
    }
]


client.add_model_info_list(models)
client.load_model("gemma2")

input={
  "input_text": "Do you know something about Dota2?",
  "max_new_tokens": 2,
  "return_logits": True
}
print(client.generate("gemma2",data=input))
