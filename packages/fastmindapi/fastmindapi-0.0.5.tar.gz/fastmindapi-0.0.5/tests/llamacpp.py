from llama_cpp import Llama

llm = Llama(
      model_path="/Users/wumengsong/Resource/gguf/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf",
      n_gpu_layers=-1)
# gemma-2-2b-q8_0.gguf
# Meta-Llama-3.1-8B-Instruct-Q8_0.gguf
# qwen2-7b-instruct-q8_0.gguf

# output = llm(
#       "Q: Do you know Sparse AutoEncoder?", # Prompt
#       max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
#       stop=["Q:"], # Stop generating just before the model would generate a new question
#       echo=True # Echo the prompt back in the output
# ) # Generate a completion, can also call create_completion
# print(output)


tokens = llm.tokenize(b"Do you know something about Dota2?")
# for token in llm.generate(tokens, top_k=40, top_p=0.95, temp=1.0, repeat_penalty=1.0):
#       print(llm.detokenize([token]))

generator = llm.generate(tokens, top_k=40, top_p=0.95, temp=1.0, repeat_penalty=1.0)
print(llm.detokenize([next(generator)]))
print(llm.detokenize([next(generator)]))