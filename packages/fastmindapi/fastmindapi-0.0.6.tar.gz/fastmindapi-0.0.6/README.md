# FastMindAPI

![PyPI - Version](https://img.shields.io/pypi/v/fastmindapi?style=flat-square&color=red) ![GitHub License](https://img.shields.io/github/license/fairyshine/FastMindAPI?style=flat-square&color=yellow) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/fairyshine/FastMindAPI?style=flat-square&color=green) ![PyPI - Downloads](https://img.shields.io/pypi/dm/fastmindapi?style=flat-square&color=blue)

An easy-to-use, high-performance(?) backend for serving LLMs and other AI models, built on FastAPI.

## 🚀 Quick Start

### Install

```shell
pip install fastmindapi
```

### Use

#### Run the server 

```shell
# in Shell
fastmindapi-server --port 8000
```

```Python
# in Python
import fastmindapi as FM

server = FM.Server()
server.run()
```

#### Access via client / HTTP requests

```shell
curl http://IP:PORT/docs#/
```

```python
import fastmindapi as FM

client = FM.Client(IP="x.x.x.x", PORT=xxx) # 127.0.0.1:8000 for default

client.add_model_info_list(model_info_list)
client.load_model(model_name)
client.generate(model_name, generation_request)
```

> 🪧 **We primarily maintain the backend server; the client is provided for reference only.** The main usage is through sending HTTP requests. (We might release FM-GUI in the future.)

## ✨ Features

### Model: Support models with various backends

- ✅  [Transformers](https://github.com/huggingface/transformers)
  - `TransformersCausalLM` ( `AutoModelForCausalLM`)
  - `PeftCausalLM` ( `PeftModelForCausalLM` )
  
- ✅  [llama.cpp](https://github.com/abetlen/llama-cpp-python)
  - `LlamacppLM` (`Llama`)

- [MLC LLM](https://llm.mlc.ai)
- [vllm](https://github.com/vllm-project/vllm)
- ...

### Modules: More than just chatting with models

- Function Calling (extra tools in Python)
- Retrieval
- Agent
- ...

### Flexibility: Easy to Use & Highly Customizable

- Load the model when coding / runtime
- Add any APIs you want

