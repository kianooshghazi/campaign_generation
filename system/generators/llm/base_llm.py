import requests

class BaseLLM:
    def __init__(self, base_url="http://localhost:11434", model="llama3"):
        self.api_url = f"{base_url}/api/generate"
        self.model = model

    def generate_text(self, prompt):
        response = requests.post(
            self.api_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"].strip()
