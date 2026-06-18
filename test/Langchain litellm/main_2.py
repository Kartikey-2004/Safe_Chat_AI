from langchain_litellm import ChatLiteLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

primary = ChatLiteLLM(model="gpt-x")
fallback_1 = ChatLiteLLM(model="gpt-4o-mini", temperature=0.2)
fallback_2 = ChatLiteLLM(model="groq/llama-3.3-70b-versatile", temperature=0.2)

robust_llm = primary.with_fallbacks([fallback_1, fallback_2])

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            'You are an expert AI engineer. Always reply in JSON: {{"answer": ...}}',
        ),
        (
            "user",
            "{question}",
        ),
    ]
)

chain = prompt | robust_llm | StrOutputParser()

result = chain.invoke(
    {"question": "What are the top 3 benefits of an LLM Gateway?"},
)
print(result)
