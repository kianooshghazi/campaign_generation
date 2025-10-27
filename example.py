from system.generators.image.image_generator import ImageGenerator
from system.generators.image_text_interactions.image_descriptor import ImageDescriptor
from system.generators.llm.prompt_variator import PromptVariator
from system.generators.llm.llm_judge import LLMJudge
from system.generators.llm.translator import Translator

# Instantiate tools
generator = ImageGenerator()
descriptor = ImageDescriptor()
variator = PromptVariator()
judge = LLMJudge()
translator = Translator()

# Step 1: Generate an image
prompt = "a futuristic cityscape at sunset"
output_path = "outputs/sample.png"
generator.generate(prompt, output_path)

# Step 2: Describe the image
description = descriptor.describe(output_path)

# Step 3: Vary the prompt
new_prompt = variator.rewrite(prompt, description)

# Step 4: Judge the relevance
is_valid = judge.evaluate(description, prompt)

# Step 5: Translate the prompt
translated = translator.translate(prompt, "French")

# Print results
print("Image Description:", description)
print("Rewritten Prompt:", new_prompt)
print("Is Valid:", is_valid)
print("Translated:", translated)
