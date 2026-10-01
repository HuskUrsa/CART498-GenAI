# A02 — P+7 and P+666

Sam Hoyek · CART 498 B · Fall 2026

## Deliverables

- `P+7.txt`: required seventh-highest-probability next-token transformation.
- `P+666.txt`: selected creative variation at rank 666.
- `A02_P7_P666_Sam_Hoyek.ipynb`: commented notebook generating and checking both outputs.
- `reflection.md`: approved 294-word reflection; citation and AI disclosure follow the body.

## Reproduce

Open the notebook in Google Colab with a CPU runtime and run all code cells in order. The setup pins Transformers 5.17.0, the version used during generation. PyTorch is provided by Colab; the original run used 2.11.0+cpu. The notebook prints actual versions and verifies exact output equality. It downloads the GPT-2 model and tokenizer from Hugging Face, requiring an internet connection but no paid API or secret key. It writes the two poems and a token audit in the current directory. Download the outputs before ending a Colab runtime.

Each line uses only its original prefix before the removed final word. We rank the full next-token vocabulary and select indices 6 and 665 (one-based ranks 7 and 666). Original punctuation and stanza breaks are retained; tokens are not filtered, repaired, or completed into words. Incomplete forms such as “isn,” “med,” and “N” are intentional consequences of the one-token rule. Rank 666 means the 666th most probable next token, not the 666th generated poem.

## Sources and credits

- Stevens, Wallace. 1921. “The Snow Man.” Source text supplied in Gabriel Vigliensoni's CART 498 Assignment 2 brief. https://moodle.concordia.ca/moodle/mod/assign/view.php?id=4616704. The copied instructor background text and images are omitted from this submission notebook.
- Radford, Alec, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. 2019. “Language Models Are Unsupervised Multitask Learners.” OpenAI. GPT-2 model and tokenizer (MIT licence): https://huggingface.co/openai-community/gpt2. Model trained on OpenAI's WebText corpus; no training dataset was downloaded or used separately in this assignment.
- Hugging Face. “Transformers.” Version 5.17.0; Apache 2.0 licence. https://github.com/huggingface/transformers.
- PyTorch contributors. “PyTorch.” Original generation version 2.11.0+cpu; BSD-style licence. https://github.com/pytorch/pytorch.
- theory underground. 2025. “"The burgeoning science of 666olgy" | Ft. Nick Land.” YouTube video, 38:23. November 18. https://www.youtube.com/watch?v=YMaQLeUcvAo. The spelling “666olgy” reproduces the displayed video title.

## AI assistance

OpenAI Codex prepared and explained the Python code, ran it in Google Colab, assembled the reflection from Sam's own answers with a technical implementation paragraph, and helped package and check the files. GPT-2 produced the ranked replacement tokens. Sam selected rank 666, supplied the observations and interpretation, and approved the final reflection and submission. The exact Codex model identifier was not exposed in this session; it is not guessed here. Library versions are recorded above and printed by the notebook. The proposed all-noun method is explanatory only.
