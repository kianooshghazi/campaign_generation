from system.generators.llm.base_llm import BaseLLM

class Translator(BaseLLM):
    def translate(self, text, target_language):
        prompt = (
            f"Translate the following text to {target_language}. Only return the translated sentence.\n\n"
            f"{text}"
        )
        return self.generate_text(prompt)
