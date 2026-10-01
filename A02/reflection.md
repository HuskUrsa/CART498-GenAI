# P+666 — Reflection

Sam Hoyek · CART 498 · Assignment 2

It’s interesting that things continued to make sense even when selecting tokens hundreds of places down the probability ranking. I’m interested in numerology, specifically Nick Land’s discussion of a burgeoning science of “666ology,” so I chose P+666 because I was curious to see what would come up.

Funnily enough, a lot of words and themes that felt Landian to me came up. The text felt coded: it brought up Britain, dystopian themes and imagery, and associations with secret languages. Replacements such as “wounds” and “war” changed the atmosphere of Wallace Stevens’s poem *The Snow Man*. It remained poetic, but felt more CCRU-coded, which is why it interested me.

The text starts to break down around “Blake” and “N.” These replacements make the grammar harder to follow, but that breakdown becomes part of the experience of reading it. Compared with P+7, P+666 selects much less probable alternatives, yet parts of the text still suggest meaning. The connection to CCRU feels like a mixture of what the model produced and what I brought to the reading, because those things are interlinked. I feel it is worth exploring numerological implications with generative AI and playing with those for fun.

To adapt P+7 to replace every noun, I would first identify the nouns in the original text. For each noun, I would use the original text preceding it as the model’s context, filter predictions to alternatives that function as nouns, and choose the seventh-highest-probability noun alternative. This differs from selecting the seventh token without filtering. Since tokens can be word fragments, the method would also need to handle complete noun candidates. I would keep the original context throughout, rather than feed replacements into later predictions, because I’m curious about what happens if we remain circling around our source.

## Reference

theory underground. 2025. “"The burgeoning science of 666olgy" | Ft. Nick Land.” YouTube video, 38:23. November 18. https://www.youtube.com/watch?v=YMaQLeUcvAo.

## AI assistance disclosure

Sam Hoyek supplied the observations, interpretation, choice of 666, and preferred noun-replacement approach. OpenAI Codex assembled the approved reflection from his answers and added the technical implementation explanation. The interpretation of the generated poem is personal; it is not evidence of a numerological mechanism. Code preparation and environment details are documented in README.md.
