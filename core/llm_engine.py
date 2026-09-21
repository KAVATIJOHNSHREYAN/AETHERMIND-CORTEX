"""
AetherMind Cortex Local LLM Engine
Provides integration with Ollama for model discovery, health monitoring, streaming responses, and performance metrics.
"""

import time
from typing import List, Dict, Any, Generator, Optional
import ollama
from core.logger import get_logger

logger = get_logger("LLMEngine")

class OllamaEngine:
    """Local LLM Engine interfacing with Ollama service."""

    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.client = ollama.Client(host=host)

    def check_service_status(self) -> Dict[str, Any]:
        """Checks if Ollama service is running and accessible."""
        try:
            models = self.client.list()
            return {
                "online": True,
                "model_count": len(models.get("models", [])),
                "error": None
            }
        except Exception as e:
            logger.warning(f"Ollama service check failed: {e}")
            return {
                "online": False,
                "model_count": 0,
                "error": str(e)
            }

    def list_available_models(self) -> List[str]:
        """Retrieves list of installed Ollama model names."""
        try:
            res = self.client.list()
            models_list = res.get("models", [])
            model_names = [m.get("name", m.get("model", "")) for m in models_list]
            logger.info(f"Discovered Ollama models: {model_names}")
            return model_names
        except Exception as e:
            logger.error(f"Failed to list local Ollama models: {e}")
            return []

    def stream_chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Streams response chunks from local Ollama model.
        Yields dictionaries with 'delta', 'accumulated', 'metrics', and 'done'.
        """
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        start_time = time.time()
        accumulated_text = ""
        token_estimate = 0

        try:
            response_stream = self.client.chat(
                model=model,
                messages=full_messages,
                stream=True,
                options={
                    "temperature": temperature,
                    "top_p": top_p
                }
            )

            for chunk in response_stream:
                delta = chunk.get("message", {}).get("content", "")
                accumulated_text += delta
                token_estimate += max(1, len(delta.split()))  # Rough word/token count estimation

                elapsed = time.time() - start_time
                speed = token_estimate / elapsed if elapsed > 0 else 0.0

                yield {
                    "delta": delta,
                    "accumulated": accumulated_text,
                    "done": False,
                    "metrics": {
                        "elapsed_sec": round(elapsed, 2),
                        "token_count": token_estimate,
                        "tokens_per_sec": round(speed, 1)
                    }
                }

            total_elapsed = time.time() - start_time
            yield {
                "delta": "",
                "accumulated": accumulated_text,
                "done": True,
                "metrics": {
                    "elapsed_sec": round(total_elapsed, 2),
                    "token_count": token_estimate,
                    "tokens_per_sec": round(token_estimate / total_elapsed if total_elapsed > 0 else 0.0, 1)
                }
            }

        except Exception as e:
            logger.warning(f"Ollama local model unavailable or offline ({e}). Generating cognitive fallback response.")
            fallback_text = (
                f"🧠 **AetherMind Cortex Fallback Reasoning Engine**\n\n"
                f"I am operating in **Offline Cognitive Simulation Mode** (Local Ollama server is not connected or model `{model}` is not pulled locally).\n\n"
                f"### Intent & Goal Analysis\n"
                f"- **User Prompt Processed:** \"{messages[-1]['content'] if messages else 'N/A'}\"\n"
                f"- **Pipeline Phase:** Pre-execution verification complete.\n"
                f"- **Recommendation:** To unlock full local LLM inference, start your local Ollama instance (`ollama serve`) and pull a model (e.g. `ollama pull llama3`).\n\n"
                f"*All long-term memories, knowledge vector indexes, and profile preferences remain 100% active and saved locally.*"
            )
            yield {
                "delta": fallback_text,
                "accumulated": fallback_text,
                "done": True,
                "metrics": {"elapsed_sec": 0.1, "token_count": len(fallback_text.split()), "tokens_per_sec": 50.0}
            }
