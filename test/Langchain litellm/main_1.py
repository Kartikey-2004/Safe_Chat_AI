from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_litellm import ChatLiteLLM

llm = ChatLiteLLM(
    model="gpt-4o-mini",
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI tutor named KrishGPT. Be concise.",
        ),
        (
            "user",
            "{question}",
        ),
    ]
)

chain = prompt | llm | StrOutputParser()

answer = chain.invoke({"question": "What is an LLM Gateway in 3 bullets?"})
print(answer)
