# 🖼️ Campaign Image Generator

This project is a full-stack campaign generation tool that:
- Accepts structured campaign data (product, region, audience, message)
- Generates enriched prompts
- Creates campaign images with Stable Diffusion
- Displays results with metadata in a simple web UI

---

## 🚀 Getting Started

### 🔧 Requirements
- LLaMA Installed
- Docker installed
- macOS (for `open index.html` to work — or change that line for your OS)

---

## ▶️ Run the App

Just run:

```bash
./run.sh

A browser will automatically open to allow you to play with the POC. once the app is installed. 
Please look into the .assets folder to find the generated assets. 
Watch the video for a walkthrough.


## ⚖️ Trade-offs & Design Rationale

This project was intentionally designed to **run entirely locally**, without requiring authentication tokens, hosted APIs, or cloud infrastructure. The goal was to create a prototype that is accessible to **non-technical users** such as product managers, marketing leads, and decision-makers, while still being clear and maintainable for technical collaborators.

### 🧠 Design Philosophy

* **Low overhead, high reproducibility:** Everything runs with a single command — `./run.sh`. This builds the Docker image, launches the backend, and opens the UI automatically.
* **Zero onboarding friction:** No account setup, tokens, or environment configuration are required. Users can simply clone the repo and run it.
* **Tailored for non-technical audiences:** The interface and workflow are designed so a non-developer can trigger the entire flow from their terminal or file explorer.

### 🔁 System Intent & Feedback Loop

The architecture was designed to replicate a **creative feedback loop**:

1. The user inputs key campaign details — product, target region, target audience, campaign message, and language.
2. The system enriches the input, generates multiple image variants, and describes them.
3. A lightweight **LLM “Judge”** evaluates whether the generated image aligns with the intent of the campaign.

This “LLM-as-a-critic” loop ensures that the system doesn’t blindly accept generated results, but instead applies an internal check for relevance and quality.

### 🧩 Future Extensions

In future iterations, the system can integrate **image embedding-based validation**:

* Extract embeddings from both the **generated image** and a **reference logo or visual**.
* Compute similarity scores to detect whether expected branding or labels appear.
* Optionally fine-tune the embedding model to better distinguish **logos** from backgrounds — enabling more precise validation for real-world use cases.

### 🧠 Technical Considerations

While my experience is strongest in **language modeling** and **computer vision**, this project extends into **multimodal generative AI**.
I focused on clarity, reproducibility, and functionality over novelty — prioritizing code that can be easily extended and understood rather than deeply optimized for performance or bleeding-edge research.

### 💻 Hardware & Model Constraints

This prototype was developed on a **MacBook Air**, which has limited compute power and no dedicated GPU.
Accordingly:

* The smallest available models were chosen — **LLaMA (lightweight variant)** for text tasks and **Stable Diffusion v1-4** for image generation.
* All processing runs on **CPU** for maximum portability.
* The structure allows future scaling: swapping in more powerful models or GPUs without code redesign.

### 🎯 Alignment with the Problem Statement

This solution directly addresses the target problem:

* Accepts structured campaign specifications,
* Generates both images and descriptive text,
* Validates and refines results through a built-in feedback mechanism, and
* Displays final outputs in a clear, self-contained UI.

The outcome is a **minimal-overhead, locally executable proof-of-concept** that demonstrates the complete logical loop — from structured input to creative output, judgment, and visualization — without reliance on external services or complex setup.
