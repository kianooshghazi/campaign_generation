from system.generators.llm.base_llm import BaseLLM

class PromptVariator(BaseLLM):
    def rewrite(self, base_prompt, image_description):
        prompt = (
            f"Describe a campaign image to an image generator model to advertise a product. "
            "Your output will be directly used as a generative image prompt, be specific and describe the details of the image we want."
            "this is advertising content so your descriptions should highlight the product."
            f"Make it appropriate for the audience that I will give you the profile of. Here is the information: {image_description}"
            f"your prompt needs to absolutely be centered around the product mentioned above"
            f"Return only the rewritten sentence and nothing else.\n\n"
            f"If appropriate, somehow represent the campaign message in the image as well. Here is the message: {base_prompt}"
        )
        return self.generate_text(prompt)
