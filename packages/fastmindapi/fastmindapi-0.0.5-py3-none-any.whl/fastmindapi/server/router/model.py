from pydantic import BaseModel, ConfigDict
from fastapi import APIRouter, Request

PREFIX = "/model"

class BasicModel(BaseModel):
    model_name: str
    model_type: str
    model_path: str
    model_foundation: str = None # for Peft Model
    model_config = ConfigDict(protected_namespaces=())

class GenerationRequest(BaseModel):
    input_text: str
    max_new_tokens: int = None
    return_logits: bool = False
    logits_top_k: int = 10
    stop_strings: list[str] = None

    model_config=ConfigDict(protected_namespaces=())

class GenerationOutput(BaseModel):
    output_text: str
    logits: list

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    max_new_tokens: int = 256

    model_config=ConfigDict(protected_namespaces=())

def add_model_info(request: Request, item: BasicModel):
    server = request.app.state.server
    if item.model_name in server.module["model"].available_models:
        server.logger.info(item.model_name+" is already listed in [available_models].")
        if server.module["model"].available_models[item.model_name]["model_type"] != item.model_type:
            server.logger.info("Updating model type: "+server.module["model"].available_models[item.model_name]["model_type"]+" -> "+item.model_type+".")
            server.module["model"].available_models[item.model_name]["model_type"] = item.model_type
        if server.module["model"].available_models[item.model_name]["model_path"] != item.model_path:
            server.logger.info("Updating model path: "+server.module["model"].available_models[item.model_name]["model_path"]+" -> "+item.model_path+".")
            server.module["model"].available_models[item.model_name]["model_path"] = item.model_path
    else:
        server.module["model"].available_models[item.model_name] = {
            "model_type": item.model_type,
            "model_path": item.model_path
            }
    if item.model_foundation is not None:
        server.module["model"].available_models[item.model_name]["model_foundation"] = item.model_foundation
    return True

def load_model(request: Request, model_name: str):
    server = request.app.state.server
    try:
        server.module["model"].load_model_from_path(model_name)
        return True
    except Exception as e:
        return "【Error】: "+str(e)

def unload_model(request: Request, model_name: str):
    server = request.app.state.server
    if model_name in server.module["model"].loaded_models:
        del server.module["model"].loaded_models[model_name]
        return f"{model_name} is released successfully."
    else:
        return f"{model_name} is not loaded right now."

def simple_generate(request: Request, model_name: str, item: GenerationRequest):
    server = request.app.state.server
    output_text = server.module["model"].loaded_models[model_name](input_text = item.input_text, 
                                                                        max_new_tokens=item.max_new_tokens if item.max_new_tokens is not None else None)
    return output_text

def generate(request: Request, model_name: str, item: GenerationRequest):
    server = request.app.state.server
    try:
        assert model_name in server.module["model"].loaded_models
    except AssertionError:
        return f"【Error】: {model_name} is not loaded."
    outputs = server.module["model"].loaded_models[model_name].generate(**item.model_dump())
    return outputs

def chat(request: Request, model_name: str, item: ChatRequest):
    server = request.app.state.server
    try:
        assert model_name in server.module["model"].loaded_models
    except AssertionError:
        return f"【Error】: {model_name} is not loaded."
    outputs = server.module["model"].loaded_models[model_name].chat(messages=item.messages, max_new_tokens=item.max_new_tokens)
    return outputs

def get_model_router():
    router = APIRouter(prefix=PREFIX)

    router.add_api_route("/add_info", add_model_info, methods=["POST"])
    router.add_api_route("/load/{model_name}", load_model, methods=["GET"])
    router.add_api_route("/unload/{model_name}", unload_model, methods=["GET"])
    router.add_api_route("/call/{model_name}", simple_generate, methods=["POST"])
    router.add_api_route("/generate/{model_name}", generate, methods=["POST"])
    router.add_api_route("/chat/{model_name}", chat, methods=["POST"])
    return router
