from google.adk.agents import Agent
from fetchreddit import search_product_mentions

reddit_agent = Agent(
    name="reddit_agent",
    model="gemini-2.0-flash",
    description="Collects reddit posts about the product and audience.",
    instructions="""
    When given a product and audience, use the fetchreddit tool to search for relevant posts on Reddit.
    questions to consider:
    - What are people saying about the product?
    - Are there any common praises or complaints?
    - How does the audience perceive the product?
    - What features or aspects of the product are most discussed?
    - Are there any trends in the discussions that could inform marketing strategies?
    
    Use the insights from Reddit and return a summary of key findings that can help
    in crafting a marketing campaign based on the given product and audience.

    Always use the tool to gather real data before answering.
    Format your response as a concise summary of insights from Reddit posts.
    """,
    tools=[search_product_mentions],
    output_key="reddit_insights"
)