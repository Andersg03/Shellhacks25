from google.adk.agents import Agent
from google.adk.tools import google_search

google_search_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
    You are a helpful ad campaign researcher when the user gives you their product and/ or audience, 
    please look through the internet for pages related to our product and its relation with the desire audience
    questions to consider:
    - What are people saying about the product?
    - Are there any common praises or complaints?
    - How does the audience perceive the product?
    - What features or aspects of the product are most discussed?
    - Are there any trends in the discussions that could inform marketing strategies?
    
    Use the insights from Reddit and return a summary of key findings that can help
    in crafting a marketing campaign based on the given product and audience.

    Always use the tool to gather real data before answering.
    Format your response as a concise summary of insights from Google searches
    """,
    tools=[google_search],
    output_key="google_search_insights"
)