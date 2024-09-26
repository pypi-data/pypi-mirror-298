from .transformers.CausalLM import TransformersCausalLM
from .transformers.PeftModel import PeftCausalLM
from .llama_cpp.LLM import LlamacppLLM

class ModelModule:
    def __init__(self):
        self.available_models = {}
        self.loaded_models = {}

    # TODO rewrite load_model, also in server.core.main
    # def load_model(self, model_name: str, model):
    #     self.loaded_models[model_name] = model

    def load_model_from_path(self, model_name: str):
        '''
        Load the specific model.
        '''
        model_type = self.available_models[model_name]["model_type"]
        model_path = self.available_models[model_name]["model_path"]
        
        # 匹配模型类型
        match model_type:
            case "TransformersCausalLM":
                self.loaded_models[model_name] = TransformersCausalLM.from_path(model_path)
            case "PeftCausalLM":
                model_foundation = self.available_models[model_name]["model_foundation"]
                if model_foundation not in self.loaded_models:
                    self.loaded_models[model_foundation] = TransformersCausalLM.from_path(self.available_models[model_foundation]["model_path"])
                base_model = self.loaded_models[model_foundation]
                assert isinstance(base_model, TransformersCausalLM)
                self.loaded_models[model_name] = PeftCausalLM.from_path(base_model, model_path)
            case "LlamacppLLM":
                self.loaded_models[model_name] = LlamacppLLM.from_path(model_path)

