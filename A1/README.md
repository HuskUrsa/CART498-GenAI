# CART 498 — Assignment 1: surreal image variations

This submission presents three variations from my existing local Z-Image tests, as discussed with Gabriel. The **main series** is the three numbered carwash JPGs and their matching TXT files in this folder. The additional studies and ChatGPT images are supporting process and bonus material.

| Main image | Prompt file | Seed |
| --- | --- | ---: |
| `01_carwash_seed_87353459.jpg` | `01_carwash_seed_87353459.txt` | 87353459 |
| `02_carwash_seed_364487729.jpg` | `02_carwash_seed_364487729.txt` | 364487729 |
| `03_carwash_seed_782654091.jpg` | `03_carwash_seed_782654091.txt` | 782654091 |

The three TXT files contain the same **exact prompt used for generation**. I varied the seed to test how one scene changed across outputs; I have not presented these as three separately written prompts. Each JPG is an export of its corresponding raw generated PNG, before Photoshop editing.

## Method and process

I generated the images locally with the `filipstrand/Z-Image-Turbo-mflux-4bit` model through MFLUX/MLX at 768 × 768 pixels and 9 steps. [`generation/generate_mflux_storyboard.py`](generation/generate_mflux_storyboard.py) is a copy of the Python script used for the original workflow. It invokes MFLUX rather than Diffusers, and its original local environment is described in [`generation/README.md`](generation/README.md). The script is included as process evidence rather than a claim that it runs independently from this folder.

[`z_image_studies/`](https://github.com/HuskUrsa/CART498-GenAI/tree/main/A1/z_image_studies) contains four scenarios, each with its saved prompt, three JPG exports, three seeds, and a generation record linking the exports to the source PNGs. The [contact sheet](z_image_studies/contact_sheet.png) offers an overview. The carwash scenario duplicates the main series for a complete process record.

## Essay and bonus

[`A1_short_essay_Sam_Hoyek.pdf`](A1_short_essay_Sam_Hoyek.pdf) is my 255-word reflection on the process, generative AI in creative work, and Arca's *Riquiquí;Bronze-Instances(1-100)*. The separately labeled [`bonus_chatgpt_mediated_rooms/`](https://github.com/HuskUrsa/CART498-GenAI/tree/main/A1/bonus_chatgpt_mediated_rooms) shows three related visual trials. Its TXT files are retrospective summaries; the exact ChatGPT prompts and seeds were not recovered, so those images are not part of the three required prompt/image pairs.

[`PROVENANCE_AND_CREDITS.md`](PROVENANCE_AND_CREDITS.md) identifies the model, tools, source records, and assistance in preparing this package.
