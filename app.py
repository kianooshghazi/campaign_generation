from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

from system.generators.image.image_generator import ImageGenerator
from system.generators.image_text_interactions.image_descriptor import ImageDescriptor
from system.generators.llm.prompt_variator import PromptVariator
from system.generators.llm.llm_judge import LLMJudge
from system.generators.llm.translator import Translator
from system.common.logger.logger import setup_logger
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
from uuid import uuid4 

from system.common.image_modifiers.image_annotator import ImageAnnotator


logger = setup_logger()

app = Flask(__name__)
CORS(app)

ASPECT_RATIOS = {
    "1:1": (512, 512),
    "9:16": (768, 512),
    "16:9": (512, 768),
}

# Initialize tools
annotator = ImageAnnotator()
image_generator = ImageGenerator()
descriptor = ImageDescriptor()
prompt_variator = PromptVariator()
judge = LLMJudge()
translator = Translator()

@app.route("/generate", methods=["POST"])
def generate():
    request_id = uuid4()
    data = request.get_json()
    logger.info(f"{request_id} | request body:  {data}")
    product = data["product"]
    base_prompt = data["campaign_message"]
    target_region = data["target_region"]
    target_audience = data["target_audience"]
    language = data["language"]

    logger.info(f"{request_id} | Received generation request: {data}")

    output_dir = Path(".assets") / product
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {}

    for ratio_name, (w, h) in ASPECT_RATIOS.items():
        image_path = output_dir / f"{ratio_name}.png"
        is_acceptable = False
        retry_count = 0

        while not is_acceptable and retry_count < 3:
            
            enriched_prompt = prompt_variator.rewrite(
                base_prompt=base_prompt,
                image_description=f"Product: {product}. Target audience: {target_audience}. Target region: {target_region}."
            )
            logger.info(f"{request_id} | enriched_prompt: {enriched_prompt}")
            asset_exists = image_path.exists()
            if asset_exists:
                logger.info(f"{request_id} | Using existing image for {ratio_name}")
                image = Image.open(image_path)
            else:
                image = image_generator.generate(
                    enriched_prompt,
                    width=w,
                    height=h
                )
                logger.info(f"{request_id} | Saving image {image_path}")
                image.save(image_path)

            description = descriptor.describe(image)
            logger.info(f"{request_id} | image description: {description}")

            translated_text = translator.translate(base_prompt, language)
            logger.info(f"{request_id} | translated_text: {translated_text}")
            # Bypassing if the asset exists. Ideally I would rewrite the asset if it no longer 
            # represents the campaign message (maybe campaign message updated). 
            # Leaving this bypass because of explicit requirements but in a real scenario I would try to 
            # learn why we would always reuse an existing asset. 
            is_acceptable = judge.evaluate(description, base_prompt) if not asset_exists else True
            logger.info(f"{request_id} | is_acceptable: {is_acceptable}")
            if not is_acceptable:
                continue
            annotated_image = annotator.annotate(image, translated_text)
            annotated_image.save(image_path)

            result[ratio_name] = {
                "prompt": base_prompt,
                "enriched_prompt": enriched_prompt,
                "description": description,
                "translated_text": translated_text,
                "accepted": is_acceptable,
                "path": str(image_path)
            }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
