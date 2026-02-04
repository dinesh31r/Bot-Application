import os
import glob
from llama_cpp import Llama

class LLMEngine:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        # Find any .gguf file in the models directory
        model_files = glob.glob("models/*.gguf")
        
        if not model_files:
            print("WARNING: No GGUF model found in 'models/' directory. LLM will not work.")
            return

        model_path = model_files[0]
        print(f"Loading Local LLM from: {model_path}")
        
        try:
            # Initialize Llama model
            # n_gpu_layers=-1 tries to offload all to GPU if available and installed with cuBLAS
            self.model = Llama(
                model_path=model_path,
                n_ctx=2048,  # Context window
                n_gpu_layers=-1, 
                verbose=False
            )
            print("Local LLM Loaded Successfully.")
        except Exception as e:
            print(f"Failed to load LLM: {e}")

    def generate_response(self, query: str, context: str = "") -> str:
        if not self.model:
            return "Thinking module offline. Please check model configuration."

        # Construct Prompt
        system_prompt = """You are JARVIS, a highly advanced AI assistant. 
Your personality is helpful, polite, and precise. 
If context is provided, use it to answer the question. 
If you don't know the answer, say so elegantly."""

        if context:
            prompt = f"{system_prompt}\n\nContext Information:\n{context}\n\nUser: {query}\nJARVIS:"
        else:
            prompt = f"{system_prompt}\n\nUser: {query}\nJARVIS:"

        try:
            output = self.model(
                prompt,
                max_tokens=256,
                stop=["User:", "\n"],
                echo=False,
                temperature=0.7
            )
            return output['choices'][0]['text'].strip()
        except Exception as e:
            return f"Error computing response: {e}"

llm_engine = LLMEngine()
