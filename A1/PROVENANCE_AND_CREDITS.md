# Provenance and credits

## Main Z-Image series and supporting tests

- **Images:** Original local generations for Sam Hoyek's in-progress experimental music and visual project, *demonstration_02: soma on_affect*. The top-level JPGs are exports of raw PNG outputs, not Photoshop edits. `z_image_studies/` preserves four scenarios with one exact prompt and three seeds each. Each `generation_record.json` links a JPG to its seed and source-PNG SHA-256 hash.
- **Model:** [`filipstrand/Z-Image-Turbo-mflux-4bit`](https://huggingface.co/filipstrand/Z-Image-Turbo-mflux-4bit), a 4-bit MFLUX-compatible quantization by Filip Strand of [Tongyi Lab's Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo). The quantized model card labels its licence `tongyi-qianwen-license` and directs readers to the base model for licensing detail.
- **Runtime:** [MFLUX](https://github.com/mflux-community/mflux), using Apple's MLX on a local machine. MFLUX's [software licence](https://github.com/mflux-community/mflux/blob/main/LICENSE) is MIT. The four batches used 768 x 768 output and 9 steps. The recorded seeds are in each scenario's generation record.
- **Code:** `generation/generate_mflux_storyboard.py` is an unchanged copy of the local Python script used to invoke the MFLUX generator and write manifests. It is included as actual workflow code; it is **not** a Diffusers script. The local workflow and assignment package were prepared with Codex assistance.

## Bonus ChatGPT trial

The three images under `bonus_chatgpt_mediated_rooms/` were generated with OpenAI's ChatGPT image tool during D2 visual exploration. The exact model version, original prompts, and seeds were not recorded; the paired TXT files are retrospective prompt summaries. They are labeled as bonus evidence rather than reproducible main outputs.

## Written reflection

Sam Hoyek supplied the reflective ideas and personal judgments in `A1_short_essay_Sam_Hoyek.pdf`. Codex assisted with light formatting, a factual process sentence, source identification for Arca's *Riquiquí;Bronze-Instances(1-100)*, and PDF production. The named work is credited in the PDF with [Arca's release page](https://arca1000000.com/release/536724-arca-riquiqubronze-instances1-100) and [Bronze's project description](https://bronze.ai/listen/arca/).
