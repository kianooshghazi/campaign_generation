from system.generators.llm.base_llm import BaseLLM

class LLMJudge(BaseLLM):
    def evaluate(self, image_description, original_prompt):
        prompt = (
            f"Does the following image description match the original prompt? Answer only yes or no.\n\n"
            f"Image description: {image_description}\n"
            f"Prompt: {original_prompt}"
        )
        return self.generate_text(prompt).lower().strip() == "yes"
