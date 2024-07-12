from openai import OpenAI

client = OpenAI()

def query_llm(prompt, model="gpt-3.5-turbo"):
    completions = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return completions.choices[0].message.content

def get_answer(question, context_documents):
    context_divider = "\n---\n"
    question = question.strip()
    context = context_divider.join(context_documents)
    template_rag = (
        "You are an assistant in the Human Resources department of an outsourcing company.\n"
        "Respond to the question based on the context required by the employee.\n"
        "The context is delimited by the inverted commas.\n"
        "```\n"
        "{context}\n"
        "```\n"
        "Question: {question}\n"
    )
    final_prompt = template_rag.format(context=context, question=question)
    return query_llm(final_prompt)