import os
from dotenv import load_dotenv
from crewai import LLM,Agent,Crew,Process
import crewai.llms.cache as crew_cache
from crewai_tools import SerperDevTool
crew_cache.mark_cache_breakpoint=lambda msg:msg


load_dotenv()

llm=LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

search_tool=SerperDevTool()



news_agent=Agent(
    role="Stock News Analyst",
    goal="Analyze recent news related to a given stock and identify news that could affect its price.",
    backstory="You are experinced financial news analyst who focuses on identifying important events and their potential impact on stock prices .",
    llm=llm,
    tools=[search_tool]
)

from crewai import Task


news_task=Task(
    description=
    """
Search the internet for recent and relevant news about {stock}.

Identify:
1.Important recent news
2.Wheather each news item is positive , negative, or neutral
3.Why it may affect the company
4.The source/title of the news

Do not make up news. Use the search tool to find actual information.
""",

expected_output="""
A concise report contating:
1.Important recent news
2.Their potential impact
3.Overall news sentiment
""",

agent=news_agent
)

crew=Crew(
    agents=[news_agent],
    tasks=[news_task],
    process=Process.sequential,
    verbose=True
)

stock=input("Enter Stock name: ")

result = crew.kickoff(
    inputs={"stock":stock}
)

print(result)