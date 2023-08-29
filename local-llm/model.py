from gpt4all import GPT4All

model = GPT4All("orca-mini-3b.ggmlv3.q4_0.bin")
# https://huggingface.co/TheBloke/orca_mini_3B-GGML


def orca_mini_3b(
    prompt,
    max_tokens,
    temp,
    top_k,
    top_p,
    repeat_penalty,
    repeat_last_n,
    n_batch,
    n_predict,
    streaming,
):
    """
    Args:
        prompt: The prompt for the model to complete.
        max_tokens: The maximum number of tokens to generate.
        temp: The model temperature. Larger values increase creativity but decrease factuality.
        top_k: Randomly sample from the top_k most likely tokens at each generation step. Set this to 1 for greedy decoding.
        top_p: Randomly sample at each generation step from the top most likely tokens whose probabilities add up to top_p.
        repeat_penalty: Penalize the model for repetition. Higher values result in less repetition.
        repeat_last_n: How far in the models generation history to apply the repeat penalty.
        n_batch: Number of prompt tokens processed in parallel. Larger values decrease latency but increase resource requirements.
        n_predict: Equivalent to max_tokens, exists for backwards compatibility.
        streaming: If True, this method will instead return a generator that yields tokens as the model generates them.

    Returns:
        Generator that yields the completion token by token.
    """

    output = model.generate(
        f"{prompt} I will now summarize this in one sentence:",
        max_tokens,
        temp,
        top_k,
        top_p,
        repeat_penalty,
        repeat_last_n,
        n_batch,
        n_predict,
        streaming,
    )
    return output


blog_text = (
    'The rapid advance of artificial intelligence has generated a lot of buzz, with some predicting it will lead to an idyllic utopia and others warning it will bring the end of humanity. But speculation about where AI technology is going, while important, can also drown out important conversations about how we should be handling the AI technologies available today.\nOne such technology is generative AI, which can create content including text, images, audio, and video. Popular generative AIs like the chatbot ChatGPT generate conversational text based on training data taken from the internet.\nToday a group of 14 researchers from a number of organizations including MIT published a commentary article in Science that helps set the stage for discussions about generative AI\u2019s immediate impact on creative work and society more broadly. The paper\u2019s MIT-affiliated co-authors include Media Lab postdoc Ziv Epstein SM \u201919, PhD \u201923; Matt Groh SM \u201919, PhD \u201923; PhD students Rob Mahari \u201917 and Hope Schroeder; and Professor Alex "Sandy" Pentland.\nMIT News spoke with Epstein, the lead author of the paper.\nQ: Why did you write this paper?\nA: Generative AI tools are doing things that even a few years ago we never thought would be possible. This raises a lot of fundamental questions about the creative process and the human\u2019s role in creative production. Are we going to get automated out of jobs? How are we going to preserve the human aspect of creativity with all of these new technologies?\nThe complexity of black-box AI systems can make it hard for researchers and the broader public to understand what\u2019s happening under the hood, and what the impacts of these tools on society will be. Many discussions about AI anthropomorphize the technology, implicitly suggesting these systems exhibit human-like intent, agency, or self-awareness. Even the term \u201cartificial intelligence\u201d reinforces these beliefs: ChatGPT uses first-person pronouns, and we say AIs \u201challucinate.\u201d These agentic roles we give AIs can undermine the credit to creators whose labor underlies the system\u2019s outputs, and can deflect responsibility from the developers and decision makers when the systems cause harm.\nWe\u2019re trying to build coalitions across academia and beyond to help think about the interdisciplinary connections and research areas necessary to grapple with the immediate dangers to humans coming from the deployment of these tools, such as disinformation, job displacement, and changes to legal structures and culture.\nQ: What do you see as the gaps in research around generative AI and art today?\nA: The way we talk about AI is broken in many ways. We need to understand how perceptions of the generative process affect attitudes toward outputs and authors, and also design the interfaces and systems in a way that is really transparent about the generative process and avoids some of these misleading interpretations. How do we talk about AI and how do these narratives cut along lines of power? As we outline in the article, there are these themes around AI\u2019s impact that are important to consider: aesthetics and culture; legal aspects of ownership and credit; labor; and the impacts to the media ecosystem. For each of those we highlight the big open questions.\nWith aesthetics and culture, we\u2019re considering how past art technologies can inform how we think about AI. For example, when photography was invented, some painters said it was \u201cthe end of art.\u201d But instead it ended up being its own medium and eventually liberated painting from realism, giving rise to Impressionism and the modern art movement. We\u2019re saying generative AI is a medium with its own affordances. The nature of art will evolve with that. How will artists and creators express their intent and style through this new medium?\nIssues around ownership and credit are tricky because we need copyright law that benefits creators, users, and society at large. Today\u2019s copyright laws might not adequately apportion rights to artists when these systems are training on their styles. When it comes to training data, what does it mean to copy? That\u2019s a legal question, but also a technical question. We\u2019re trying to understand if these systems are copying, and when.\nFor labor economics and creative work, the idea is these generative AI systems can accelerate the creative process in many ways, but they can also remove the ideation process that starts with a blank slate. Sometimes, there\u2019s actually good that comes from starting with a blank page. We don\u2019t know how it\u2019s going to influence creativity, and we need a better understanding of how AI will affect the different stages of the creative process. We need to think carefully about how we use these tools to complement people\u2019s work instead of replacing it.\nIn terms of generative AI\u2019s effect on the media ecosystem, with the ability to produce synthetic media at scale, the risk of AI-generated misinformation must be considered. We need to safeguard the media ecosystem against the possibility of massive fraud on one hand, and people losing trust in real media on the other.\nQ: How do you hope this paper is received \u2014 and by whom?\nA: The conversation about AI has been very fragmented and frustrating. Because the technologies are moving so fast, it\u2019s been hard to think deeply about these ideas. To ensure the beneficial use of these technologies, we need to build shared language and start to understand where to focus our attention. We\u2019re hoping this paper can be a step in that direction. We\u2019re trying to start a conversation that can help us build a roadmap toward understanding this fast-moving situation.\nArtists many times are at the vanguard of new technologies. They\u2019re playing with the technology long before there are commercial applications. They\u2019re exploring how it works, and they\u2019re wrestling with the ethics of it. AI art has been going on for over a decade, and for as long these artists have been grappling with the questions we now face as a society. I think it is critical to uplift the voices of the artists and other creative laborers whose jobs will be impacted by these tools. Art is how we express our humanity. It\u2019s a core human, emotional part of life. In that way we believe it\u2019s at the center of broader questions about AI\u2019s impact on society, and hopefully we can ground that discussion with this.\n',
)

if __name__ == "__main__":
    print(orca_mini_3b(blog_text, 64, 0.7, 40, 0.2, 1.8, 128, 8, None, False))
