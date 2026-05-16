from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
from rich import print

print("Agents.py Output:")

load_dotenv()

def _last_message_text(result: dict) -> str:
    messages = result.get("messages", [])
    if not messages:
        return ""
    last = messages[-1]
    return getattr(last, "content", str(last))

#model setup 
llm = ChatOpenAI(model = "gpt-4o-mini",temperature=0)


#1st agent 
def build_search_agent():
    print("[agents] building search agent...")
    agent = create_agent(model=llm, tools=[web_search])
    print("[agents] search agent ready")
    return agent

#2nd agent 
def build_reader_agent():
    print("[agents] building reader agent...")
    agent = create_agent(model=llm, tools=[scrape_url])
    print("[agents] reader agent ready")
    return agent

#writer chain 
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 
critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
     ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()


if __name__ == "__main__":
    topic = "What is LangGraph?"

    print("\n========== STEP 1: Search agent ==========")
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [{"role": "user", "content": f"Research this topic: {topic}"}],
    })
    research = _last_message_text(search_result)
    print("[search_agent] last message:\n", research)

    print("\n========== STEP 2: Writer chain ==========")
    report = writer_chain.invoke({"topic": topic, "research": research})
    print("[writer_chain] report:\n", report)

    print("\n========== STEP 3: Critic chain ==========")
    critique = critic_chain.invoke({"report": report})
    print("[critic_chain] critique:\n", critique)

    print("\n========== DONE ==========")
