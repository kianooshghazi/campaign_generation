let campaignCount = 0;

document.getElementById("add-campaign").addEventListener("click", addCampaignBlock);
document.getElementById("campaign-form").addEventListener("submit", handleSubmit);

// Add initial block
addCampaignBlock();

function addCampaignBlock() {
  const container = document.getElementById("campaigns-container");
  const block = document.createElement("div");
  block.className = "campaign-block";
  block.dataset.index = campaignCount;

  block.innerHTML = `
    <label>Product</label>
    <input type="text" name="product-${campaignCount}" required />

    <label>Campaign Message</label>
    <textarea name="message-${campaignCount}" required></textarea>

    <label>Target Region</label>
    <input type="text" name="region-${campaignCount}" required />

    <label>Target Audience</label>
    <input type="text" name="audience-${campaignCount}" required />

    <label>Language</label>
    <input type="text" name="language-${campaignCount}" required />
  `;

  container.appendChild(block);
  campaignCount++;
}

function handleSubmit(e) {
  e.preventDefault();
  const resultsContainer = document.getElementById("results-container");
  resultsContainer.innerHTML = `<p>Processing...</p>`;

  const blocks = document.querySelectorAll(".campaign-block");
  const requests = [];

  blocks.forEach(block => {
    const idx = block.dataset.index;
    const payload = {
      product: block.querySelector(`[name="product-${idx}"]`).value,
      campaign_message: block.querySelector(`[name="message-${idx}"]`).value,
      target_region: block.querySelector(`[name="region-${idx}"]`).value,
      target_audience: block.querySelector(`[name="audience-${idx}"]`).value,
      language: block.querySelector(`[name="language-${idx}"]`).value,
    };

    requests.push(
      fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).then(res => res.json())
    );
  });

  Promise.all(requests).then(responses => {
    resultsContainer.innerHTML = "";

    responses.forEach((response, i) => {
      const resultDiv = document.createElement("div");
      resultDiv.className = "result-block";

      resultDiv.innerHTML = `<h3>Campaign ${i + 1}</h3>`;

      Object.entries(response).forEach(([ratio, data]) => {
        resultDiv.innerHTML += `
          <p><strong>${ratio}</strong></p>
          <p>Prompt: ${data.prompt}</p>
          <p>Enriched: ${data.enriched_prompt}</p>
          <p>Description: ${data.description}</p>
          <p>Translated Text: ${data.translated_text}</p>
          <p>Accepted: ${data.accepted}</p>
          <img src="${data.path}" />
        `;
      });

      resultsContainer.appendChild(resultDiv);
    });
  });
}
