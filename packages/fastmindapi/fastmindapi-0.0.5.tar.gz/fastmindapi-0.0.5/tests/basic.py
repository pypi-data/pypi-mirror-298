import tests_settings  # noqa: F401
import fastmindapi as FM

server = FM.Server()

# client.module["model"].available_models["llama3"]={
#     "model_type": "LlamacppLLM",
#     "model_path": "/Users/wumengsong/Resource/gguf/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
# }
# client.module["model"].load_model_from_path("llama3")

# server.module["model"].available_models["gemma2"]={
#     "model_type": "TransformersCausalLM",
#     "model_path": "/Users/wumengsong/Resource/gemma-2-2b"
# }
# server.module["model"].load_model_from_path("gemma2")

server.run()